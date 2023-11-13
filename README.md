# Download images from url and convert to webp
Kann auch bei Bedarf eine Kompression durchführen.

## Installieren
	pip install -r requirements.txt

## Ausführen
Speichert die Bilder im Ordner (url)-images-75 (Standardqualitätlevel ist 75)

	python3 down-webp.py URL

Die Qualität kann noch als zusätzlicher Parameter mitgegeben werden (1-95), dann wird es in einem anderen Ordner gespeichert. Beispiel:

	python3 down-webp.py URL 50
	# speichert Bilder in (url)-images-50

Die Bilder haben ein Präfix (Reihenfolge des Bildes).