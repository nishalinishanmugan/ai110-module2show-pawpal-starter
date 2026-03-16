from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(schedule: list[tuple[str, Task]], title: str) -> None:
    print(f"\n=== {title} ===\n")

    if not schedule:
        print("No tasks found.")
        return

    for index, (pet_name, task) in enumerate(schedule, start=1):
        status = "Done" if task.completion_status else "Not Done"
        print(
            f"{index}. Pet: {pet_name}\n"
            f"   Task: {task.description}\n"
            f"   Time Needed: {task.time_needed} minutes\n"
            f"   Frequency: {task.frequency}\n"
            f"   Scheduled Time: {task.scheduled_time}\n"
            f"   Due Date: {task.due_date}\n"
            f"   Priority: {task.priority}\n"
            f"   Status: {status}\n"
        )


def main() -> None:
    owner = Owner(name="Nisha")

    pet1 = Pet(name="Milo", species="Dog", age=4)
    pet2 = Pet(name="Luna", species="Cat", age=2)

    today = date.today()

    # Tasks added out of order
    task1 = Task(
        description="Morning walk",
        time_needed=30,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=today,
        priority=3
    )
    task2 = Task(
        description="Feed breakfast",
        time_needed=10,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=today,
        priority=5
    )
    task3 = Task(
        description="Brush fur",
        time_needed=15,
        frequency="Weekly",
        scheduled_time="14:00",
        due_date=today,
        priority=2
    )
    task4 = Task(
        description="Clean litter box",
        time_needed=20,
        frequency="Daily",
        scheduled_time="09:00",
        due_date=today,
        priority=4
    )

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet2.add_task(task4)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    print_schedule(scheduler.retrieve_all_tasks(), "All Tasks")
    print_schedule(scheduler.sort_tasks_by_time(), "Tasks Sorted by Time")

    print("\n=== Conflict Warnings ===\n")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")

    print("\n=== Mark Daily Task Complete ===\n")
    result = scheduler.mark_task_complete("Milo", "Morning walk")
    print(result)

    print_schedule(
        scheduler.filter_tasks(pet_name="Milo"),
        "Milo's Tasks After Completing Morning Walk"
    )

    print_schedule(scheduler.create_daily_schedule(), "Today's Schedule")

    print("Schedule Explanation:")
    print(scheduler.get_schedule_explanation())


if __name__ == "__main__":
    main()