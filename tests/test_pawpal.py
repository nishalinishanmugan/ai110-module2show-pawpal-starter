from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_mark_complete():
    task = Task(
        description="Walk dog",
        time_needed=30,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=date.today()
    )

    assert task.completion_status is False

    task.mark_complete()

    assert task.completion_status is True


def test_pet_add_task():
    pet = Pet(
        name="Milo",
        species="Dog",
        age=4
    )

    task = Task(
        description="Feed",
        time_needed=10,
        frequency="Daily",
        scheduled_time="09:00",
        due_date=date.today()
    )

    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_sort_tasks_by_time():
    owner = Owner(name="Nisha")
    pet = Pet(name="Milo", species="Dog", age=4)

    task1 = Task(
        description="Long walk",
        time_needed=30,
        frequency="Daily",
        scheduled_time="10:00",
        due_date=date.today()
    )
    task2 = Task(
        description="Quick feeding",
        time_needed=10,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=date.today()
    )
    task3 = Task(
        description="Brush fur",
        time_needed=15,
        frequency="Weekly",
        scheduled_time="09:00",
        due_date=date.today()
    )

    # Add out of order on purpose
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time()

    assert sorted_tasks[0][1].description == "Quick feeding"
    assert sorted_tasks[1][1].description == "Brush fur"
    assert sorted_tasks[2][1].description == "Long walk"


def test_daily_task_completion_creates_next_day_task():
    owner = Owner(name="Nisha")
    pet = Pet(name="Milo", species="Dog", age=4)

    today = date.today()
    daily_task = Task(
        description="Morning walk",
        time_needed=30,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=today
    )

    pet.add_task(daily_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Milo", "Morning walk")

    assert "Created next daily task" in result
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completion_status is True
    assert pet.tasks[1].description == "Morning walk"
    assert pet.tasks[1].completion_status is False
    assert pet.tasks[1].due_date == today + timedelta(days=1)


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(name="Nisha")
    pet1 = Pet(name="Milo", species="Dog", age=4)
    pet2 = Pet(name="Luna", species="Cat", age=2)

    today = date.today()

    task1 = Task(
        description="Morning walk",
        time_needed=30,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=today
    )
    task2 = Task(
        description="Feed breakfast",
        time_needed=10,
        frequency="Daily",
        scheduled_time="08:00",
        due_date=today
    )

    pet1.add_task(task1)
    pet2.add_task(task2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Conflict" in conflicts[0]
    assert "08:00" in conflicts[0]