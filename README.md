# Download images from url and convert to webp
Kann auch bei Bedarf eine Kompression durchführen.

## Installieren
	pip install -r requirements.txt

## Ausführen
Speichert die Bilder im Ordner tmp-images-75 (Standardqualitätlevel ist 75)

	python3 down-webp.py URL

Die Qualität kann noch als zusätzlicher Parameter mitgegeben werden (1-95), dann wird es in einem anderen Ordner gespeichert. Beispiel:

	python3 down-webp.py URL 50
	# speichert Bilder in tmp-images-50
