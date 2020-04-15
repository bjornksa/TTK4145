# Exercise 9 - Scheduling

## Properties

### Task 1:
 1. Why do we assign priorities to tasks?

We assign priorities to tasks to decide what tasks are most important. When multiple processes asks for the same resources at the same time, we want the most important task (the task with the highest priority) to be executed first.

 2. What features must a scheduler have for it to be usable for real-time systems?

The scheduler have to be predictable.


## Inversion and inheritance


| Task | Priority   | Execution sequence | Release time |
|------|------------|--------------------|--------------|
| a    | 3          | `E Q V E`          | 4            |
| b    | 2          | `E V V E E E`      | 2            |
| c    | 1 (lowest) | `E Q Q Q E`        | 0            |

 - `E` : Executing
 - `Q` : Executing with resource Q locked
 - `V` : Executing with resource V locked


### Task 2: Draw Gantt charts to show how the former task set:
 1. Without priority inheritance

 | Task | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14|
 |------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
 | a    |   |   |   |   |E  |   |   |   |   |   |   |Q  |V  |E  |   |
 | b    |   |   |E  |V  |   |V  |E  |E  |E  |   |   |   |   |   |   |
 | c    |E  |Q  |   |   |   |   |   |   |   |Q  |Q  |   |   |   |E  |

 2. With priority inheritance

 | Task | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14|
 |------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
 | a    |   |   |   |   |E  |   |   |Q  |   |V  |E  |   |   |   |   |
 | b    |   |   |E  |V  |   |   |   |   |V  |   |   |E  |E  |E  |   |
 | c    |E  |Q  |   |   |   |Q  |Q  |   |   |   |   |   |   |   |E  |


### Task 3: Explain:
 1. What is priority inversion? What is unbounded priority inversion?

Priority inversion: a task of higher priority have to wait for a task of lower priority. This may happen when the two tasks share the same resources.

Unbounded priority inversion: An instance of priority inversion where the higher priority task may get stuck waiting for the lower priority task forever.

 3. Does priority inheritance avoid deadlocks?

No. Priority inheritance does not avoid dedlocks.



## Utilization and response time

### Task set 2:

| Task | Period (T) | Exec. Time (C) |
|------|------------|----------------|
| a    | 50         | 15             |
| b    | 30         | 10             |
| c    | 20         | 5              |

### Task 4:
 1. There are a number of assumptions/conditions that must be true for the utilization and response time tests to be usable (The "simple task model"). What are these assumptions? Comment on how realistic they are.

"Fixed set of periodic, independent tasks with known periods, constant worst-case execution times, and deadlines equal to their periods. They run on a single processor where overheads run in zero time. A critical instant is the instant when the processor runs with maximum load." (Wikipendium)

 2. Perform the utilization test for the task set. Is the task set schedulable?

If the task set is schedulable, then U <= n*(2⁽1/n)-1.
Using the formula attached at the end of this document, we get the following:

U = 0.883 <= 0.7789.

Since the equation above fails, we know that the task is not schedulable.

 3. Perform response-time analysis for the task set. Is the task set schedulable? If you got different results than in 2), explain why.

Task c:

w_0 = 5 \
R_c = 5 <= 20

Task b:

w_0 = 10 \
w_1 = 10 + (10/20)5 = 15 \
w_2 = 10 + (15/20)5 = 15 \
R_b = 15 <= 30

Task c:

w_0 = 15 \
w_1 = 15 + (15/30)10 + (15/20)5 = 30 \
w_2 = 15 + (30/30)10 + (30/20)5 = 35 \
w_3 = 15 + (35/30)10 + (35/20)5 = 45 \
w_4 = 15 + (45/30)10 + (45/20)5 = 50 \
w_5 = 15 + (50/30)10 + (50/20)5 = 50 \
R_1 = 50 <= 50

 4. (Optional) Draw a Gantt chart to show how the task set executes using rate monotonic priority assignment, and verify that your conclusions are correct.

## Formulas

Utilization:
![U = \sum_{i=1}^{n} \frac{C_i}{T_i} \leq n(2^{\frac{1}{n}}-1)](eqn-utilization.png)

Response-time:
![w_{i}^{n+1} = C_i + \sum_{j \in hp(i)} \bigg \lceil {\frac{w_i^n}{T_j}} \bigg \rceil C_j](eqn-responsetime.png)
