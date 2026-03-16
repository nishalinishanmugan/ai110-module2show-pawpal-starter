from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Optional
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time_needed: int
    frequency: str
    scheduled_time: str
    due_date: date
    completion_status: bool = False
    priority: int = 1

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completion_status = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completion_status = False

    def get_next_due_date(self) -> Optional[date]:
        """Return the next due date for recurring tasks."""
        frequency_lower = self.frequency.lower()

        if frequency_lower == "daily":
            return self.due_date + timedelta(days=1)
        if frequency_lower == "weekly":
            return self.due_date + timedelta(weeks=1)

        return None

    def create_next_instance(self) -> Optional["Task"]:
        """Create the next recurring instance of this task if applicable."""
        next_due_date = self.get_next_due_date()

        if next_due_date is None:
            return None

        return Task(
            description=self.description,
            time_needed=self.time_needed,
            frequency=self.frequency,
            scheduled_time=self.scheduled_time,
            due_date=next_due_date,
            completion_status=False,
            priority=self.priority
        )

    def get_task_summary(self) -> str:
        """Return a readable summary of the task."""
        status = "Done" if self.completion_status else "Not Done"
        return (
            f"{self.description} | {self.time_needed} min | "
            f"{self.frequency} | {self.scheduled_time} | "
            f"Due: {self.due_date} | Priority {self.priority} | {status}"
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_description: str) -> bool:
        """Remove a task by description."""
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
        """Remove a pet by name."""
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

    def get_pet_by_name(self, pet_name: str) -> Optional[Pet]:
        """Return a pet by name if it exists."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
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
        """Sort incomplete tasks by shortest duration first."""
        return sorted(
            self.get_incomplete_tasks(),
            key=lambda item: item[1].time_needed
        )

    def sort_tasks_by_priority(self) -> List[tuple[str, Task]]:
        """Sort incomplete tasks by highest priority first."""
        return sorted(
            self.get_incomplete_tasks(),
            key=lambda item: item[1].priority,
            reverse=True
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completion_status: Optional[bool] = None
    ) -> List[tuple[str, Task]]:
        """Filter tasks by pet name and/or completion status."""
        tasks = self.retrieve_all_tasks()

        if pet_name is not None:
            tasks = [
                (current_pet_name, task)
                for current_pet_name, task in tasks
                if current_pet_name.lower() == pet_name.lower()
            ]

        if completion_status is not None:
            tasks = [
                (current_pet_name, task)
                for current_pet_name, task in tasks
                if task.completion_status == completion_status
            ]

        return tasks

    def create_daily_schedule(self) -> List[tuple[str, Task]]:
        """Return incomplete tasks sorted by priority then time."""
        return sorted(
            self.get_incomplete_tasks(),
            key=lambda item: (-item[1].priority, item[1].time_needed)
        )

    def mark_task_complete(self, pet_name: str, task_description: str) -> str:
        """Mark a task complete and create next recurring instance if applicable."""
        pet = self.owner.get_pet_by_name(pet_name)

        if pet is None:
            return f"Pet '{pet_name}' was not found."

        for task in pet.tasks:
            if task.description.lower() == task_description.lower() and not task.completion_status:
                task.mark_complete()

                next_task = task.create_next_instance()
                if next_task is not None:
                    pet.add_task(next_task)
                    return (
                        f"Marked '{task.description}' complete for {pet.name}. "
                        f"Created next {task.frequency.lower()} task due on {next_task.due_date}."
                    )

                return f"Marked '{task.description}' complete for {pet.name}."

        return f"Task '{task_description}' was not found for {pet.name}."

    def detect_conflicts(self) -> List[str]:
        """Return warnings for tasks with same due date and scheduled time."""
        warnings = []
        incomplete_tasks = self.get_incomplete_tasks()

        for (pet1, task1), (pet2, task2) in combinations(incomplete_tasks, 2):
            if (
                task1.due_date == task2.due_date and
                task1.scheduled_time == task2.scheduled_time
            ):
                warnings.append(
                    f"Conflict: '{task1.description}' ({pet1}) and "
                    f"'{task2.description}' ({pet2}) at {task1.scheduled_time} on {task1.due_date}"
                )

        return warnings

    def get_schedule_explanation(self) -> str:
        """Explain how the schedule was organized."""
        return (
            "Tasks are included from all pets, incomplete tasks are prioritized, "
            "higher-priority tasks appear first, and shorter tasks break ties. "
            "Recurring daily and weekly tasks create a new future instance when completed."
        )