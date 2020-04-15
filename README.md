# Heisr

Kjør heisen med
```bash
python3 distributor.py
```

For å kjøre flere heiser ved siden av hverandre som skal koble seg til ulike simulatorporter kan man gjøre følgende:

``` bash
python3 distributor.py
python3 distributor.py 1
python3 distributor.py 2
```

Dette vil starte tre heiser med henholdsvis id 0, 1 og 2.

Heisene prøver å koble seg på simulator som kjører på port `15657 + id`. I dette tilfellet altså 15657, 15658 og 15659.

For å kjøre tre simulatorer på portene over kan man gjøre følgende:

```bash
./SimElevatorServer
./SimElevatorServer --port 15658
./SimElevatorServer --port 15659
```
