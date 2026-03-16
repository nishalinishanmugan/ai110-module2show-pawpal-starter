classDiagram

class Owner {
    - name: str
    - time_available: int
    - preferences: list
    + update_time_available(time)
    + update_preferences(pref)
}

class Pet {
    - name: str
    - species: str
    - age: int
    - care_notes: str
    + update_info()
    + get_summary()
}

class Task {
    - title: str
    - category: str
    - duration: int
    - priority: int
    - preferred_time: str
    - notes: str
    - is_mandatory: bool
    + edit_task()
    + mark_complete()
    + get_task_details()
}

class Scheduler {
    - tasks: list
    - available_time: int
    - selected_plan: list
    - reasoning_log: list
    + generate_plan()
    + sort_tasks_by_priority()
    + filter_tasks_by_constraints()
    + explain_plan()
}

Owner "1" --> "1..*" Pet : owns
Pet "1" --> "0..*" Task : has
Scheduler "1" --> "0..*" Task : schedules
Owner "1" --> "1" Scheduler : provides constraints