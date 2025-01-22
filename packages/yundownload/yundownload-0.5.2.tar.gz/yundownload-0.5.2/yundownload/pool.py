import asyncio
import time
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait, Future
from typing import TYPE_CHECKING, Callable, Optional, Awaitable

from niquests import Session, AsyncSession

from yundownload.core import Retry, Result, Status, Proxies, Auth
from yundownload.downloader import stream_downloader, slice_downloader, async_stream_downloader, async_slice_downloader
from yundownload.logger import logger

if TYPE_CHECKING:
    from yundownload.request import Request

"""
uvloop 优化协程
"""


class BaseDP:
    _retry: Retry = Retry()
    _future_list = []

    @abstractmethod
    def push(self, item: 'Request'):
        pass

    @abstractmethod
    def _task_fail(self, result: Result):
        pass

    @abstractmethod
    def _task_handle(self, item: 'Request'):
        pass

    @abstractmethod
    def _task_start(self, item: 'Request',
                    func: Callable[[Session | AsyncSession, 'Request'], Result]):
        pass

    @abstractmethod
    def close(self):
        pass


class DownloadPools(BaseDP):

    def __init__(
            self,
            max_workers: int = 5,
            timeout: int = 20,
            retry: Retry = Retry(),
            verify: bool = True,
            proxies: Optional['Proxies'] = None,
            auth: Optional['Auth'] = None,
    ) -> None:
        self._retry = retry
        self._max_workers = max_workers
        self._thread_pool: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=max_workers)
        self.timeout = timeout
        self.client = Session(
            retries=retry.retry_connect,
            pool_maxsize=max_workers,
            pool_connections=max_workers
        )
        if proxies is not None:
            self.client.mounts = {
                "http": proxies.http,
                "https": proxies.https,
            }
        if auth is not None:
            self.client.auth = (auth.username, auth.password)
        self.client.verify = verify

    def _task_start(self, item: 'Request',
                    func: Callable[['Session', 'Request', Callable], Result]) -> Result:
        return func(self.client, item, self._pool_submit)

    def push(self, item: 'Request'):
        logger.info(f'[{item.save_path.name}] push task')
        while len([1 for item in self._future_list if not item.done()]) >= self._max_workers - 1:
            logger.info('push task wait...')
            time.sleep(3)
        future: Future = self._pool_submit(self._task_handle, item)
        self._future_list.append(future)
        pass

    @property
    def _pool_submit(self):
        return self._thread_pool.submit

    def _task_handle(self, item: 'Request') -> Result:
        err = None
        slice_flag = False
        result = None
        for i in range(0, self._retry.retry + 1):
            try:
                if not slice_flag:
                    item.stat.close()
                    result = self._task_start(item, stream_downloader)
                    if result.status == Status.SLICE:
                        slice_flag = True
                if slice_flag:
                    item.stat.close()
                    result = self._task_start(item, slice_downloader)
                item.status = result.status
                return result
            except Exception as e:
                err = e
                if i < self._retry.retry:
                    logger.warning(
                        f"retrying {i} of {self._retry.retry}, error: {e} | line: {e.__traceback__.tb_lineno}")
                    time.sleep(self._retry.retry_delay)
                continue
        result = Result(
            status=Status.FAIL,
            request=item,
            error=err
        )
        self._task_fail(result)
        item.status = result.status
        return result

    def _task_fail(self, result: Result):
        result.request.error_callback(result)

    def results(self):
        logger.info('yundownload result')
        return [future.result() for future in self._future_list]

    def close(self):
        wait(self._future_list)
        self._thread_pool.shutdown(wait=True)
        logger.info('yundownload close')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncDownloadPools(BaseDP):

    def __init__(
            self,
            max_workers: int = 5,
            timeout: int = 20,
            retry: Retry = Retry(),
            verify: bool = True,
            proxies: Optional['Proxies'] = None,
            auth: Optional['Auth'] = None,
    ) -> None:
        self._retry = retry
        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(max_workers)
        self._max_workers = max_workers
        self.timeout = timeout
        self.client = AsyncSession(
            retries=retry.retry_connect,
            pool_maxsize=max_workers,
            pool_connections=max_workers
        )
        if proxies is not None:
            self.client.mounts = {
                "http": proxies.http,
                "https": proxies.https,
            }
        if auth is not None:
            self.client.auth = (auth.username, auth.password)
        self.client.verify = verify

    async def _task_start(self, item: 'Request',
                          func: Callable[[AsyncSession, 'Request', asyncio.Semaphore], Awaitable[Result]]):
        return await func(self.client, item, self._semaphore)

    async def push(self, item: 'Request'):
        logger.info(f'[{item.save_path.name}] push task')
        while len([1 for item in self._future_list if not item.done()]) >= self._max_workers:
            logger.info('push task wait...')
            await asyncio.sleep(3)
        future = asyncio.create_task(self._task_handle(item))
        self._future_list.append(future)

    async def _task_handle(self, item: 'Request') -> Result:
        err = None
        slice_flag = False
        result = None
        for i in range(0, self._retry.retry + 1):
            try:
                if not slice_flag:
                    item.stat.clear()
                    result = await self._task_start(item, async_stream_downloader)
                    if result.status == Status.SLICE:
                        slice_flag = True
                if slice_flag:
                    item.stat.clear()
                    result = await self._task_start(item, async_slice_downloader)
                item.status = result.status
                item.stat.close()
                return result
            except Exception as e:
                err = e
                if i < self._retry.retry:
                    logger.warning(
                        f"retrying... {i} of {self._retry.retry}, error msg: {e} line: {e.__traceback__.tb_lineno}",
                        exc_info=True
                    )
                    await asyncio.sleep(self._retry.retry_delay)
                continue
        result = Result(
            status=Status.FAIL,
            request=item,
            error=err
        )
        logger.error(err, exc_info=True)
        await self._task_fail(result)
        item.status = result.status
        item.stat.close()
        return result

    async def _task_fail(self, result: Result):
        await result.request.aerror_callback(result)

    async def results(self):
        logger.info('yundownload result')
        return await asyncio.gather(*self._future_list)

    async def close(self):
        await self.results()
        await self.client.close()
        logger.info('yundownload close')

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
