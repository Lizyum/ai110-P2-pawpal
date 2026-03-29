import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, time, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, Priority


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
    result = task.mark_complete()
    assert task.completed is True
    assert result is None  # non-recurring task returns no next occurrence


def test_mark_complete_daily_returns_next_occurrence():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    today = date.today()
    task = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=today,
                priority=Priority.MEDIUM, task_name="Medication", task_description="",
                duration=5, recurrence="daily")

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.date == today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.recurrence == "daily"


def test_mark_complete_weekly_returns_next_occurrence():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    today = date.today()
    task = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=today,
                priority=Priority.LOW, task_name="Grooming", task_description="",
                duration=60, recurrence="weekly")

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.date == today + timedelta(weeks=1)
    assert next_task.recurrence == "weekly"


def test_add_task_increases_pet_task_count():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Luna", breed="Siamese", age=5)

    assert len(pet.tasks) == 0
    pet.add_task(make_task(owner.uuid, pet.uuid))
    assert len(pet.tasks) == 1


def test_schedule_fixed_time_tasks_appear_before_flexible():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    owner.add_pet(pet)

    flexible = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
                    priority=Priority.HIGH, task_name="Walk", task_description="", duration=30)
    fixed = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
                 priority=Priority.LOW, task_name="Vet", task_description="", duration=60,
                 start_time=time(10, 0))

    pet.add_task(flexible)
    pet.add_task(fixed)

    schedule = Scheduler(owner_id=owner.uuid, date=date.today()).generate_day_schedule(owner)

    assert schedule[0].task_name == "Vet"
    assert schedule[1].task_name == "Walk"


def test_schedule_fixed_tasks_ordered_by_start_time():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    owner.add_pet(pet)

    late = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
                priority=Priority.LOW, task_name="Grooming", task_description="", duration=45,
                start_time=time(14, 0))
    early = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
                 priority=Priority.LOW, task_name="Vet", task_description="", duration=60,
                 start_time=time(9, 0))

    pet.add_task(late)
    pet.add_task(early)

    schedule = Scheduler(owner_id=owner.uuid, date=date.today()).generate_day_schedule(owner)

    assert schedule[0].task_name == "Vet"
    assert schedule[1].task_name == "Grooming"


def test_filter_tasks_by_pet():
    owner = Owner(name="Jane")
    buddy = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    luna = Pet(owner_id=owner.uuid, name="Luna", breed="Siamese", age=5)
    owner.add_pet(buddy)
    owner.add_pet(luna)

    buddy.add_task(make_task(owner.uuid, buddy.uuid))
    luna.add_task(make_task(owner.uuid, luna.uuid))

    assert len(owner.get_tasks_by_pet(buddy.uuid)) == 1
    assert owner.get_tasks_by_pet(buddy.uuid)[0].pet_id == buddy.uuid


def test_filter_tasks_by_status():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    owner.add_pet(pet)

    t1 = make_task(owner.uuid, pet.uuid)
    t2 = make_task(owner.uuid, pet.uuid)
    t1.mark_complete()
    pet.add_task(t1)
    pet.add_task(t2)

    assert len(owner.get_tasks_by_status(completed=True)) == 1
    assert len(owner.get_tasks_by_status(completed=False)) == 1


def test_detect_conflicts_same_start_time():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    owner.add_pet(pet)

    t1 = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
              priority=Priority.HIGH, task_name="Vet", task_description="",
              duration=60, start_time=time(10, 0))
    t2 = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
              priority=Priority.MEDIUM, task_name="Grooming", task_description="",
              duration=30, start_time=time(10, 0))

    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = Scheduler(owner_id=owner.uuid, date=date.today())
    scheduler.generate_day_schedule(owner)

    pet_lookup = {pet.uuid: pet.name}
    conflicts = scheduler.detect_conflicts(pet_lookup)

    assert len(conflicts) == 1
    assert "Vet" in conflicts[0]
    assert "Grooming" in conflicts[0]


def test_no_conflicts_non_overlapping_tasks():
    owner = Owner(name="Jane")
    pet = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
    owner.add_pet(pet)

    t1 = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
              priority=Priority.HIGH, task_name="Vet", task_description="",
              duration=30, start_time=time(9, 0))
    t2 = Task(owner_id=owner.uuid, pet_id=pet.uuid, date=date.today(),
              priority=Priority.MEDIUM, task_name="Grooming", task_description="",
              duration=30, start_time=time(10, 0))

    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = Scheduler(owner_id=owner.uuid, date=date.today())
    scheduler.generate_day_schedule(owner)

    pet_lookup = {pet.uuid: pet.name}
    conflicts = scheduler.detect_conflicts(pet_lookup)

    assert len(conflicts) == 0
