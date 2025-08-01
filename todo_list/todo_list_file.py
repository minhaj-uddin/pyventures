import os
import json

FILE = "tasks.json"


def print_menu():
    print('\nTodo List Menu:')
    print('1. View Tasks')
    print('2. Add a Task')
    print('3. Remove a Task')
    print('4. Complete Task')
    print('5. Exit')


def get_choice():
    while True:
        choice = input('Enter your choice: ')
        if choice not in ('1', '2', '3', '4', '5'):
            print('Invalid choice')
        else:
            return choice


def display_tasks(tasks):
    if not tasks:
        print('No tasks in the list.')
        return

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task['completed'] else "✗"
        print(f"{index}. [{status}] {task['description']}")


def add_task(tasks):
    task = input('Enter a new task: ').strip()
    if task:
        tasks.append({'description': task, 'completed': False})
    else:
        print('Invalid task!')


def remove_task(tasks):
    display_tasks(tasks)
    if not tasks:
        return

    try:
        task_number = int(input('Enter the task number to remove: '))
        if 1 <= task_number <= len(tasks):
            tasks.pop(task_number - 1)
        else:
            print('Invalid task number')
    except ValueError:
        print('Invalid input')


def complete_task(tasks):
    display_tasks(tasks)
    if not tasks:
        return

    try:
        task_number = int(
            input('Enter the task number to mark as completed: '))
        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1]['completed'] = True
        else:
            print('Invalid task number')
    except ValueError:
        print('Invalid input')


def save_tasks(tasks):
    with open(FILE, 'w') as f:
        json.dump(tasks, f, indent=4)


def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, 'r') as f:
        return json.load(f)


def main():
    tasks = load_tasks()

    while True:
        print_menu()
        choice = get_choice()

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            complete_task(tasks)
        else:
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break


if __name__ == '__main__':
    main()
