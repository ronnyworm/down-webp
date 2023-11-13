# Download images from url and convert to webp
Also performs compression by default.

## Install
	pip install -r requirements.txt

## Execute
Saves the images in the folder (url)-images-75 (default quality level is 75)

	python3 down-webp.py URL

The quality can be specified as an additional parameter (1-95), then it will be saved in a different folder. Example:

	python3 down-webp.py URL 50
	# saves images in (url)-images-50

The images have a prefix (order of the image).

## Image file types
converted to lowercase automatically

	['png', 'jpeg', 'jpg', 'webp']