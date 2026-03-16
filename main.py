from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(schedule: list[tuple[str, Task]]) -> None:
    print("\n=== Today's Schedule ===\n")

    if not schedule:
        print("No tasks scheduled for today.")
        return

    for index, (pet_name, task) in enumerate(schedule, start=1):
        status = "Done" if task.completion_status else "Not Done"
        print(
            f"{index}. Pet: {pet_name}\n"
            f"   Task: {task.description}\n"
            f"   Time Needed: {task.time_needed} minutes\n"
            f"   Frequency: {task.frequency}\n"
            f"   Priority: {task.priority}\n"
            f"   Status: {status}\n"
        )


def main() -> None:
    # Create owner
    owner = Owner(name="Nisha")

    # Create pets
    pet1 = Pet(name="Milo", species="Dog", age=4)
    pet2 = Pet(name="Luna", species="Cat", age=2)

    # Create tasks
    task1 = Task(
        description="Morning walk",
        time_needed=30,
        frequency="Daily",
        priority=3
    )
    task2 = Task(
        description="Feed breakfast",
        time_needed=10,
        frequency="Daily",
        priority=5
    )
    task3 = Task(
        description="Brush fur",
        time_needed=15,
        frequency="Weekly",
        priority=2
    )
    task4 = Task(
        description="Clean litter box",
        time_needed=20,
        frequency="Daily",
        priority=4
    )

    # Add tasks to pets
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet2.add_task(task4)

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Generate schedule
    today_schedule = scheduler.create_daily_schedule()

    # Print schedule
    print_schedule(today_schedule)

    # Print explanation
    print("Schedule Explanation:")
    print(scheduler.get_schedule_explanation())


if __name__ == "__main__":
    main()