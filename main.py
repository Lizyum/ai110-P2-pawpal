from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, Priority

# --- Setup ---
owner = Owner(name="Jane")

buddy = Pet(owner_id=owner.uuid, name="Buddy", breed="Labrador", age=3)
luna  = Pet(owner_id=owner.uuid, name="Luna",  breed="Siamese",  age=5)

owner.add_pet(buddy)
owner.add_pet(luna)

today = date.today()

# --- Tasks ---
buddy.add_task(Task(
    owner_id=owner.uuid,
    pet_id=buddy.uuid,
    date=today,
    priority=Priority.HIGH,
    task_name="Morning Walk",
    task_description="30 minute walk around the block.",
    duration=30,
))

buddy.add_task(Task(
    owner_id=owner.uuid,
    pet_id=buddy.uuid,
    date=today,
    priority=Priority.CRITICAL,
    task_name="Vet Appointment",
    task_description="Annual checkup at 10am.",
    duration=60,
))

luna.add_task(Task(
    owner_id=owner.uuid,
    pet_id=luna.uuid,
    date=today,
    priority=Priority.MEDIUM,
    task_name="Administer Medication",
    task_description="Give Luna her daily allergy medication.",
    duration=5,
))

# --- Schedule ---
scheduler = Scheduler(owner_id=owner.uuid, date=today)
schedule = scheduler.generate_day_schedule(owner)

print(f"\n📋 Today's Schedule for {owner.name} — {today}\n")
print(f"{'#':<4} {'Task':<25} {'Pet':<10} {'Priority':<10} {'Duration'}")
print("-" * 65)

pet_lookup = {p.uuid: p.name for p in owner.pets}

for i, task in enumerate(schedule, start=1):
    pet_name = pet_lookup.get(task.pet_id, "Unknown")
    print(f"{i:<4} {task.task_name:<25} {pet_name:<10} {task.priority.name:<10} {task.duration} min")

print()
