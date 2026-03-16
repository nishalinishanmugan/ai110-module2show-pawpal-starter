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
Yes because I initially had planned for 5 classes before I knew it was supposed to be 4 classes after reading later. I also didn't think about how the Owner would manager multiple pets and have a method that would retrieve all the tasks across all the pets. 
- If yes, describe at least one change and why you made it.
I changed my UML diagram from 5 classes to 4. I changed the Task class attributes after understanding what was required. these changes made it easier to meet the project requirements. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler has task priority, which determines which task should be completed. Higher priority tasks are scheduled before lower priority tasks. For example, feeding is ranked higher over grooming. I also have task completion status to ensure only incomplete tasks are included. 

- How did you decide which constraints mattered most?
I decided which contraints mattered most based on the owner's time and the pet's prioritizes. A pet need the essentials first like food and water. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It chooses higher prioritize tasks, and it does prioritize a balanced schedule throughout the day. 
- Why is that tradeoff reasonable for this scenario?
Tasks are prioritzed over urgency. Like high-prority are proritized if they are not completed. This means that the schedule isn't balanced throughout the day. But this ensures that more tasks are not left incomplete after each day. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI for multiple parts of this project like generating the UML design, brainstorming different factors of this project like the classes. I also used AI for the code generation and debugging errors. 
- What kinds of prompts or questions were most helpful?
The more detailed the prompts and questions were, the more helpful of a response I got from the AI. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
I didn't accept AI suggestions that went againt what the project was asking. The AI first suggesting 6 classes but this project specified 4 main classes. And if the AI's suggestion was too complicated, I wouldn't accept it either. 
- How did you evaluate or verify what the AI suggested?
I tested the logic in my terminal by runing py main.py and py -m pytest. And I made sure the results matched what I was expecting. 

---

## 4. Testing and Verification

Core Behaviors
- Adding task to pets work correctly 
- Marking a task completes and it updates correctly 
- Sorting tasks works correctly 
- Recurring tasks works correct and creates a new instance
- Overlapping tasks are identified

Edge Cases
- Pet has no tasks
- Owner has no pets
- Two tasks happening at the same time
- All tasks are completed
- Tasks with the same priority or duration

**a. What you tested**

- What behaviors did you test?
I tested core behaviors to make sure the scheduler logic works correctly. I verified the task completion status when it is marked complete. I also checked the pet's task count and confirmed that tasks are sorted correctly. I also checked that conflict detection identifies tasks schedules at the same time. 
- Why were these tests important?
These tests are imporant because they cover the essiential features of the system, and this includes task management, scheduling behavior, and overlap detection. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am pretty sure that my scheduler works correctly for my cases. All my tests pass in my test cases. 
- What edge cases would you test next if you had more time?
If I had more time, I would test additional edge cases like multiple recurring tasks being completing at the same time, tasks with idential priority and duration values, invalid scheduled time, pets with no tasks, and owner with no pets. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satified with all the features I added to this project. I liked builidng up the Scheduler class and I was able to ad edge cases to it. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would expand this project to include my test cases. I want to support better timing input and I also want to include owner preferences like times of the day. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I like that I incrementally added to each part of this project. Starting of with a UML diagram was helpful. The more detailed I was with the AI, the better of a response I was recieving. So I was trying to think through all the aspects of this project. The best results came when I used AI for brainstorming, debugging, and refinement, and I also evaluated the suggestions carefully and adapted them to fit my actual design and requirements.
