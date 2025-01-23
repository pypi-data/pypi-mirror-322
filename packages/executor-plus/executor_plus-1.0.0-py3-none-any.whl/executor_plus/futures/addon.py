# Author: Yuting Zhang
# This file is part of flexible_executor, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = ['PoolExecutorAddon']

from typing import Optional
from concurrent.futures import Future, Executor
from weakref import ProxyType


class PoolExecutorAddon:

    def __init__(self):
        from .executors import PoolExecutor
        self.executor: Optional[ProxyType[PoolExecutor]] = None

    def on_start(self) -> None:
        pass

    def initializer(self) -> None:
        pass

    def pre_submit(self) -> None:
        pass

    def post_submit(self, future: Future) -> None:
        pass

    def after_join(self) -> None:
        pass

