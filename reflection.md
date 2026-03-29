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
