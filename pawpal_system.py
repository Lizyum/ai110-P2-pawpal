from dataclasses import dataclass, field
from datetime import date, time, timedelta
from enum import IntEnum
from typing import Optional
import uuid



class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Owner:
    name: str
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    @property
    def tasks(self) -> list["Task"]:
        """Return all tasks across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_tasks_by_pet(self, pet_id: str) -> list["Task"]:
        """Return all tasks for a specific pet by ID."""
        return [t for t in self.tasks if t.pet_id == pet_id]

    def get_tasks_by_status(self, completed: bool) -> list["Task"]:
        """Return all tasks matching the given completion status."""
        return [t for t in self.tasks if t.completed == completed]


@dataclass
class Pet:
    owner_id: str
    name: str
    breed: str
    age: int
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    medication_ids: list[str] = field(default_factory=list)
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by ID, raising ValueError if not found."""
        match = next((t for t in self.tasks if t.id == task_id), None)
        if match is None:
            raise ValueError(f"Task '{task_id}' not found.")
        self.tasks.remove(match)

    def birthday(self) -> None:
        """Increment the pet's age by one year."""
        self.age += 1

    def update_medication(self, medication_id: str) -> None:
        """Add a medication ID to the pet's medication list if not already present."""
        if medication_id not in self.medication_ids:
            self.medication_ids.append(medication_id)



@dataclass
class Task:
    owner_id: str
    pet_id: str
    date: date
    priority: Priority
    task_name: str
    task_description: str
    duration: int  # in minutes
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False
    start_time: Optional[time] = None
    recurrence: Optional[str] = None  # "daily" or "weekly"

    def edit_task(self, **kwargs) -> None:
        """Update any task field by keyword argument, raising ValueError for unknown fields."""
        for field_name, value in kwargs.items():
            if not hasattr(self, field_name):
                raise ValueError(f"'{field_name}' is not a valid Task field.")
            setattr(self, field_name, value)

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task instance for the next recurrence, or None if not recurring."""
        if self.recurrence == "daily":
            delta = timedelta(days=1)
        elif self.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        return Task(
            owner_id=self.owner_id,
            pet_id=self.pet_id,
            date=self.date + delta,
            priority=self.priority,
            task_name=self.task_name,
            task_description=self.task_description,
            duration=self.duration,
            start_time=self.start_time,
            recurrence=self.recurrence,
        )

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next occurrence if recurring, else None."""
        self.completed = True
        return self.next_occurrence()



@dataclass
class Scheduler:
    owner_id: str
    date: date
    schedule: list[Task] = field(default_factory=list)

    def generate_day_schedule(self, owner: "Owner") -> list[Task]:
        """Return today's tasks: fixed-time tasks anchored first by start_time, then flexible tasks by priority and duration."""
        todays_tasks = [t for t in owner.tasks if t.date == self.date]
        fixed = sorted([t for t in todays_tasks if t.start_time is not None], key=lambda t: t.start_time)
        flexible = sorted([t for t in todays_tasks if t.start_time is None], key=lambda t: (-t.priority, t.duration))
        self.schedule = fixed + flexible
        return self.schedule

    def detect_conflicts(self, pet_lookup: dict[str, str]) -> list[str]:
        """Return a list of warning messages for any overlapping fixed-time tasks."""
        fixed = [t for t in self.schedule if t.start_time is not None]
        warnings = []
        for i, a in enumerate(fixed):
            for b in fixed[i + 1:]:
                a_start = a.start_time.hour * 60 + a.start_time.minute
                a_end = a_start + a.duration
                b_start = b.start_time.hour * 60 + b.start_time.minute
                b_end = b_start + b.duration
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"⚠️ Conflict: '{a.task_name}' ({pet_lookup.get(a.pet_id, 'Unknown')}) "
                        f"overlaps with '{b.task_name}' ({pet_lookup.get(b.pet_id, 'Unknown')})"
                    )
        return warnings
