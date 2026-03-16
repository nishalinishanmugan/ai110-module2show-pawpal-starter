classDiagram

class Owner {
    - name: str
    - pets: List[Pet]
    + add_pet(pet)
    + remove_pet(pet_name)
    + get_all_tasks()
    + get_pet_by_name(pet_name)
}

class Pet {
    - name: str
    - species: str
    - age: int
    - tasks: List[Task]
    + add_task(task)
    + remove_task(task_description)
    + get_tasks()
    + get_pet_summary()
}

class Task {
    - description: str
    - time_needed: int
    - frequency: str
    - scheduled_time: str
    - due_date: date
    - completion_status: bool
    - priority: int
    + mark_complete()
    + mark_incomplete()
    + get_next_due_date()
    + create_next_instance()
    + get_task_summary()
}

class Scheduler {
    - owner: Owner
    + retrieve_all_tasks()
    + get_incomplete_tasks()
    + sort_tasks_by_time()
    + sort_tasks_by_priority()
    + filter_tasks(pet_name, completion_status)
    + create_daily_schedule()
    + mark_task_complete(pet_name, task_description)
    + detect_conflicts()
    + get_schedule_explanation()
}

Owner "1" --> "0..*" Pet : owns
Pet "1" --> "0..*" Task : has
Scheduler "1" --> "1" Owner : uses
Scheduler ..> Task : sorts / filters
Scheduler ..> Pet : checks tasks