from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time_needed: int
    frequency: str
    completion_status: bool = False
    priority: int = 1

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completion_status = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completion_status = False

    def get_task_summary(self) -> str:
        """Return a readable summary of the task."""
        status = "Done" if self.completion_status else "Not Done"
        return (
            f"{self.description} | {self.time_needed} min | "
            f"{self.frequency} | Priority {self.priority} | {status}"
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a care task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_description: str) -> bool:
        """Remove a task by description. Returns True if removed."""
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)
                return True
        return False

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pet_summary(self) -> str:
        """Return a short summary of the pet."""
        return f"{self.name} is a {self.age}-year-old {self.species}."


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name. Returns True if removed."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                return True
        return False

    def get_all_tasks(self) -> List[tuple[str, Task]]:
        """Return all tasks from all pets as (pet_name, task) tuples."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def retrieve_all_tasks(self) -> List[tuple[str, Task]]:
        """Get all tasks from all of the owner's pets."""
        return self.owner.get_all_tasks()

    def get_incomplete_tasks(self) -> List[tuple[str, Task]]:
        """Return only incomplete tasks across all pets."""
        return [
            (pet_name, task)
            for pet_name, task in self.retrieve_all_tasks()
            if not task.completion_status
        ]

    def sort_tasks_by_time(self) -> List[tuple[str, Task]]:
        """Sort tasks by shortest time first."""
        return sorted(
            self.get_incomplete_tasks(),
            key=lambda item: item[1].time_needed
        )

    def sort_tasks_by_priority(self) -> List[tuple[str, Task]]:
        """Sort tasks by highest priority first."""
        return sorted(
            self.get_incomplete_tasks(),
            key=lambda item: item[1].priority,
            reverse=True
        )

    def create_daily_schedule(self) -> List[tuple[str, Task]]:
        """Return incomplete tasks sorted by priority then time."""
        return sorted(
            self.get_incomplete_tasks(),
            key=lambda item: (-item[1].priority, item[1].time_needed)
        )

    def get_schedule_explanation(self) -> str:
        """Explain how the schedule was organized."""
        return (
            "Tasks are included from all pets, incomplete tasks are prioritized, "
            "higher-priority tasks appear first, and shorter tasks break ties."
        )