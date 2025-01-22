import asyncio
import math
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import aiofiles
from niquests import Session, AsyncSession, Response, AsyncResponse

from yundownload.core import Result, Status
from yundownload.exception import NotSliceSizeError
from yundownload.logger import logger
from yundownload.utils import check_range_transborder, merge_file, async_check_range_transborder, async_merge_file

if TYPE_CHECKING:
    from yundownload.request import Request


def stream_downloader(
        client: Session,
        request: 'Request',
        poll_push: Callable
) -> Result:
    continued_flag = False
    request_headers = request.headers.copy()
    request.save_path.parent.mkdir(exist_ok=True, parents=True)
    if request.save_path.exists():
        request_headers['Range'] = f'bytes={request.save_path.stat().st_size}-'
        request.stat.push(request.save_path.stat().st_size)
    logger.info(f'[{request.save_path.name}] stream request wait...')

    response = client.request(
        method=request.method,
        url=request.url,
        timeout=request.timeout,
        params=request.params,
        data=request.data,
        headers=request_headers,
        cookies=request.cookies,
        auth=request.auth,
        stream=True
    )
    logger.info(f'[{request.save_path.name}] stream request success')
    if response.status_code == 416:
        check_range_transborder(
            client,
            request
        )
        logger.info(f'[{request.save_path.name}] The file already exists')
        return Result(
            status=Status.EXIST,
            request=request
        )
    response.raise_for_status()
    if response.headers.get('Accept-Ranges', None) == 'bytes' or response.status_code == 206:
        continued_flag = True
    elif response.headers.get('Content-Length', None) is not None and not request.save_path.exists():
        continued_flag = True

    correct_size = int(response.headers.get('Content-Length', -1))
    request.save_path.parent.mkdir(exist_ok=True, parents=True)
    request.correct_size = correct_size
    if correct_size:
        if continued_flag and correct_size > request.slice_threshold and not request.stream:
            logger.info(f'[{request.save_path.name}] select slice download')
            return Result(
                status=Status.SLICE,
                request=request
            )
    with request.save_path.open('ab' if continued_flag else 'wb') as f:
        for chunk in response.iter_content(request.stream_size):
            f.write(chunk)
            request.stat.push(len(chunk))

    logger.info(f'[{request.save_path.name}] file download success')
    result = Result(
        status=Status.SUCCESS,
        request=request
    )
    request.success_callback(result)
    return result


def slice_downloader(
        client: Session,
        request: 'Request',
        poll_push: Callable
) -> Result:
    if not request.correct_size:
        raise NotSliceSizeError(request.save_path)
    if request.correct_size / request.slice_size > 100:
        logger.warning(
            f'[{request.save_path} <{int(request.correct_size / request.slice_size)}>] slice size is too big')
        warnings.warn(
            f'[{request.save_path} <{int(request.correct_size / request.slice_size)}>] if the number of slices in the '
            f'file is too large, check whether the slices are too small')
    slice_flag_name = request.save_path.name.replace('.', '-')
    future_list = []
    logger.info(f'[{request.save_path}] <{math.ceil(request.correct_size / request.slice_size)}> slices')
    for start in range(0, request.correct_size, request.slice_size):
        end = start + request.slice_size - 1
        chunk_path = request.save_path.parent.joinpath(
            '{}--{}.ydstf'.format(
                slice_flag_name,
                start))
        future = poll_push(
            chunk_downloader,
            client,
            request,
            start,
            end,
            chunk_path
        )
        future_list.append(future)
    result = [future.result() for future in future_list]
    status = [res[0] for res in result]
    if all(status):
        merge_file(slice_flag_name, request.save_path)
        result = Result(
            status=Status.SUCCESS,
            request=request
        )
        request.success_callback(result)
        return result
    raise list(filter(lambda x: not x[0], result))[0][1]


def chunk_downloader(
        client: Session,
        request: 'Request',
        start: int,
        end: int,
        save_path: Path,
) -> (bool, None | Exception):
    logger.info(f'[{save_path}] chunk start download')
    headers = request.headers.copy()
    headers['Range'] = f'bytes={start}-{end}'
    if save_path.exists():
        if save_path.stat().st_size == request.slice_size:
            logger.info(f'[{save_path}] The file chunk already exists skip')
            return True, None
        elif save_path.stat().st_size > request.slice_size:
            save_path.unlink()
        else:
            request.stat.push(save_path.stat().st_size)
            chunk_start_size = start + save_path.stat().st_size
            headers['Range'] = f'bytes={chunk_start_size}-{end}'
            request.stat.push(save_path.stat().st_size)
            if chunk_start_size == request.correct_size:
                return True, None
    try:
        response = client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            data=request.data,
            headers=headers,
            cookies=request.cookies,
            auth=request.auth,
            timeout=request.timeout,
            stream=True
        )
        response: Response
        response.raise_for_status()
        with save_path.open('ab') as f:
            for chunk in response.iter_content(chunk_size=request.stream_size):
                f.write(chunk)
                request.stat.push(len(chunk))
        logger.info(f'[{save_path}] chunk download success')
        return True, None
    except Exception as e:
        logger.error(f'[{save_path}] chunk download error {e}', exc_info=True)
        return False, e


async def async_stream_downloader(
        client: AsyncSession,
        request: 'Request',
        semaphore: asyncio.Semaphore
) -> Result:
    continued_flag = False
    request_headers = request.headers.copy()
    request.save_path.parent.mkdir(exist_ok=True, parents=True)
    if request.save_path.exists():
        request_headers['Range'] = f'bytes={request.save_path.stat().st_size}-'
        await request.stat.apush(request.save_path.stat().st_size)
    logger.info(f'[{request.save_path.name}] stream request wait...')
    async with semaphore:
        response = await client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            data=request.data,
            headers=request_headers,
            cookies=request.cookies,
            auth=request.auth,
            timeout=request.timeout,
            stream=True
        )
        logger.info(f'[{request.save_path.name}] stream request success')
        response: AsyncResponse
        if response.status_code == 416:
            await async_check_range_transborder(
                client,
                request
            )
            logger.info(f'[{request.save_path.name}] The file already exists')
            return Result(
                status=Status.EXIST,
                request=request
            )
        response.raise_for_status()
        if response.headers.get('Accept-Ranges', None) == 'bytes' or response.status_code == 206:
            continued_flag = True
        elif response.headers.get('Content-Length', None) is not None and not request.save_path.exists():
            continued_flag = True

        correct_size = int(response.headers.get('Content-Length', -1))
        request.save_path.parent.mkdir(exist_ok=True, parents=True)
        request.correct_size = correct_size
        if correct_size:
            if continued_flag and correct_size > request.slice_threshold and not request.stream:
                return Result(
                    status=Status.SLICE,
                    request=request
                )
        async with aiofiles.open(request.save_path, 'ab' if continued_flag else 'wb') as f:
            async for chunk in response.aiter_bytes(chunk_size=request.stream_size):
                await f.write(chunk)
                await request.stat.apush(len(chunk))

        logger.info(f'[{request.save_path.name}] file download success')
        result = Result(
            status=Status.SUCCESS,
            request=request
        )
        await request.asuccess_callback(result)
        return result


async def async_slice_downloader(
        client: AsyncSession,
        request: 'Request',
        semaphore: asyncio.Semaphore
) -> Result:
    if not request.correct_size:
        raise NotSliceSizeError(request.save_path)
    if request.correct_size / request.slice_size > 100:
        logger.warning(
            f'[{request.save_path} <{int(request.correct_size / request.slice_size)}>] slice size is too big')
        warnings.warn(
            f'[{request.save_path} <{int(request.correct_size / request.slice_size)}>] if the number of slices in the '
            f'file is too large, check whether the slices are too small')
    slice_flag_name = request.save_path.name.replace('.', '-')
    task_list = []
    logger.info(f'[{request.save_path}] <{math.ceil(request.correct_size / request.slice_size)}> slices')
    for start in range(0, request.correct_size, request.slice_size):
        end = start + request.slice_size - 1
        chunk_path = request.save_path.parent.joinpath(
            '{}--{}.ydstf'.format(
                slice_flag_name,
                start))
        task_list.append(
            asyncio.create_task(
                async_chunk_downloader(
                    client,
                    request,
                    start,
                    end,
                    chunk_path,
                    semaphore)))
    result = await asyncio.gather(*task_list)
    status = [res[0] for res in result]
    if all(status):
        await async_merge_file(slice_flag_name, request.save_path)
        result = Result(
            status=Status.SUCCESS,
            request=request
        )
        await request.asuccess_callback(result)
        return result
    raise list(filter(lambda x: not x[0], result))[0][1]


async def async_chunk_downloader(
        client: AsyncSession,
        request: 'Request',
        start: int,
        end: int,
        save_path: Path,
        semaphore: asyncio.Semaphore
) -> (bool, None | Exception):
    logger.info(f'[{save_path}] chunk start download')
    headers = request.headers.copy()
    headers['Range'] = f'bytes={start}-{end}'
    if save_path.exists():
        if save_path.stat().st_size == request.slice_size:
            logger.info(f'[{save_path}] The file chunk already exists skip')
            return True, None
        elif save_path.stat().st_size > request.slice_size:
            save_path.unlink()
        else:
            await request.stat.apush(save_path.stat().st_size)
            chunk_start_size = start + save_path.stat().st_size
            headers['Range'] = f'bytes={chunk_start_size}-{end}'
            if chunk_start_size == request.correct_size:
                return True, None
    try:
        async with semaphore:
            response = await client.request(
                method=request.method,
                url=request.url,
                params=request.params,
                data=request.data,
                headers=headers,
                cookies=request.cookies,
                auth=request.auth,
                timeout=request.timeout,
                stream=True
            )
            response: AsyncResponse
            response.raise_for_status()
            async with aiofiles.open(save_path, 'ab') as f:
                async for chunk in await response.iter_content(chunk_size=request.stream_size):
                    await f.write(chunk)
                    await request.stat.apush(len(chunk))

            logger.info(f'[{save_path}] chunk download success')
            return True, None
    except Exception as e:
        logger.error(f'[{save_path}] Chunk download error {e}', exc_info=True)
        return False, e
