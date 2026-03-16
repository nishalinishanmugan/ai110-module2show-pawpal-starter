import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Keep the Owner object alive across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Default Owner")

owner = st.session_state.owner

st.title("🐾 PawPal+")
st.markdown("Plan pet care tasks, add pets, and generate a daily schedule.")

st.divider()

# Owner section
st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value=owner.name)

if st.button("Update Owner Name"):
    owner.name = owner_name.strip() if owner_name.strip() else owner.name
    st.success("Owner name updated.")

st.divider()

# Add pet section
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name")
pet_species = st.selectbox("Species", ["Dog", "Cat", "Other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    if pet_name.strip():
        new_pet = Pet(
            name=pet_name.strip(),
            species=pet_species,
            age=int(pet_age)
        )
        owner.add_pet(new_pet)
        st.success(f"{pet_name} added successfully.")
    else:
        st.error("Please enter a pet name.")

st.divider()

# Show current pets
st.subheader("Current Pets")
selected_pet = None

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)

    for pet in owner.pets:
        if pet.name == selected_pet_name:
            selected_pet = pet
            break

    st.write(
        f"Selected Pet: **{selected_pet.name}** "
        f"({selected_pet.species}, age {selected_pet.age})"
    )
else:
    st.info("No pets added yet.")

st.divider()

# Add task section
st.subheader("Add a Task")
task_description = st.text_input("Task description", value="Morning walk")
task_time = st.number_input("Time needed (minutes)", min_value=1, max_value=240, value=20)
task_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "As needed"])
task_priority = st.number_input("Priority", min_value=1, max_value=5, value=3)

if st.button("Add Task"):
    if selected_pet is None:
        st.error("Please add and select a pet first.")
    elif task_description.strip():
        new_task = Task(
            description=task_description.strip(),
            time_needed=int(task_time),
            frequency=task_frequency,
            priority=int(task_priority)
        )
        selected_pet.add_task(new_task)
        st.success(f"Task added to {selected_pet.name}.")
    else:
        st.error("Please enter a task description.")

st.divider()

# Show tasks
st.subheader("Current Tasks")
if owner.pets:
    has_tasks = False
    for pet in owner.pets:
        if pet.tasks:
            has_tasks = True
            st.markdown(f"### {pet.name}'s Tasks")
            for task in pet.tasks:
                status = "Done" if task.completion_status else "Not Done"
                st.write(
                    f"- **{task.description}** | {task.time_needed} min | "
                    f"{task.frequency} | Priority {task.priority} | {status}"
                )
    if not has_tasks:
        st.info("No tasks added yet.")
else:
    st.info("No pets available yet.")

st.divider()

# Schedule section
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.create_daily_schedule()

    if schedule:
        st.success("Daily schedule generated.")
        st.markdown("## Today's Schedule")

        for index, (pet_name, task) in enumerate(schedule, start=1):
            status = "Done" if task.completion_status else "Not Done"
            st.write(
                f"{index}. **{pet_name}** — {task.description} "
                f"({task.time_needed} min, {task.frequency}, "
                f"Priority {task.priority}, {status})"
            )

        st.markdown("### Why this plan was chosen")
        st.write(scheduler.get_schedule_explanation())
    else:
        st.warning("No incomplete tasks available to schedule.")
