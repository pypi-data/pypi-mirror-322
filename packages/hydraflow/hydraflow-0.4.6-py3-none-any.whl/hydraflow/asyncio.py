"""Provide functionality for running commands and monitoring file changes."""

from __future__ import annotations

import asyncio
import logging
from asyncio.subprocess import PIPE
from pathlib import Path
from typing import TYPE_CHECKING

import watchfiles

if TYPE_CHECKING:
    from asyncio.streams import StreamReader
    from collections.abc import Callable

    from watchfiles import Change


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def execute_command(
    program: str,
    *args: str,
    stdout: Callable[[str], None] | None = None,
    stderr: Callable[[str], None] | None = None,
    stop_event: asyncio.Event,
) -> int:
    """Run a command asynchronously and pass the output to callback functions.

    Args:
        program (str): The program to run.
        *args (str): Arguments for the program.
        stdout (Callable[[str], None] | None): Callback for standard output.
        stderr (Callable[[str], None] | None): Callback for standard error.
        stop_event (asyncio.Event): Event to signal when the process is done.

    Returns:
        int: The return code of the process.

    """
    try:
        process = await asyncio.create_subprocess_exec(
            program,
            *args,
            stdout=PIPE,
            stderr=PIPE,
        )
        await asyncio.gather(
            process_stream(process.stdout, stdout),
            process_stream(process.stderr, stderr),
        )
        returncode = await process.wait()

    except Exception as e:
        msg = f"Error running command: {e}"
        logger.exception(msg)
        returncode = 1

    finally:
        stop_event.set()

    return returncode


async def process_stream(
    stream: StreamReader | None,
    callback: Callable[[str], None] | None,
) -> None:
    """Read a stream asynchronously and pass each line to a callback function.

    Args:
        stream (StreamReader | None): The stream to read from.
        callback (Callable[[str], None] | None): The callback function to handle
        each line.

    """
    if stream is None or callback is None:
        return

    while True:
        line = await stream.readline()
        if line:
            callback(line.decode().strip())
        else:
            break


async def monitor_file_changes(
    paths: list[str | Path],
    callback: Callable[[set[tuple[Change, str]]], None],
    stop_event: asyncio.Event,
    **awatch_kwargs,
) -> None:
    """Watch file changes in specified paths and pass the changes to a callback.

    Args:
        paths (list[str | Path]): List of paths to monitor for changes.
        callback (Callable[[set[tuple[Change, str]]], None]): The callback
        function to handle file changes.
        stop_event (asyncio.Event): Event to signal when to stop watching.
        **awatch_kwargs: Additional keyword arguments to pass to watchfiles.awatch.

    """
    str_paths = [str(path) for path in paths]
    try:
        async for changes in watchfiles.awatch(
            *str_paths,
            stop_event=stop_event,
            **awatch_kwargs,
        ):
            callback(changes)
    except Exception as e:
        msg = f"Error watching files: {e}"
        logger.exception(msg)
        raise


async def run_and_monitor(
    program: str,
    *args: str,
    stdout: Callable[[str], None] | None = None,
    stderr: Callable[[str], None] | None = None,
    watch: Callable[[set[tuple[Change, str]]], None] | None = None,
    paths: list[str | Path] | None = None,
    **awatch_kwargs,
) -> int:
    """Run a command and optionally watch for file changes concurrently.

    Args:
        program (str): The program to run.
        *args (str): Arguments for the program.
        stdout (Callable[[str], None] | None): Callback for standard output.
        stderr (Callable[[str], None] | None): Callback for standard error.
        watch (Callable[[set[tuple[Change, str]]], None] | None): Callback for
        file changes.
        paths (list[str | Path] | None): List of paths to monitor for changes.
        **awatch_kwargs: Additional keyword arguments to pass to `watchfiles.awatch`.

    """
    stop_event = asyncio.Event()
    run_task = asyncio.create_task(
        execute_command(
            program,
            *args,
            stop_event=stop_event,
            stdout=stdout,
            stderr=stderr,
        ),
    )
    if watch and paths:
        coro = monitor_file_changes(paths, watch, stop_event, **awatch_kwargs)
        monitor_task = asyncio.create_task(coro)
    else:
        monitor_task = None

    try:
        if monitor_task:
            await asyncio.gather(run_task, monitor_task)
        else:
            await run_task

    except Exception as e:
        msg = f"Error in run_and_monitor: {e}"
        logger.exception(msg)
        raise

    finally:
        stop_event.set()
        await run_task
        if monitor_task:
            await monitor_task

    return run_task.result()


def run(
    program: str,
    *args: str,
    stdout: Callable[[str], None] | None = None,
    stderr: Callable[[str], None] | None = None,
    watch: Callable[[set[tuple[Change, str]]], None] | None = None,
    paths: list[str | Path] | None = None,
    **awatch_kwargs,
) -> int:
    """Run a command synchronously and optionally watch for file changes.

    This function is a synchronous wrapper around the asynchronous
    `run_and_monitor` function. It runs a specified command and optionally
    monitors specified paths for file changes, invoking the provided callbacks for
    standard output, standard error, and file changes.

    Args:
        program (str): The program to run.
        *args (str): Arguments for the program.
        stdout (Callable[[str], None] | None): Callback for handling standard
            output lines.
        stderr (Callable[[str], None] | None): Callback for handling standard
            error lines.
        watch (Callable[[set[tuple[Change, str]]], None] | None): Callback for
            handling file changes.
        paths (list[str | Path] | None): List of paths to monitor for file
            changes.
        **awatch_kwargs: Additional keyword arguments to pass to
            `watchfiles.awatch`.

    Returns:
        int: The return code of the process.

    """
    if watch and not paths:
        paths = [Path.cwd()]

    return asyncio.run(
        run_and_monitor(
            program,
            *args,
            stdout=stdout,
            stderr=stderr,
            watch=watch,
            paths=paths,
            **awatch_kwargs,
        ),
    )
