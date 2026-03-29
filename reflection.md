# PawPal+ Project Reflection

## 1. System Design

Core Actions: 
1. Add a pet profile
2. View daily tasks
3. Allow for user to add/edit tasks (including removal of tasks upon completion?)

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Classes:
1. **Owner** : This class is meant to handle all owner profile configuration
- Attributes: UUID, Name
- Methods: createProfile

2. **Pets** : This class is meant to handle all pet profile configuration
- Attributes: UUID, OwnerID, Name, Breed, Age, MedicationID
- Methods: createPetProfile

3. **Tasks** : This class is meant to handle all task configuration (including removal/editing of tasks)
- Attributes: ID, OwnerID, PetID, Date, Priority, TaskName, TaskDescription, Duration, Completed?
- Methods: addTask, removeTask, editTask

4. **Scheduler** : This class is meant to encapsulate the 'smart' functionality of our tool, that generates a schedule based on the owner's list of tasks for the day (evaluates each task's priority, duration, and owner's availablity)
- Attributes: Date, Schedule
- Methods: generateDaySchedule

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

**Changes Made:**
- Moved the edit/add task methods to be a part of the Owner class. Our first implementation forgot to account for the list of tasks that have to be visible from the Owner class in order to create a schedule for the owner. Therefore, with the list of tasks living in the Owner class, the methods to remove or add to that list should easily access that list, which would not have been possible if these methods were part of the Tasks class (handles individal task configuration).

**Summary of All Changes Made:**
- Added `pets` and `tasks` list attributes to `Owner` to establish direct relationships between an owner and their data, replacing loose string ID references as the only link.
- Added `owner_id` to `Scheduler` so schedule generation is scoped to a specific owner.
- Converted `createProfile` and `createPetProfile` to class methods (`@classmethod`) since they construct new objects rather than operate on existing ones.
- Replaced raw `int` priority on `Task` with a `Priority` enum (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) to enforce valid values and improve readability.
- Removed `addTask`/`removeTask` from `Task` and placed them on `Owner`, where the task list is accessible.

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
