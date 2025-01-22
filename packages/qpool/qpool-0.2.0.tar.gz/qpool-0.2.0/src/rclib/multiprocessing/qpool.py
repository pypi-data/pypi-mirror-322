from __future__ import annotations
import asyncio
from uuid import uuid4
from annotated_types import Ge
from typing import (
    List,
    Any,
    Union,
    Optional,
    Dict,
    Type,
    Callable,
    Annotated,
)
import heapq
from pydantic import BaseModel, UUID4
from multiprocessing import Value, get_context

from contextlib import AsyncExitStack
from queue import Empty
from enum import Enum
from threading import Thread
import inspect
from rclib.multiprocessing.logging import setup_logging, log
from rclib.utils.errors.decorators import enforce_type_hints_contracts
from rclib.utils.dictionary import deep_merge
import logging
import time
from traceback import format_exc

from rclib.multiprocessing.models import (
    Identifiable,
    KeywordActionable,
    PositionalActionable,
    MixedActionable,
    RequiresProps,
    ProgressUpdate,
    Progresses,
    Retryable,
    Lifecycle,
    Actionable,
    TaskState,
    Evaluatable,
    ResultTaskPair,
)
from rclib.multiprocessing.tasks import (
    LogTask,
    ProgressTask,
    Task,
    ControlTask,
    ExitTask,
    EOQ,
    set_task_status,
)
from rclib.multiprocessing.queues import (
    ModelQueue,
    drain_queue,
    TaskQueue,
    LogQueue,
    ResultQueue,
    ControlQueue,
    ProgressQueue,
    explicitly_is,
    implicitly_is,
    log_task,
)
from rclib.multiprocessing.progress import run_progress, add


class WorkerState(Enum):
    """Enumeration of possible worker states over the course of a Worker lifecycle."""

    created = "created"  # Worker has been created but not yet started
    running = "running"  # Worker is running
    paused = "paused"  # Worker is paused, listening only for control commands
    stopped = "stopped"  # Worker has been stopped
    sleeping = "sleeping"  # Worker is sleeping, waiting for the next task


class Worker:
    def __init__(
        self,
        context: Any,
        actions: Dict[str, Callable],
        control_queues: Dict[str, ModelQueue],
        task_queue: ModelQueue,
        total_progress_tasks: Optional[Value] = None,
        log_queue: Optional[ModelQueue] = None,
        result_queue: Optional[ModelQueue] = None,
        progress_queue: Optional[ModelQueue] = None,
        props: Optional[Union[Dict[str, Any], BaseModel]] = None,
        name: Optional[str] = None,
        task_id: Optional[int] = -1,
        id: Optional[UUID4] = None,
        get_time: Callable[[], float] = time.monotonic,
    ) -> None:
        self.context = context
        self.total_progress_tasks = total_progress_tasks
        self.finished_tasks = self.context.Value("i", 0)
        self.total_tasks = self.context.Value("i", 0)
        self.last_update = None
        self.get_time = get_time
        self.start_time = get_time()
        self.id = id if id else uuid4()
        self.name = name if name else f"Worker-{self.id}"
        self.task_id = task_id
        self.control_queues = control_queues
        self.task_queue = task_queue
        self.log_queue = log_queue
        self.result_queue = result_queue
        self.retries = []
        self.progress = ProgressUpdate(task_id=self.task_id)
        self.progress_delta = ProgressUpdate(task_id=self.task_id)
        self.progress_queue = progress_queue
        self.is_retrying = False
        self.actions = actions
        # Props can be a dictionary or a BaseModel, if it's a BaseModel we'll dump it to a dictionary
        props = props if props else {}
        if isinstance(props, BaseModel):
            props = props.model_dump()
        self.props = props
        self.status = WorkerState.created

        self._process = self.context.Process(
            target=self.start_event_loop,
            kwargs={"actions": self.actions, "props": self.props},
            name=self.name,
        )

    def update_progress(self, force_update: bool = False):
        update = self.progress_delta.model_dump(exclude_unset=True)
        if self.progress_queue and (
            force_update
            or self.last_update is None
            or self.get_time() - self.last_update > 1
        ):
            self.last_update = self.get_time()
            merged = deep_merge(
                self.progress.model_dump(),
                update,
                strategies={
                    k: add if isinstance(v, (int, float)) else "override"
                    for k, v in self.progress
                },
            )
            self.progress = ProgressUpdate.parse_obj(merged)
            with self.total_progress_tasks.get_lock():
                self.total_progress_tasks.value += 1
            self.progress_queue.put(
                ProgressTask(
                    kwargs={"update": self.progress_delta},
                )
            )
            self.progress_delta = ProgressUpdate(task_id=self.task_id)

    def log(self, message: str, level: int):
        if self.log_queue:
            self.log_queue.put(
                LogTask(action="log", kwargs={"message": message, "level": level})
            )

    def start(self):
        if not self._process.is_alive():
            self.log(f"Starting process for {self.name}", logging.DEBUG)
            self._process.start()
            self.status = WorkerState.running

    async def execute_task(self, task: Actionable, func, props, is_async: bool):
        task_is_identifiable = isinstance(task, Identifiable)
        task_has_lifecycle = isinstance(task, Lifecycle)
        task_provides_progress = isinstance(task, Progresses)
        task_can_be_retried = isinstance(task, Retryable)
        task_requires_props = isinstance(task, RequiresProps)
        task_accepts_positional_args = isinstance(task, PositionalActionable)
        task_accepts_keyword_args = isinstance(task, KeywordActionable)
        task_accepts_mixed_args = isinstance(task, MixedActionable)
        task_can_be_evaluated_for_success = isinstance(task, Evaluatable)
        last_exception = None
        result_data = None
        try:
            if task_is_identifiable:
                log_task(
                    queue=self.log_queue,
                    task=task,
                    message=f"Executing task: {task.id}",
                    level=logging.INFO,
                )

            # Extract arguments from the task
            args = task.args if isinstance(task, PositionalActionable) else []
            kwargs = task.kwargs if isinstance(task, KeywordActionable) else {}

            # Handle props if the task requires them
            if task_requires_props:
                if task_accepts_keyword_args or task_accepts_mixed_args:
                    kwargs["props"] = task.filter_props(props=props)
                elif task_accepts_positional_args:
                    args.append(task.filter_props(props=props))

            # Execute the function/coroutine
            if is_async:
                if task_is_identifiable:
                    self.log(f"Running async task: {task.id}", logging.INFO)
                coroutine = func(*args, **kwargs)
                result_data = await coroutine
            else:
                if task_is_identifiable:
                    self.log(f"Running sync task: {task.id}", logging.INFO)
                result_data = func(*args, **kwargs)

            # Evaluate the result
            success = (
                task.evaluate(result_data)
                if task_can_be_evaluated_for_success
                else True
            )

            if not success:
                if task_is_identifiable:
                    log_task(
                        queue=self.log_queue,
                        task=task,
                        message=f"Task {task.id} failed on evaluation.",
                        level=logging.WARNING,
                    )

                set_task_status(task, TaskState.fail)
                return

            set_task_status(task, TaskState.success)

            if self.result_queue:
                if task_is_identifiable:
                    log_task(
                        queue=self.log_queue,
                        task=task,
                        message=f"Task {task.id} succeeded, pushing result to result queue. Result Queue has {self.result_queue.queue.qsize()} items.",
                        level=logging.DEBUG,
                    )

                self.result_queue.put(ResultTaskPair(task=task, result=result_data))
        except Exception:
            last_exception = format_exc()
            set_task_status(task, TaskState.fail)
            log_task(
                queue=self.log_queue,
                task=task,
                message=f"Error while executing task {task} with function {func}: {last_exception}",
                level=logging.ERROR,
            )
        finally:
            if task_has_lifecycle:
                if task.status == TaskState.fail:
                    task_can_be_retried = task_can_be_retried and task.remaining() > 0
                    if not task_can_be_retried:
                        if task_is_identifiable:
                            self.log(
                                f"Retries exhausted for task {task.id}", logging.WARNING
                            )
                        with self.finished_tasks.get_lock():
                            self.finished_tasks.value += 1
                        self.progress_delta.failures += 1
                        if self.result_queue:
                            self.result_queue.put(
                                ResultTaskPair(
                                    task=task, result=[last_exception, result_data]
                                )
                            )
                        if self.is_retrying:
                            self.progress_delta.completed += 1
                    else:
                        set_task_status(task, TaskState.retry)

                if task.status == TaskState.retry:
                    self.progress_delta.retries += 1
                    task.attempt()
                    if task.status == TaskState.retry:
                        if task_is_identifiable:
                            self.log(
                                f"Task {task.id} is being retried, {task.remaining()} retries remaining. Backing off...",
                                logging.INFO,
                            )
                        heapq.heappush(
                            self.retries, (self.get_time() + task.backoff(), task)
                        )
                    else:
                        # He's dead, Jim
                        self.progress_delta.failures += 1
                        self.result_queue.put(
                            ResultTaskPair(
                                task=task, result=[last_exception, result_data]
                            )
                        )
                elif task.status == TaskState.success:
                    self.progress_delta.completed += 1
                    with self.finished_tasks.get_lock():
                        self.finished_tasks.value += 1

                if task_provides_progress:
                    self.update_progress()

    def start_event_loop(self, actions: Dict[str, Callable], props: Dict[str, Any]):
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.log(f"Starting event loop for {self.name}", logging.DEBUG)
            self.loop.run_until_complete(self.run(actions, props=props))
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

    async def run(self, actions: Dict[str, Callable], props: Dict[str, Any]):
        self.task_done = 0
        # ======================================================================== #
        # Resolve all props and enter them as context managers if necessary
        # ======================================================================== #
        async with AsyncExitStack() as stack:
            for key, value in props.items():
                resolved_value = value
                if asyncio.iscoroutinefunction(value):
                    resolved_value = await value()
                elif callable(value):
                    resolved_value = value()

                if hasattr(resolved_value, "__aenter__") and hasattr(
                    resolved_value, "__aexit__"
                ):
                    resource = await stack.enter_async_context(resolved_value)
                    props[key] = resource
                elif hasattr(resolved_value, "__enter__") and hasattr(
                    resolved_value, "__exit__"
                ):
                    resource = stack.enter_context(resolved_value)
                    props[key] = resource
                else:
                    props[key] = resolved_value
            self.exit_stack = stack.pop_all()

        # Store the props on the worker
        self.props = props

        try:
            self.log(f"Worker {self.name} is running", logging.INFO)
            self.status = WorkerState.running
            self.progress_delta.status = f"Starting {self.name}"
            # ======================================================================== #
            # Main worker loop
            # ======================================================================== #
            while True:
                # Indicates if we're currently retrying a task, relevant as retried tasks are not in queues and do not require a task_done call
                self.is_retrying = False

                # Grab a failed task to retry if available
                self.progress_delta.status = f"Fetching retry tasks in {self.name}"
                task = None
                if (
                    self.retries
                    and self.retries[0]
                    and self.retries[0][0] <= self.get_time()
                ):
                    self.is_retrying = True
                    retry_time, task = heapq.heappop(self.retries)
                    self.log(
                        f"Worker {self.name} is retrying task {task} from the task queue",
                        logging.INFO,
                    )
                    self.progress_delta.status = f"Retrying task {task.id}"

                self.progress_delta.status = (
                    f"Checking for control tasks in {self.name}"
                )
                # If we didn't get a failed task to retry, try to get a new control task
                if task is None:
                    try:
                        for queue in self.control_queues.values():
                            control_task: Optional[ControlTask] = queue.get(block=False)
                            queue.task_done()
                            if (
                                isinstance(control_task, ExitTask)
                                # and total_tasks == finished_tasks
                            ):
                                self.log(
                                    f"Received exit task in worker {self.name}",
                                    logging.INFO,
                                )
                                self.status = WorkerState.stopped
                                return
                            else:
                                self.log(
                                    message=f"Worker {self.name} received control task {control_task} but is delaying as the conditions for it's execution are not yet met.",
                                    level=logging.INFO,
                                )
                                queue.put(control_task)
                    except Empty:
                        pass

                self.progress_delta.status = f"Checking for work tasks in {self.name}"
                # If we got neither a failed task to retry nor a control task, try to get a new task
                if task is None:
                    try:
                        task = self.task_queue.get(block=False)
                        if task:
                            self.progress_delta.total += 1
                            with self.total_tasks.get_lock():
                                self.total_tasks.value += 1
                            self.task_queue.task_done()
                    except Empty:
                        pass

                task_is_identifiable = isinstance(task, Identifiable)
                task_is_actionable = isinstance(task, Actionable)

                # If we got a valid non-control task by any means, process it
                if task is not None:
                    self.progress_delta.status = f"Attempting task {task.id}"
                    if task_is_identifiable:
                        self.log(
                            f"Worker {self.name} is attempting task {task.id}",
                            logging.INFO,
                        )
                    # If we have a task that maps to an action, execute it
                    if task_is_actionable:
                        self.active_task = task

                        set_task_status(task, TaskState.attempt)

                        func = self.actions[task.action]
                        await self.execute_task(
                            task=task,
                            func=func,
                            props=props,
                            is_async=inspect.iscoroutinefunction(func),
                        )
                else:
                    self.status = WorkerState.sleeping
                    await asyncio.sleep(0.1)
        except Exception as e:
            self.log(
                f"Worker {self.name} encountered an exception: {e}\n{format_exc()}",
                logging.ERROR,
            )
        finally:
            if self.progress_queue:
                self.progress_delta.status = f"Stopping worker {self.name}"
                self.update_progress(force_update=True)

            await self.exit_stack.aclose()


class Orchestrator:
    @enforce_type_hints_contracts
    def __init__(
        self,
        num_workers: Annotated[int, Ge(0)],
        actions: Dict[str, Callable],
        props: Optional[Dict[str, Any]] = None,
        show_progress: bool = False,
        task_models: List[Type[Task]] | None = None,
    ):
        task_models = (
            task_models if task_models is not None and len(task_models) > 0 else [Task]
        )
        self.context = get_context("spawn")

        self.total_progress_tasks = self.context.Value("i", 0)
        self.total_tasks = 0
        self.props = props if props is not None else {}
        self.started = False
        self.task_queue = TaskQueue(
            context=self.context, name="tasks", models=task_models, joinable=True
        )
        self.log_queue = LogQueue(context=self.context, name="log", joinable=True)
        self.result_queues = {}
        logger_id = uuid4()
        control_queue_name = f"control-{logger_id}"
        self.logger_control_queues = {
            f"{control_queue_name}": ControlQueue(
                context=self.context,
                name=f"{control_queue_name}",
                joinable=True,
            )
        }
        self.worker_control_queues = {}
        self.workers = []
        self.show_progress = show_progress
        self.progress_thread = None
        self.progress_queue = None
        if show_progress:
            self.progress_queue = ProgressQueue(
                context=self.context, name="progress", joinable=True
            )
            self.total_progress_tasks = self.context.Value("i", 0)
            self.remaining_progress_tasks = self.context.Value("i", 0)

        self.logger = Worker(
            context=self.context,
            name=f"logger-{logger_id}",
            id=uuid4(),
            total_progress_tasks=None,
            control_queues={"primary": self.logger_control_queues[control_queue_name]},
            task_queue=self.log_queue,
            actions={"log": log},
            props={"logger": setup_logging},
        )
        for i in range(num_workers):
            id = uuid4()
            control_queue_name = f"control-{id}"
            self.worker_control_queues[control_queue_name] = ControlQueue(
                context=self.context, name=control_queue_name, joinable=True
            )
            self.result_queues["worker-{i}"] = ResultQueue(
                context=self.context, name=f"worker-{i}-results", joinable=False
            )
            self.workers.append(
                Worker(
                    context=self.context,
                    name=f"worker-{i}",
                    id=id,
                    task_id=i,
                    control_queues={
                        "primary": self.worker_control_queues[control_queue_name]
                    },
                    log_queue=self.log_queue,
                    task_queue=self.task_queue,
                    result_queue=self.result_queues["worker-{i}"],
                    progress_queue=self.progress_queue,
                    total_progress_tasks=self.total_progress_tasks,
                    actions=actions,
                    props=self.props,
                )
            )

    @enforce_type_hints_contracts
    def update_progress(self, update: ProgressUpdate):
        with self.total_progress_tasks.get_lock():
            self.total_progress_tasks.value += 1
        if self.show_progress and self.progress_queue:
            self.progress_queue.put(
                ProgressTask(
                    kwargs={
                        "update": update,
                    }
                )
            )

    @enforce_type_hints_contracts
    def log(self, message: str, level: int):
        self.log_queue.put(
            LogTask(
                kwargs={
                    "message": message,
                    "level": level,
                }
            )
        )

    async def start_workers(self):
        """Starts workers and optionally monitors progress."""
        self.started = True
        self.logger.start()
        # Start workers
        self.log(
            message=f"Started logger with id {self.logger.id} and name {self.logger.name}",
            level=logging.DEBUG,
        )

        for worker in self.workers:
            worker.start()

        if self.show_progress:
            self.progress_thread = Thread(
                target=run_progress,
                args=(
                    self.progress_queue,
                    len(self.workers),
                    self.total_progress_tasks,
                    self.remaining_progress_tasks,
                ),
                daemon=True,
            )
            self.progress_thread.start()

    def _sum_worker_finished_tasks(self, workers: List[Worker]) -> int:
        total = 0
        for worker in workers:
            with worker.finished_tasks.get_lock():
                total += worker.finished_tasks.value
        return total

    async def stop_workers(self) -> List[ResultTaskPair]:
        """Stop workers and ensure progress monitoring is stopped properly."""
        self.log(message="Waiting for workers to finish tasks", level=logging.INFO)

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Waiting for workers to finish tasks",
            )
        )
        for worker in self.workers:
            total_finished_tasks = self._sum_worker_finished_tasks(self.workers)
            while self.total_tasks != total_finished_tasks:
                self.log(
                    message=f"Waiting for results to be processed {self.total_tasks} != {total_finished_tasks}",
                    level=logging.DEBUG,
                )
                await asyncio.sleep(0.1)
                total_finished_tasks = self._sum_worker_finished_tasks(self.workers)
        self.task_queue.close()
        self.task_queue.join()

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Closing worker control queues",
            )
        )
        # Stop all workers
        self.log(message="Closing worker control queues", level=logging.DEBUG)
        for control_queue in self.worker_control_queues.values():
            control_queue.put(ExitTask())
            control_queue.close()
            control_queue.join()

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Stopping worker processes",
            )
        )
        # Ensure all worker processes are properly terminated
        self.log(message="Joining worker processes", level=logging.INFO)
        results: List[ResultTaskPair] = []
        for worker in self.workers:
            if worker.result_queue:
                worker.result_queue.queue.put(ResultTaskPair(task=EOQ(), result=None))
            self.log(
                message=f"Draining results from worker {worker.name}",
                level=logging.DEBUG,
            )
            results.extend(drain_queue(worker.result_queue))
            worker._process.join()
            self.log(message=f"Worker-{worker.id} has exited.", level=logging.DEBUG)

        self.log(message="All workers have exited", level=logging.INFO)

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Closing final resources...",
            )
        )
        # Stop progress monitoring
        if self.show_progress and self.progress_queue and self.progress_thread:
            self.update_progress(ProgressUpdate(task_id=-1, total=-1))
            self.progress_queue.join()
            self.progress_thread.join()

        # Stop the logger
        self.log_queue.close()
        self.log_queue.join()
        for queue in self.logger_control_queues.values():
            queue.put(ExitTask())
            queue.close()
            queue.join()
        self.logger._process.join()
        return results

    @enforce_type_hints_contracts
    async def add_task(self, task: Task):
        """Add task to the task queue and start workers if not started."""
        self.total_tasks += 1
        await self.add_tasks([task])

    @enforce_type_hints_contracts
    async def add_tasks(self, tasks: List[Actionable]) -> List[Task]:
        """Add task to the task queue and start workers if not started."""
        if not self.started:
            await self.start_workers()

        self.total_tasks += len(tasks)
        enqueue_failures = []
        for task in tasks:
            set_task_status(task, TaskState.queue)
            if not self.task_queue.put(task):
                enqueue_failures.append(task)
        self.total_tasks -= len(enqueue_failures)
        added = len(tasks) - len(enqueue_failures)

        # Update progress if progress monitoring is enabled
        if self.show_progress and self.progress_queue and added:
            self.update_progress(
                ProgressUpdate(
                    task_id=-1,
                    total=len(tasks),
                )
            )
        self.log(
            message=f"Added {added} tasks to the task queue. Remaining: {len(enqueue_failures)}",
            level=logging.DEBUG,
        )
        return enqueue_failures
