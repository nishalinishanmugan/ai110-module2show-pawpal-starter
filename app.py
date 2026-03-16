import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def priority_badge(priority: str) -> str:
    if priority == "High":
        return "🔴 High"
    if priority == "Medium":
        return "🟡 Medium"
    return "🟢 Low"


def task_type_emoji(task: Task) -> str:
    description = task.description.lower()

    if "walk" in description:
        return "🚶"
    if "feed" in description or "food" in description:
        return "🍽️"
    if "med" in description or "medicine" in description:
        return "💊"
    if "groom" in description or "brush" in description:
        return "🧼"
    if "play" in description or "enrichment" in description:
        return "🎾"
    if "litter" in description:
        return "🧹"
    return "🐾"


def status_badge(task: Task) -> str:
    return "✅ Done" if task.completion_status else "⏳ Pending"


def priority_value(priority: str) -> int:
    mapping = {"Low": 1, "Medium": 2, "High": 3}
    return mapping.get(priority, 2)


def tasks_to_rows(task_tuples: list[tuple[str, Task]]) -> list[dict]:
    rows = []
    for pet_name, task in task_tuples:
        rows.append(
            {
                "Pet": pet_name,
                "Type": task_type_emoji(task),
                "Task": task.description,
                "Duration (min)": task.time_needed,
                "Frequency": task.frequency,
                "Scheduled Time": task.scheduled_time,
                "Due Date": str(task.due_date),
                "Priority": priority_badge(task.priority),
                "Status": status_badge(task),
            }
        )
    return rows


if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Default Owner")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.markdown(
    "Plan pet care tasks, organize priorities, detect conflicts, and generate a smarter daily schedule."
)

st.divider()

st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value=owner.name)

if st.button("Update Owner Name"):
    owner.name = owner_name.strip() if owner_name.strip() else owner.name
    st.success("Owner name updated.")

st.divider()

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
        st.success(f"{pet_name.strip()} added successfully.")
    else:
        st.error("Please enter a pet name.")

st.divider()

st.subheader("Current Pets")
selected_pet = None

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)

    for pet in owner.pets:
        if pet.name == selected_pet_name:
            selected_pet = pet
            break

    st.success(
        f"Selected Pet: {selected_pet.name} ({selected_pet.species}, age {selected_pet.age})"
    )
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
task_description = st.text_input("Task description", value="Morning walk")
task_time_needed = st.number_input("Time needed (minutes)", min_value=1, max_value=240, value=20)
task_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "As needed"])
task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
task_scheduled_time = st.text_input("Scheduled time (HH:MM)", value="08:00")
task_due_date = st.date_input("Due date", value=date.today())

if st.button("Add Task"):
    if selected_pet is None:
        st.error("Please add and select a pet first.")
    elif task_description.strip():
        new_task = Task(
            description=task_description.strip(),
            time_needed=int(task_time_needed),
            frequency=task_frequency,
            scheduled_time=task_scheduled_time.strip(),
            due_date=task_due_date,
            priority=task_priority
        )
        selected_pet.add_task(new_task)
        st.success(f"Task added to {selected_pet.name}.")
    else:
        st.error("Please enter a task description.")

st.divider()

st.subheader("Current Tasks")
all_tasks = scheduler.retrieve_all_tasks()

if all_tasks:
    st.table(tasks_to_rows(all_tasks))
else:
    st.info("No tasks added yet.")

st.divider()

st.subheader("View Smarter Task Lists")

filter_pet_name = st.selectbox(
    "Filter by pet",
    ["All Pets"] + [pet.name for pet in owner.pets] if owner.pets else ["All Pets"]
)

filter_status = st.selectbox(
    "Filter by status",
    ["All", "Incomplete", "Completed"]
)

sort_option = st.selectbox(
    "Sort tasks by",
    ["Priority", "Time Needed", "Weighted Smart Order"]
)

filtered_tasks = scheduler.retrieve_all_tasks()

if filter_pet_name != "All Pets":
    filtered_tasks = [
        (pet_name, task)
        for pet_name, task in filtered_tasks
        if pet_name == filter_pet_name
    ]

if filter_status == "Incomplete":
    filtered_tasks = [
        (pet_name, task)
        for pet_name, task in filtered_tasks
        if not task.completion_status
    ]
elif filter_status == "Completed":
    filtered_tasks = [
        (pet_name, task)
        for pet_name, task in filtered_tasks
        if task.completion_status
    ]

if sort_option == "Priority":
    filtered_tasks = sorted(
        filtered_tasks,
        key=lambda item: (-priority_value(item[1].priority), item[1].time_needed)
    )
elif sort_option == "Time Needed":
    filtered_tasks = sorted(
        filtered_tasks,
        key=lambda item: item[1].time_needed
    )
else:
    filtered_tasks = sorted(
        filtered_tasks,
        key=lambda item: scheduler.calculate_task_weight(item[1]),
        reverse=True
    )

if filtered_tasks:
    st.table(tasks_to_rows(filtered_tasks))
else:
    st.info("No tasks match the current filters.")

st.divider()

st.subheader("Complete a Task")

if owner.pets and all_tasks:
    complete_pet_name = st.selectbox(
        "Choose pet for task completion",
        [pet.name for pet in owner.pets],
        key="complete_pet_name"
    )

    matching_pet_tasks = scheduler.filter_tasks(
        pet_name=complete_pet_name,
        completion_status=False
    )
    task_choices = [task.description for _, task in matching_pet_tasks]

    if task_choices:
        complete_task_description = st.selectbox(
            "Choose task to mark complete",
            task_choices
        )

        if st.button("Mark Task Complete"):
            result = scheduler.mark_task_complete(
                complete_pet_name,
                complete_task_description
            )
            st.success(result)
    else:
        st.info("This pet has no incomplete tasks.")
else:
    st.info("Add pets and tasks before marking tasks complete.")

st.divider()

st.subheader("Build Schedule")

schedule_mode = st.radio(
    "Schedule mode",
    ["Standard Priority Schedule", "Weighted Smart Schedule"]
)

if st.button("Generate Schedule"):
    if schedule_mode == "Standard Priority Schedule":
        schedule = scheduler.create_daily_schedule()
        explanation = scheduler.get_schedule_explanation()
    else:
        schedule = scheduler.create_weighted_schedule()
        explanation = scheduler.get_weighted_schedule_explanation()

    conflicts = scheduler.detect_conflicts()

    if conflicts:
        st.warning("Scheduling conflicts detected:")
        for conflict in conflicts:
            st.warning(conflict)

    if schedule:
        st.success("Daily schedule generated.")
        st.markdown("### Today's Schedule")
        st.table(tasks_to_rows(schedule))

        st.markdown("### Why this plan was chosen")
        st.info(explanation)
    else:
        st.warning("No incomplete tasks available to schedule.")
