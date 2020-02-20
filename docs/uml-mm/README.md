# UML-greiene her baserer seg på PlantUML

## Trenger plantUML, JRE og graphviz
Kan installeres greit i bash
```bash
sudo apt install -y graphviz default-jre

sudo mkdir -p /opt/plantuml
cd /opt/plantuml
UML=http://sourceforge.net/projects/plantuml/files/plantuml.jar/download
sudo curl -JLO ${UML}
```


## For å få fram ganske digge uml-diagrammer i Atom:
- Last ned .jar fra https://plantuml.com/download
- Installer plantuml-preview https://atom.io/packages/plantuml-preview


## For å få fram ganske digge uml-diagrammer i Code:
- Installer plantUML extension (jebbs.plantuml)
- Åpne en uml fil og trykk alt+D
