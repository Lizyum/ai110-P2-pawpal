from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum
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

    def edit_task(self, **kwargs) -> None:
        """Update any task field by keyword argument, raising ValueError for unknown fields."""
        for field_name, value in kwargs.items():
            if not hasattr(self, field_name):
                raise ValueError(f"'{field_name}' is not a valid Task field.")
            setattr(self, field_name, value)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True



@dataclass
class Scheduler:
    owner_id: str
    date: date
    schedule: list[Task] = field(default_factory=list)

    def generate_day_schedule(self, owner: "Owner") -> list[Task]:
        """Return today's tasks sorted by priority descending, then duration ascending."""
        todays_tasks = [t for t in owner.tasks if t.date == self.date]
        self.schedule = sorted(todays_tasks, key=lambda t: (-t.priority, t.duration))
        return self.schedule
