class ToDo:
    def __init__(self):
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)
        return self._tasks

    def remove_task(self, task):
        self._tasks.remove(task)
        return self._tasks

    def list_tasks(self):
        return self._tasks

    def get_by_index(self, index):
        return self._tasks[index]

    def to_dict(self):
        result = {}
        count = 1
        for task in self._tasks:
            result[str(count)] = task
            count += 1
        return result
