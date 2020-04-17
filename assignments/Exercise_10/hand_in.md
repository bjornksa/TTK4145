# Part 1 - Deadlock
## 1
``` LTSA
RESOURCE = (get->put->RESOURCE).

A = (printer.get->scanner.get->copy ->printer.put->scanner.put->A).

B = (scanner.get->printer.get->copy ->scanner.put->printer.put->B).

||SYS = (a:A||b:B
||{a,b}::printer:RESOURCE
 ||{a,b}::scanner:RESOURCE
 ).
```
This system creates a deadlock if one process starts with aquring the printer resource while the other aqquires the scanner. LTSA easily finds the lock:
```
Trace to DEADLOCK:
	a.printer.get
	b.scanner.get
Analysed in: 1ms
```
## 2
There are four sufficient and necessary conditions for deadlock. When all conditions hold simultaneously, a deadlock happens.
 - Mutual Exlusion
 - Resource holding
 - No preemption
 - Circular wait

# Part 2 - Livelock
## 1
```
LIGHT    = (turn_on->green -> turn_off -> LIGHT | turn_on->green -> turn_off -> LIVELOCK_LIGHT_1),
LIVELOCK_LIGHT_1 = (turn_on-> red -> turn_off -> LIVELOCK_LIGHT_2),
LIVELOCK_LIGHT_2 = (turn_on-> yellow -> turn_off -> LIVELOCK_LIGHT_1).
```
This system creates a livelock if the *LIGHT* process blinks red and goes to LIVELOCK_LIGHT_1

```
Progress violation for actions:
	green
Trace to terminal set of states:
	turn_on
	green
	turn_off
Cycle in terminal set:
	turn_on
	red
	turn_off
	turn_on
	yellow
	turn_off
Actions in terminal set:
	{red, turn_off, turn_on, yellow}
Progress Check in: 2ms
```
## 2
```
progress P = {yellow, red}
```
Adding this line to tell the system we only need the yellow and red lights no longer gives any warnings off progress violation. Perhaps we want a blinking yellow/red light to warn about a detected error or similar.

# Part 3 - Dining philosophers
## 1
From the included LTSA exmples:
```
PHIL = (sitdown->right.get->left.get
          ->eat->left.put->right.put
          ->arise->PHIL).

FORK = (get -> put -> FORK).

||DINERS(N=3)=
   forall [i:0..N-1]
   (phil[i]:PHIL
   ||{phil[i].left,phil[((i-1)+N)%N].right}::FORK).

menu RUN = {phil[0..4].{sitdown,eat}}

```
this causes the standard dining philosopher deadlock


```
Trace to DEADLOCK:
	phil.0.sitdown
	phil.0.right.get
	phil.1.sitdown
	phil.1.right.get
	phil.2.sitdown
	phil.2.right.get
Analysed in: 0ms
```
## 2
7 philosophers is no problem, 8 takes some time and maxes out one CPU core
Output with 8 philosophers -- States: 1679616 Transitions: 11837296 Memory used: 916909K

9 philosophers makes the computer struggle and took so long that I stopped it before it finished. Any more seems pointless
## 3
Adding the following to the system
```
PHIL(I=0) = (when (I%2==0)
                 sitdown->left.get->right.get
                   ->eat->left.put->right.put->arise->PHIL
            |when (I%2==1)
                 sitdown->right.get->left.get
                   ->eat->left.put->right.put->arise->PHIL
            ).
```
 gives a setup where half the philosophers start by piking up the left fork, and avoids all deadlocks.
## 4
Fair solutions include numbering the chopsticks and having the philopsophers pick the lowest one at all times, or using a salt shaker (mutex) that the eating philosopher has to hold
