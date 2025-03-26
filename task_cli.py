import time
import sys
import json
import os

class TaskManager():
    def __init__(self):
        self.tasks = []
        self.task_statuses = {"todo": [], "in-progress": [], "done": []}
        self.next_id = 0

    def add_task(self, description):
        task = Task(self.next_id, description, 'todo')
        self.tasks.append(task)
        self.task_statuses['todo'].append(task)
        self.next_id += 1

    def update_task(self, id, description):
        for task in self.tasks:
            if task.id == id:
                task.description = description
                task.updatedAt = time.time()
                print(f'Task updated successfully(ID: {task.id})')

    def delete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                self.tasks.remove(task)
                self.task_statuses[task.status].remove(task)
                print(f'Task deleted successfully(ID: {task.id})')

    def change_status(self, id, status):
        for task in self.tasks:
            if task.id == id:
                self.task_statuses[task.status].remove(task)
                task.status = status
                self.task_statuses[status].append(task)
                task.updatedAt = time.time()
                print(f'Task status changed successfully(ID: {task.id})')

    def save(self):
        with open('tasks.json', 'w') as f:
            tasks = []
            for task in self.tasks:
                tasks.append(task.__dict__)
            json.dump(tasks, f, indent=4)

    def load(self):
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            for task in tasks:
                new_task = Task(task['id'], task['description'], task['status'])
                new_task.createdAt = task['createdAt']
                new_task.updatedAt = task['updatedAt']
                self.tasks.append(new_task)
                self.task_statuses[new_task.status].append(new_task)
            self.next_id = self.tasks[-1].id + 1

class Task():
    def __init__(self, id, description, status):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = time.time()
        self.updatedAt = time.time()

def main():
    args = sys.argv
    task_manager = TaskManager()

    if os.path.exists('tasks.json'):
        task_manager.load()

    if args[1] == 'add':
        if len(args) < 3:
            print("Please provide a task description.")
            return
        task_manager.add_task(args[2])
        task_manager.save()
        print(f'Task added successfully(ID: {task_manager.tasks[-1].id})')

    if args[1] == 'list':
        if len(args) >= 3:
            if args[2] == 'done':
                for task in task_manager.task_statuses["done"]:
                    print(f'{task.id} - {task.description} - {task.status}')
            elif args[2] == 'todo':
                for task in task_manager.task_statuses["todo"]:
                    print(f'{task.id} - {task.description} - {task.status}')
            elif args[2] == 'in-progress':
                for task in task_manager.task_statuses["in-progress"]:
                    print(f'{task.id} - {task.description} - {task.status}')
            else:
                print("Unknown status. Use: todo, done, or in-progress.")
        else:
            for task in task_manager.tasks:
                print(f'{task.id} - {task.description} - {task.status}')


    if args[1] == 'update':
        if len(args) < 4:
            print("Usage: update <id> <new description>")
            return
        task_id = int(args[2])
        description = args[3]
        task_manager.update_task(task_id, description)
        task_manager.save()

    if args[1] == 'delete':
        if len(args) < 3:
            print("Please provide the task ID to delete.")
            return
        task_id = int(args[2])
        task_manager.delete_task(task_id)
        task_manager.save()
        
    if args[1] == 'mark-in-progress':
        if len(args) < 3:
            print("Please provide the task ID to mark as in-progress.")
            return
        task_id = int(args[2])
        task_manager.change_status(task_id, 'in-progress')
        task_manager.save()

    if args[1] == 'mark-done':
        if len(args) < 3:
            print("Please provide the task ID to mark as done.")
            return
        task_id = int(args[2])
        task_manager.change_status(task_id, 'done')
        task_manager.save()

if __name__ == "__main__":
    main()

