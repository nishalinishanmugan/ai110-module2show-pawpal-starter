from pawpal_system import Task, Pet


def test_task_mark_complete():
    task = Task(
        description="Walk dog",
        time_needed=30,
        frequency="Daily"
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
        frequency="Daily"
    )

    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1