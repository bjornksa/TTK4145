# Part 1 - Deadlock
``` LTSA
RESOURCE = (get->put->RESOURCE).

P = (printer.get->scanner.get->copy ->printer.put->scanner.put->P).

Q = (scanner.get->printer.get->copy ->scanner.put->printer.put->Q).

||SYS = (p:P||q:Q
||{p,q}::printer:RESOURCE
 ||{p,q}::scanner:RESOURCE
 ).
```
This system creates a deadlock if one process starts with aquring the printer resource while the other aqquires the scanner. LTSA easily finds the lock:
```
Trace to DEADLOCK:
	a.printer.get
	b.scanner.get
Analysed in: 1ms
```
