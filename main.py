import csv
from pathlib import Path


TODO_FILE = Path("todos.csv")
tasks = []


def add_one_task(title):
    title = title.strip()
    if not title:
        print("Task title cannot be empty.")
        return False

    tasks.append(title)
    print(f'Added task: "{title}"')
    return True


def print_list():
    if not tasks:
        print("No tasks yet.")
        return

    print("Todo List:")
    for position, title in enumerate(tasks, start=1):
        print(f"{position}. {title}")


def delete_task(number_to_delete):
    try:
        position = int(number_to_delete)
    except ValueError:
        print("Please enter a valid task number.")
        return False

    if position < 1 or position > len(tasks):
        print("Task number not found.")
        return False

    removed_task = tasks.pop(position - 1)
    print(f'Deleted task: "{removed_task}"')
    return True


def save_todos():
    with TODO_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for title in tasks:
            writer.writerow([title])


def load_todos():
    tasks.clear()

    if not TODO_FILE.exists():
        return

    with TODO_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row and row[0].strip():
                tasks.append(row[0].strip())


def print_menu():
    print()
    print("Choose an option:")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Delete task")
    print("4. Save and quit")


def main():
    load_todos()
    print("Todo List CLI")

    while True:
        print_menu()
        choice = input("> ").strip()

        if choice == "1":
            title = input("Task title: ")
            add_one_task(title)
        elif choice == "2":
            print_list()
        elif choice == "3":
            print_list()
            if tasks:
                number_to_delete = input("Task number to delete: ")
                delete_task(number_to_delete)
        elif choice == "4":
            save_todos()
            print("Todos saved. Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()

