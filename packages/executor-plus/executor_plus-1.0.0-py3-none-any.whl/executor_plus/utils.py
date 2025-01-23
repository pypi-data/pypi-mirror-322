# Author: Yuting Zhang
# This file is part of flexible_executor, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'timeout_context_for_lock',
]

import contextlib
import multiprocessing
import multiprocessing as mp
import threading
import typing


@contextlib.contextmanager
def timeout_context_for_lock(lock: typing.Union[threading.Lock, mp.Lock], timeout=None):
    if timeout is None:
        timeout = -1
    lock.acquire(timeout=timeout)
    yield lock
    lock.release()
