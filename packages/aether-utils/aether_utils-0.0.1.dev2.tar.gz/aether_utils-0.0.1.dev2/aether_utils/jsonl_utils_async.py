# Note that this should be moved to aether-utils in due course
# It will require Python>=3.11, though

import asyncio
import dataclasses
import json
import logging
import pathlib
import tempfile
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional

from aether_utils.logging_utils import get_standard_logger_for_file

_logger = get_standard_logger_for_file(__file__)


class _WorkCompleteMarker:
    def __init__(self, message: str):
        self._message = message

    @property
    def message(self) -> str:
        return self._message


@dataclasses.dataclass
class RunStats:
    success_count: int = int()
    failure_count: int = int()


async def _enqueue_from_jsonl(
    *,
    source_file: pathlib.Path,
    source_encoding: str,
    target_queue: asyncio.Queue,
    n_complete_markers: int,
    logger: logging.Logger,
):
    logger.info(f"Source file {source_file}")

    lines_read = 0
    with open(source_file, "r", encoding=source_encoding) as in_file:
        for nxt in in_file:
            logger.info(f"Reading line {lines_read}")
            nxt_dict = json.loads(nxt)
            await target_queue.put(nxt_dict)
            lines_read += 1

    for i in range(n_complete_markers):
        logger.info(f"WorkerCompleteMarker {i}")
        nxt_marker = _WorkCompleteMarker(f"Completion marker {i}")
        await target_queue.put(nxt_marker)
    logger.info(f"Completed")


async def _jsonl_from_queue(
    *,
    dest_file: pathlib.Path,
    dest_encoding: str,
    target_queue: asyncio.Queue,
    n_complete_markers_expected: int,
    logger: logging.Logger,
):
    logger.info(f"Destination file {dest_file}")

    n_complete_markers_seen = 0

    with open(dest_file, "w", encoding=dest_encoding) as out_file:
        while n_complete_markers_seen < n_complete_markers_expected:
            nxt_item = await target_queue.get()

            if isinstance(nxt_item, _WorkCompleteMarker):
                logger.info(f"Got WorkCompleteMarker '{nxt_item.message}'")
                n_complete_markers_seen += 1
            else:
                logger.info(f"Writing item")
                nxt_output = json.dumps(nxt_item)
                out_file.write(nxt_output)
                out_file.write("\n")


async def _error_jsonl_from_queue(
    *,
    error_file: Optional[pathlib.Path],
    error_encoding: Optional[str],
    target_queue: asyncio.Queue,
    n_complete_markers_expected: int,
    n_errors_max: int,
    logger: logging.Logger,
):
    logger.info(f"Starting error logger")

    def get_error_file(error_file_path: Optional[pathlib.Path]):
        if error_file_path:
            return open(error_file_path, "a", encoding=error_encoding)
        else:
            return tempfile.TemporaryFile(mode="w", encoding="utf-8-sig")

    n_complete_markers_seen = 0
    n_errors_seen = 0

    with get_error_file(error_file) as err_file:
        while n_complete_markers_seen < n_complete_markers_expected:
            nxt_item = await target_queue.get()

            if isinstance(nxt_item, _WorkCompleteMarker):
                logger.info(f"Got WorkCompleteMarker '{nxt_item.message}'")
                n_complete_markers_seen += 1
            else:
                n_errors_seen += 1
                logger.warning(f"Received Error Item (total={n_errors_seen})")
                nxt_output = json.dumps(nxt_item)
                err_file.write(nxt_output)
                err_file.write("\n")

            if n_errors_seen > n_errors_max:
                logger.fatal(f"Error limit of {n_errors_max} exceeded")
                raise ValueError("Too many error items")


async def _queue_worker(
    *,
    map_func: Callable[
        [Dict[str, Any], logging.Logger], Awaitable[Optional[Dict[str, Any]]]
    ],
    source_queue: asyncio.Queue,
    dest_queue: asyncio.Queue,
    error_queue: asyncio.Queue,
    worker_time_queue: asyncio.Queue,
    logger: logging.Logger,
) -> RunStats:
    logger.info(f"Starting")
    done = False
    success_count = 0
    failure_count = 0
    while not done:
        nxt_item = await source_queue.get()

        if isinstance(nxt_item, _WorkCompleteMarker):
            logger.info(f"Got WorkCompleteMarker '{nxt_item.message}'")
            done = True
        else:
            logger.info(f"Processing item")
            start_time = time.time()
            try:
                nxt_result = await map_func(nxt_item, logger)
                stop_time = time.time()
                if nxt_result is not None:
                    await dest_queue.put(nxt_result)
                else:
                    logger.info("map_func returned None")
                await worker_time_queue.put(stop_time - start_time)
                success_count += 1
            except Exception as e:
                stop_time = time.time()
                logger.exception(f"Item failed")
                await error_queue.put(nxt_item)
                await worker_time_queue.put(stop_time - start_time)
                failure_count += 1
    logger.info(f"Completed work items")
    marker = _WorkCompleteMarker("queue_worker")
    await dest_queue.put(marker)
    await error_queue.put(marker)
    await worker_time_queue.put(marker)
    logger.info(f"Exiting")
    return RunStats(success_count=success_count, failure_count=failure_count)


async def _queue_worker_many(
    *,
    map_func: Callable[
        [Dict[str, Any], logging.Logger], Awaitable[List[Dict[str, Any]]]
    ],
    source_queue: asyncio.Queue,
    dest_queue: asyncio.Queue,
    error_queue: asyncio.Queue,
    worker_time_queue: asyncio.Queue,
    logger: logging.Logger,
) -> RunStats:
    logger.info(f"Starting")
    done = False
    success_count = 0
    failure_count = 0
    while not done:
        nxt_item = await source_queue.get()

        if isinstance(nxt_item, _WorkCompleteMarker):
            logger.info(f"Got WorkCompleteMarker '{nxt_item.message}'")
            done = True
        else:
            logger.info(f"Processing item")
            start_time = time.time()
            try:
                nxt_result = await map_func(nxt_item, logger)
                stop_time = time.time()
                for n_r in nxt_result:
                    await dest_queue.put(n_r)
                await worker_time_queue.put(stop_time - start_time)
                success_count += 1
            except Exception as e:
                stop_time = time.time()
                logger.exception(f"Item failed: {nxt_item}")
                await error_queue.put(nxt_item)
                await worker_time_queue.put(stop_time - start_time)
                failure_count += 1
    logger.info(f"Completed work items")
    marker = _WorkCompleteMarker("queue_worker")
    await dest_queue.put(marker)
    await error_queue.put(marker)
    await worker_time_queue.put(marker)
    logger.info(f"Exiting")
    return RunStats(success_count=success_count, failure_count=failure_count)


async def _monitor_worker(
    *,
    source_queue: asyncio.Queue,
    dest_queue: asyncio.Queue,
    worker_time_queue: asyncio.Queue,
    n_complete_markers_expected: int,
    logger: logging.Logger,
):
    UPDATE_SECS = 30
    logger.info("Starting")
    all_times = []

    n_complete_markers_seen = 0
    while n_complete_markers_seen < n_complete_markers_expected:
        await asyncio.sleep(UPDATE_SECS / (1 + n_complete_markers_seen))
        src_count = source_queue.qsize()
        dst_count = dest_queue.qsize()

        # With no get_nowait() we can safely drain the
        # queue without worrying about concurrency
        for _ in range(worker_time_queue.qsize()):
            fetched = worker_time_queue.get_nowait()
            if isinstance(fetched, _WorkCompleteMarker):
                n_complete_markers_seen += 1
            else:
                all_times.append(fetched)

        min_time = -1
        max_time = -1
        mean_time = -1
        if len(all_times) > 0:
            min_time = min(all_times)
            max_time = max(all_times)
            mean_time = sum(all_times) / len(all_times)

        logger.info(f"Items in Source Queue: {src_count}")
        logger.info(f"Items in Destination Queue: {dst_count}")
        logger.info(f"Items processed so far: {len(all_times)}")
        logger.info(
            f"Times: {min_time:.2f}s (min) {mean_time:.2f}s (mean) {max_time:.2f}s (max)"
        )
    logger.info("Completed")


async def line_map_async(
    *,
    map_func: Callable[
        [Dict[str, Any], logging.Logger], Awaitable[Optional[Dict[str, Any]]]
    ],
    source_file: pathlib.Path,
    source_encoding: str,
    dest_file: pathlib.Path,
    dest_encoding: str,
    n_worker_tasks: int,
    error_file: Optional[pathlib.Path] = None,
    error_encoding: Optional[str] = None,
    n_errors_max: int = 5,
) -> RunStats:
    """
    Run an asynchronous 'map' operation on a JSONL input file.

    The `map_func` is an awaitable callable, which takes two arguments; the
    next line from the input JSONL file (in the form of a dictionary) and
    a logger.
    It is expected to return a dictionary which will become the next line
    in the output JSONL file.
    If `map_func` returns `None` then no output is generated for that
    input line.
    The optional `error_file` will have any items in the input file which
    cause an exception to be thrown.
    All three files can have their text encoding set independently.

    Internally, this function splits into three main sections.
    These are an asynchronous input file reader, the workers which run the
    `map_func`, and finally an asynchronous output file writer.
    These are linked via `asyncio.Queue`s.
    Two additional tasks handle the error output file and logging of
    performance information.
    """
    assert source_file.exists()

    source_queue = asyncio.Queue(maxsize=2 * n_worker_tasks)
    dest_queue = asyncio.Queue(maxsize=2 * n_worker_tasks)
    error_queue = asyncio.Queue(maxsize=n_worker_tasks)
    timing_queue = asyncio.Queue()

    _logger.info("Starting up TaskGroup")
    worker_tasks = []
    async with asyncio.TaskGroup() as tg:
        # The task to read in the input file
        _ = tg.create_task(
            _enqueue_from_jsonl(
                source_file=source_file,
                source_encoding=source_encoding,
                target_queue=source_queue,
                n_complete_markers=n_worker_tasks,
                logger=logging.getLogger(f"Enqueuer"),
            ),
            name="JSONL Reader",
        )
        # The worker tasks
        for i in range(n_worker_tasks):
            nxt = tg.create_task(
                _queue_worker(
                    map_func=map_func,
                    source_queue=source_queue,
                    dest_queue=dest_queue,
                    error_queue=error_queue,
                    worker_time_queue=timing_queue,
                    logger=logging.getLogger(f"Worker {i}"),
                ),
                name=f"Queue Worker {i}",
            )
            worker_tasks.append(nxt)
        # The task to write the output file
        _ = tg.create_task(
            _jsonl_from_queue(
                dest_file=dest_file,
                dest_encoding=dest_encoding,
                target_queue=dest_queue,
                n_complete_markers_expected=n_worker_tasks,
                logger=logging.getLogger(f"Dest File Writer"),
            )
        )
        # The task to write the error file
        _ = tg.create_task(
            _error_jsonl_from_queue(
                error_file=error_file,
                error_encoding=error_encoding,
                target_queue=error_queue,
                n_complete_markers_expected=n_worker_tasks,
                n_errors_max=n_errors_max,
                logger=logging.getLogger("Error File Writer"),
            )
        )
        # The task to log performance stats
        _ = tg.create_task(
            _monitor_worker(
                source_queue=source_queue,
                dest_queue=dest_queue,
                worker_time_queue=timing_queue,
                n_complete_markers_expected=n_worker_tasks,
                logger=logging.getLogger(f"Monitor"),
            )
        )
    _logger.info("All tasks complete")
    success_count = 0
    failure_count = 0
    for t in worker_tasks:
        success_count += t.result().success_count
        failure_count += t.result().failure_count

    return RunStats(success_count=success_count, failure_count=failure_count)


async def line_map_many_async(
    *,
    map_many_func: Callable[
        [Dict[str, Any], logging.Logger], Awaitable[List[Dict[str, Any]]]
    ],
    source_file: pathlib.Path,
    source_encoding: str,
    dest_file: pathlib.Path,
    dest_encoding: str,
    n_worker_tasks: int,
    error_file: Optional[pathlib.Path] = None,
    error_encoding: Optional[str] = None,
    n_errors_max: int = 5,
) -> RunStats:
    """
    Run an asynchronous 'map_many' operation on a JSONL input file.

    The `map_many_func` is an awaitable callable, which takes two arguments; the
    next line from the input JSONL file (in the form of a dictionary) and
    a logger.
    It is expected to return a list of dictionaries, each of which will become
    a new line in the output file.
    The optional `error_file` will have any items in the input file which
    cause an exception to be thrown.
    All three files can have their text encoding set independently.

    Internally, this function splits into three main sections.
    These are an asynchronous input file reader, the workers which run the
    `map_many_func`, and finally an asynchronous output file writer.
    These are linked via `asyncio.Queue`s.
    Two additional tasks handle the error output file and logging of
    performance information.
    """
    assert source_file.exists()

    source_queue = asyncio.Queue(maxsize=2 * n_worker_tasks)
    dest_queue = asyncio.Queue(maxsize=2 * n_worker_tasks)
    error_queue = asyncio.Queue(maxsize=n_worker_tasks)
    timing_queue = asyncio.Queue()

    _logger.info("Starting up TaskGroup")
    worker_tasks = []
    async with asyncio.TaskGroup() as tg:
        # The task to read in the input file
        _ = tg.create_task(
            _enqueue_from_jsonl(
                source_file=source_file,
                source_encoding=source_encoding,
                target_queue=source_queue,
                n_complete_markers=n_worker_tasks,
                logger=logging.getLogger(f"Enqueuer"),
            ),
            name="JSONL Reader",
        )
        # The worker tasks
        for i in range(n_worker_tasks):
            nxt = tg.create_task(
                _queue_worker_many(
                    map_func=map_many_func,
                    source_queue=source_queue,
                    dest_queue=dest_queue,
                    error_queue=error_queue,
                    worker_time_queue=timing_queue,
                    logger=logging.getLogger(f"Worker {i}"),
                ),
                name=f"Queue Worker {i}",
            )
            worker_tasks.append(nxt)
        # The task to write the output file
        _ = tg.create_task(
            _jsonl_from_queue(
                dest_file=dest_file,
                dest_encoding=dest_encoding,
                target_queue=dest_queue,
                n_complete_markers_expected=n_worker_tasks,
                logger=logging.getLogger(f"Dest File Writer"),
            )
        )
        # The task to write the error file
        _ = tg.create_task(
            _error_jsonl_from_queue(
                error_file=error_file,
                error_encoding=error_encoding,
                target_queue=error_queue,
                n_complete_markers_expected=n_worker_tasks,
                n_errors_max=n_errors_max,
                logger=logging.getLogger("Error File Writer"),
            )
        )
        # The task to log performance stats
        _ = tg.create_task(
            _monitor_worker(
                source_queue=source_queue,
                dest_queue=dest_queue,
                worker_time_queue=timing_queue,
                n_complete_markers_expected=n_worker_tasks,
                logger=logging.getLogger(f"Monitor"),
            )
        )
    _logger.info("All tasks complete")
    success_count = 0
    failure_count = 0
    for t in worker_tasks:
        success_count += t.result().success_count
        failure_count += t.result().failure_count

    return RunStats(success_count=success_count, failure_count=failure_count)
