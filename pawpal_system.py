from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import uuid


@dataclass
class Owner:
    name: str
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))

    def create_profile(self) -> "Owner":
        pass


@dataclass
class Pet:
    owner_id: str
    name: str
    breed: str
    age: int
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    medication_id: Optional[str] = None

    def create_pet_profile(self) -> "Pet":
        pass


@dataclass
class Task:
    owner_id: str
    pet_id: str
    date: date
    priority: int
    task_name: str
    task_description: str
    duration: int  # in minutes
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False

    def add_task(self) -> None:
        pass

    def remove_task(self) -> None:
        pass

    def edit_task(self, **_kwargs) -> None:  # noqa: unused-param
        pass


@dataclass
class Scheduler:
    date: date
    schedule: list[Task] = field(default_factory=list)

    def generate_day_schedule(self, _tasks: list[Task]) -> list[Task]:  # noqa: unused-param
        pass
