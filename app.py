import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

st.markdown("### Pets")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_pet_breed = st.text_input("Breed / Species", value="Siamese")

if st.button("Add Pet"):
    new_pet = Pet(owner_id=st.session_state.owner.uuid, name=new_pet_name, breed=new_pet_breed, age=0)
    st.session_state.owner.add_pet(new_pet)

if st.session_state.owner.pets:
    st.table([{"Name": p.name, "Breed": p.breed} for p in st.session_state.owner.pets])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if not st.session_state.owner.pets:
    st.info("Add at least one pet above before adding tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        pet_options = {p.name: p for p in st.session_state.owner.pets}
        selected_pet_name = st.selectbox("Pet", list(pet_options.keys()))
        selected_pet = pet_options[selected_pet_name]

    if st.button("Add task"):
        task = Task(
            owner_id=st.session_state.owner.uuid,
            pet_id=selected_pet.uuid,
            date=date.today(),
            priority=Priority[priority.upper()],
            task_name=task_title,
            task_description="",
            duration=int(duration),
        )
        selected_pet.add_task(task)

all_tasks = st.session_state.owner.tasks
pet_lookup = {p.uuid: p.name for p in st.session_state.owner.pets}
pet_obj_lookup = {p.uuid: p for p in st.session_state.owner.pets}
if all_tasks:
    st.write("Current tasks:")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
    col1.markdown("**Pet**")
    col2.markdown("**Task**")
    col3.markdown("**Priority**")
    col4.markdown("**Duration**")
    col5.markdown("**Action**")
    st.divider()
    for t in all_tasks:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
        col1.write(pet_lookup.get(t.pet_id, "Unknown"))
        col2.write(t.task_name)
        col3.write(t.priority.name)
        col4.write(f"{t.duration} min")
        if col5.button("Remove", key=t.id):
            pet_obj_lookup[t.pet_id].remove_task(t.id)
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not st.session_state.owner.tasks:
        st.warning("Add tasks before generating a schedule.")
    else:
        scheduler = Scheduler(owner_id=st.session_state.owner.uuid, date=date.today())
        schedule = scheduler.generate_day_schedule(st.session_state.owner)
        st.success(f"Schedule generated for {date.today()}!")
        st.table([
            {
                "Order": i + 1,
                "Pet": pet_lookup.get(t.pet_id, "Unknown"),
                "Task": t.task_name,
                "Priority": t.priority.name,
                "Duration (min)": t.duration,
            }
            for i, t in enumerate(schedule)
        ])
