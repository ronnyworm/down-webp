# down-webp
Batch download images from url and convert to webp. **Don't use services like TinyPNG, CloudConvert or Convertio with accounts and payments -> do it on your machine!**

![](hero.png)

Caution! Does not download and compress CSS background images (yet)

Also performs compression by default.

## Install
	pip install -r requirements.txt

It's recommended to use [venv](https://docs.python.org/3/library/venv.html)

## Execute
See full parameter documentation like this:

	python3 down-webp.py

Saves the images in the folder (url)-images-75-down (default quality level is 75)

	python3 down-webp.py --url URL

The quality can be specified as an additional parameter (1-95), then it will be saved in a different folder. Example:

	python3 down-webp.py --url URL --quality 50
	# saves downloaded images in (url)-images-50-down
	# saves compressed images in (url)-images-50-compressed

The images can have a prefix (order of the image) if you need this. In that case, call the script as follows:

	python3 down-webp.py --url URL --add_prefix True

If the files should not be converted to webp, also add this parameter:

	--no_webp True

## Single file mode
Use this to convert and compress a local file

	python3 down-webp.py --file FILENAME

## Image file types
converted to lowercase automatically

	['png', 'jpeg', 'jpg', 'webp']
