import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from signal import signal, SIGINT
from typing import Coroutine, Callable
from logging import getLogger

from ..core.config import Config
from .strategy import Strategy

logger = getLogger(__name__)


class Executor:
    """Executor class for running multiple strategies on multiple symbols concurrently.

    Attributes:
        executor (ThreadPoolExecutor): The executor object.
        strategy_runners (list): List of strategies.
        coroutines (list[Coroutine]): A list of coroutines to run in the executor
        functions (dict[Callable, dict]): A dictionary of functions to run in the executor
    """

    executor: ThreadPoolExecutor
    tasks: list[asyncio.Task | asyncio.Future]
    config: Config

    def __init__(self):
        self.strategy_runners: list[Strategy] = []
        self.coroutines: list[Coroutine] = []
        self.coroutine_threads: list[Coroutine] = []
        self.functions: dict[Callable:dict] = {}
        self.tasks = []
        self.config = Config()
        self.timeout = None  # Timeout for the executor. For testing purposes only
        signal(SIGINT, self.sigint_handle)

    def add_function(self, *, function: Callable, kwargs: dict = None):
        kwargs = kwargs or {}
        self.functions[function] = kwargs

    def add_coroutine(self, *, coroutine: Callable | Coroutine, kwargs: dict = None, on_separate_thread=False):
        kwargs = kwargs or {}
        coroutine = coroutine(**kwargs)
        self.coroutines.append(coroutine) if on_separate_thread is False else self.coroutine_threads.append(coroutine)

    def add_strategies(self, *, strategies: tuple[Strategy]):
        """Add multiple strategies at once

        Args:
            strategies (Sequence[Strategy]): A sequence of strategies.
        """
        self.strategy_runners.extend(strategies)

    def add_strategy(self, *, strategy: Strategy):
        """Add a strategy instance to the list of workers

        Args:
            strategy (Strategy): A strategy object
        """
        self.strategy_runners.append(strategy)

    # async def create_strategy_task(self, strategy: Strategy):
    #     task = asyncio.create_task(strategy.run_strategy())
    #     self.tasks.append(task)
    #     await task

    def run_strategy(self, strategy: Strategy):
        """Wraps the coroutine trade method of each strategy with 'asyncio.run'.

        Args:
            strategy (Strategy): A strategy object
        """
        asyncio.run(strategy.run_strategy())

    async def create_coroutine_task(self, coroutine: Coroutine):
        task = asyncio.create_task(coroutine)
        self.tasks.append(task)
        await task

    async def create_coroutines_task(self):
        """"""
        tasks = [asyncio.create_task(coroutine) for coroutine in self.coroutines]
        self.tasks.extend(tasks)
        task = asyncio.gather(*tasks, return_exceptions=True)
        self.tasks.append(task)
        await task

    def run_coroutine_tasks(self):
        """Run all coroutines in the executor"""
        asyncio.run(self.create_coroutines_task())

    def run_coroutine_task(self, coroutine):
        asyncio.run(self.create_coroutine_task(coroutine))

    @staticmethod
    def run_function(function: Callable, kwargs: dict):
        """Run a function

        Args:
            function: The function to run
            kwargs: A dictionary of keyword arguments for the function
        """
        try:
            function(**kwargs)
        except Exception as err:
            logger.error(f"Error: {err}. Unable to run function: {function.__name__}")

    def sigint_handle(self, signum, frame):
        self.config.shutdown = True

    async def exit(self):
        """Shutdown the executor"""
        start = asyncio.get_event_loop().time()
        try:
            while self.config.shutdown is False and self.config.force_shutdown is False:
                if self.timeout is not None and self.timeout < (asyncio.get_event_loop().time() - start):
                    self.config.shutdown = True
                    break
                timeout = self.timeout or 30
                await asyncio.sleep(timeout)
            for strategy in self.strategy_runners:
                strategy.running = False

            if self.config.backtest_engine is not None:
                self.config.backtest_engine.stop_testing = True

            self.executor.shutdown(wait=False, cancel_futures=False)

            for task in self.tasks:
                task.cancel()

            if self.config.force_shutdown:
                os._exit(1)
        except Exception as err:
            logger.error("%s: Unable to shutdown executor", err)
            os._exit(1)

    def execute(self, *, workers: int = 5):
        """Run the strategies with a threadpool executor.

        Args:
            workers: Number of workers to use in executor pool. Defaults to 5.

        Notes:
            No matter the number specified, the executor will always use a minimum of 5 workers.
        """
        workers_ = len(self.strategy_runners) + len(self.functions) + len(self.coroutine_threads) + 3
        workers = max(workers, workers_)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            self.executor = executor
            [self.executor.submit(self.run_strategy, strategy) for strategy in self.strategy_runners]
            [self.executor.submit(function, **kwargs) for function, kwargs in self.functions.items()]
            [self.executor.submit(self.run_coroutine_task, coroutine) for coroutine in self.coroutine_threads]
            self.executor.submit(self.run_coroutine_tasks)
