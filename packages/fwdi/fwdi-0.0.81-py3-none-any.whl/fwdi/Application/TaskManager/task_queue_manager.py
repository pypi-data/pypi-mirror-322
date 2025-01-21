from threading import Lock, Event
from ...Application.Abstractions.base_task_queue_manager import BaseTaskQueueManager
from ...Application.TaskManager.job_task import JobTask
from ...Application.TaskManager.task_queue_item import TaskQueueItem

class TaskQueueManager(BaseTaskQueueManager):
    def __init__(self) -> None:
        super().__init__()
        self.__pull_queue:dict[str, TaskQueueItem] = {}
        self.__lock = Lock()
        self.__setEvent = Event()
        self.add_queue('main')

    def add_queue(self, name:str)->TaskQueueItem | None:
        try:
            if not name in self.__pull_queue:
                self.__pull_queue[name] = TaskQueueItem()
                self.__pull_queue[name].start()

            return self.__pull_queue[name]
        except Exception as ex:
            print(ex)
            return None

    def add_task(self, task: JobTask, pull_name:str)->JobTask | None:
        try:
            if pull_name in self.__pull_queue:
                self.__pull_queue[pull_name].add(task)
            else:
                raise Exception(f"Error::Task pull is empty!")

            if not self.__setEvent.is_set():
                self.__setEvent.set()

            return task
        except Exception as ex:
            print(ex)
            return None
        finally:
            if self.__lock.locked():
                self.__lock.release()