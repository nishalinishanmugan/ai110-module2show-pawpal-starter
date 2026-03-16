from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def priority_badge(priority: str) -> str:
    """Return an emoji label for task priority."""
    if priority == "High":
        return "🔴 High"
    if priority == "Medium":
        return "🟡 Medium"
    return "🟢 Low"


def status_badge(task: Task) -> str:
    """Return a readable status label."""
    return "✅ Done" if task.completion_status else "⏳ Pending"


def print_schedule(schedule: list[tuple[str, Task]], title: str) -> None:
    """Print a formatted schedule to the terminal."""
    print(f"\n=== {title} ===\n")

    if not schedule:
        print("No tasks found.")
        return

    for index, (pet_name, task) in enumerate(schedule, start=1):
        print(
            f"{index}. Pet: {pet_name}\n"
            f"   Task: {task.description}\n"
            f"   Time Needed: {task.time_needed} minutes\n"
            f"   Frequency: {task.frequency}\n"
            f"   Scheduled Time: {task.scheduled_time}\n"
            f"   Due Date: {task.due_date}\n"
            f"   Priority: {priority_badge(task.priority)}\n"
            f"   Status: {status_badge(task)}\n"
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
        priority="High"
    )
    task2 = Task(
        description="Feed breakfast",
        time_needed=10,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=today,
        priority="High"
    )
    task3 = Task(
        description="Brush fur",
        time_needed=15,
        frequency="Weekly",
        scheduled_time="14:00",
        due_date=today,
        priority="Medium"
    )
    task4 = Task(
        description="Clean litter box",
        time_needed=20,
        frequency="Daily",
        scheduled_time="09:00",
        due_date=today,
        priority="High"
    )
    task5 = Task(
        description="Play session",
        time_needed=25,
        frequency="As needed",
        scheduled_time="18:00",
        due_date=today,
        priority="Low"
    )

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet2.add_task(task4)
    pet2.add_task(task5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    print_schedule(scheduler.retrieve_all_tasks(), "All Tasks")
    print_schedule(scheduler.sort_tasks_by_time(), "Tasks Sorted by Time")
    print_schedule(scheduler.sort_tasks_by_priority(), "Tasks Sorted by Priority")
    print_schedule(scheduler.create_daily_schedule(), "Standard Priority Schedule")
    print_schedule(scheduler.create_weighted_schedule(), "Weighted Smart Schedule")

    print("\n=== Conflict Warnings ===\n")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"⚠️ {warning}")
    else:
        print("No conflicts detected.")

    print("\n=== Mark Daily Task Complete ===\n")
    result = scheduler.mark_task_complete("Milo", "Morning walk")
    print(result)

    print_schedule(
        scheduler.filter_tasks(pet_name="Milo"),
        "Milo's Tasks After Completing Morning Walk"
    )

    print("\nSchedule Explanation:")
    print(scheduler.get_schedule_explanation())

    print("\nWeighted Schedule Explanation:")
    print(scheduler.get_weighted_schedule_explanation())


if __name__ == "__main__":
    main()