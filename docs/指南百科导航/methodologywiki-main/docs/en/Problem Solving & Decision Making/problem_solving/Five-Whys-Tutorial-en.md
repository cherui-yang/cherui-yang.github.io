# Five Whys Root Cause Analysis Tutorial

## 1. What is the Five Whys?

The **Five Whys** is a simple yet powerful root cause analysis (RCA) technique that systematically explores the cause-and-effect chain of a problem by repeatedly asking "why?" until the root cause leading to the problem is found, rather than stopping at surface symptoms.

This method was developed by Sakichi Toyoda, the founder of Toyota Motor Corporation, and adopted and promoted by the Toyota Production System. Its core idea is that the root of most problems is not obvious and requires layers of questioning to reveal.

## 2. Why Use the Five Whys?

The main purposes of using the Five Whys are:

-   **Go Beyond Surface Symptoms**: Helps the team avoid being misled by the immediate manifestations of a problem, and delve deeper into systemic or process-related root causes.
-   **Simple and Easy to Implement**: Does not require complex data analysis or statistical tools, making it easy for team members to understand and quickly get started.
-   **Identify Relationships**: Clearly reveals the causal relationships between different reasons.
-   **Find Fundamental Solutions**: By addressing the root cause, problems can be effectively prevented from recurring, rather than repeatedly dealing with the same troubles.

## 3. How to Implement the Five Whys?

Implementing the Five Whys usually follows these steps:

### Step One: Define the Problem

-   **Clearly Describe the Problem**: Work with the team to define the problem you are facing in clear, concise language. For example, "The website went down three times this week."
-   **Reach Consensus**: Ensure all participants have a common understanding of the problem.

### Step Two: Start Asking "Why?"

-   **First Question**: Ask the first "why?" for the defined problem.
    -   *Problem*: "The website went down three times this week."
    -   *Question*: "**Why** did the website go down?"
    -   *Answer*: "Because the database server was overloaded."

### Step Three: Continue Asking Until the Root Cause is Found

-   **Iterative Questioning**: Based on the previous answer, continue asking "why?". Repeat this process until a root cause is found that cannot be reasonably questioned further. Typically, about five "whys" are enough to find the root, but this is not a strict rule; sometimes it may be fewer or more than five.

    -   **Second Question**: "**Why** was the database server overloaded?"
        -   *Answer*: "Because a newly launched query function consumed a lot of resources."

    -   **Third Question**: "**Why** did this query function consume a lot of resources?"
        -   *Answer*: "Because it performed a full table scan and did not use an index."

    -   **Fourth Question**: "**Why** did it not use an index?"
        -   *Answer*: "Because the developers did not create an index for the relevant fields during design."

    -   **Fifth Question**: "**Why** did the developers not create an index?"
        -   *Answer*: "Because our Code Review Checklist did not include checks for database performance optimization, leading to this issue being overlooked."

### Step Four: Determine the Root Cause and Formulate Countermeasures

-   **Identify the Root Cause**: In the example above, the root cause can be identified as "a flaw in the code review process, lacking a database performance check step."
-   **Formulate Solutions**: Develop specific, feasible solutions for the root cause. For example, "Update the team's code review checklist to mandate performance evaluation and index checks for all database queries."

## 4. Practical Case

| Problem Statement                               |
| -------------------------------------- |
| **Our new product launch was delayed by two weeks.**       |
|                                        |
| **1. Why was it delayed?**                  |
| > Because the final Quality Assurance (QA) test failed.   |
|                                        |
| **2. Why did the QA test fail?**            |
| > Because a core functional module had a serious bug.    |
|                                        |
| **3. Why did this module have a bug?**         |
| > Because the development team encountered conflicts when integrating new and old code. |
|                                        |
| **4. Why were there conflicts during integration?**        |
| > Because the two engineers responsible for the module did not communicate sufficiently. |
|                                        |
| **5. Why did they not communicate sufficiently?**        |
| > Because our project management process did not establish mandatory cross-functional communication points. |
|                                        |
| **Root Cause and Countermeasure**                     |
| **Root Cause**: The project management process lacked critical communication mechanisms. |
| **Countermeasure**: Add a "cross-team technical solution review meeting" to the project management process to ensure full discussion of integration points before development. |

## 5. Tips and Considerations for Using the Five Whys

-   **Stay Objective**: Focus on processes and systems, not on blaming individuals.
-   **Based on Facts and Data**: When answering "why," base your answers on verifiable facts as much as possible, not subjective assumptions.
-   **Ensure Logical Chain Rigor**: Each "why" answer should directly lead to the previous question.
-   **Know When to Stop**: When you reach a root cause at a process, behavior, or system level, you can usually stop. If further questioning leads to uncontrollable answers (e.g., "because of human nature"), it means you've likely found an appropriate stopping point.

By effectively using the Five Whys, teams can systematically solve problems and drive continuous improvement in organizational processes.