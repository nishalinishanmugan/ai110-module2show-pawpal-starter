# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Brainstorm:
The three core actions can:
    1. Owner and Pet information - basic information about the owner and pet like the owner's name, pet's name, pet type, pet age, preferences, etc. 
    2. Pet care tasks - feeding, walking, medication, grooming, play schedule, etc. Time of each task and the priority. 
    3. Daily Care Plan - based on task priority, preferences, and avaiable time. Why are tasks choosen, delayed or left out.


Building Blocks: 
1. Owner
- Attributes: name, time_available, preferences, schedule_notes
- Methods: update_time_available(), update_preferences()

2. Pet
- Attributes:name, species, breed, age, care_notes
- Methods: update_info(), get_summary()

3. Task
- Attributes: title, category, duration, priority, preferred_time, notes, required or is_mandatory
- Methods: edit_task(), mark_complete(), get_task_details()

4. Planner or Scheduler
- Attributes: tasks, available_time, selected_plan, reasoning_log
- Methods: generate_plan(), sort_tasks_by_priority(), filter_tasks_by_constraints(), explain_plan()

5. DailyPlan
- Attributes: planned_tasks, total_time, unused_time, explanation
- Methods: display_plan(), calculate_total_time(), get_explanation()

- Briefly describe your initial UML design.
 The initial UML design is Owner, Pet, Task, and Scheduler. These cover the main requirements of the app based on the description. Because we need to track pet care tasks (Task), contraints (Scheduler), and Daily Plan (Scheduler). And the other two classes are Owner and Pet because those are the two thing that are interacting in our app. 

- What classes did you include, and what responsibilities did you assign to each?

The Owner class stores the pet owner’s information like name, available time, and preferences. This class represents the person making decisions and providing constraints for the daily plan. The Pet class stores information about the pet like name, species, age, and care notes. The Task class represents each pet care activity, like feeding, walking, or giving medication. It has details such as duration, priority, notes, and whether the task is mandatory. The Scheduler class is responsible for the decision making. It takes tasks and owner constraints, sorts and filters them, and generates the daily plan while also keeping track of reasoning for why tasks were chosen. A potentail logic bottle neck would be if the Scheduler becomes overloaded because it handles too many responsibilites such as sorting tasks, applying preferences, checking time limits, and explaining. It's possible that the scheduler task needs to break up into two classes. One for creating the plan and the other for storing it. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
