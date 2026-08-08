import random

class TaskTracker:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, notification_days = [], *kwargs): # <- notification_days = [], *kwargs
        if notification_days == []:
            #set default
            notification_days.append("Monday")

        description = kwargs.get('description', 'Без описания')
        priority = kwargs.get('priority', 1)
        task = {'name': name,
                'desc': description,
                'priority': priority,
                'done': False,
                "id": random.randint(0,100000), # <- "id": random.randint(0,100000)
                'notification_day': notification_days}
        self.tasks.append(task)
        return task['id']

    def remove_low_priority(self, threshold=2):
        for task in self.tasks:
            if task['priority'] < threshold:
                self.tasks.remove(task)  # <- remove in iteration
        return len(self.tasks)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task['id'] is task_id: # <- is instead of ==
                task['done'] = True
                return True
        return False