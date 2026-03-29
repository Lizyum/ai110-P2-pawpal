import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from pawpal_system import Owner, Pet, Task, Priority


def make_task(owner_id: str, pet_id: str) -> Task:
    return Task(
        owner_id=owner_id,
        pet_id=pet_id,
        date=date.today(),
        priority=Priority.MEDIUM,
        task_name="Test Task",
        task_description="A task for testing.",
        duration=15,
    )


def test_mark_complete_changes_status():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    task = make_task(owner.uuid, pet.uuid)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Luna", breed="Siamese", age=5)

    assert len(pet.tasks) == 0
    pet.add_task(make_task(owner.uuid, pet.uuid))
    assert len(pet.tasks) == 1
