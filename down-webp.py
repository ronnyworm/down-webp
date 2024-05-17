import os
import sys
import requests
import argparse as ap
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse


def download_png_images(url, folder_path, quality, prefix, makewebp, user_agent):
    # Create the folder if it doesn't exist
    folder_down_path = folder_path + '-down'
    folder_compressed_path = folder_path + '-compressed'
    os.makedirs(folder_down_path, exist_ok=True)
    os.makedirs(folder_compressed_path, exist_ok=True)

    # Send an HTTP GET request to the URL
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags with the relevant extensions
    relevant_extensions = ['png', 'jpeg', 'jpg', 'webp']
    def is_relevant_extension(x):
        return x and any(x.lower().endswith(ext) for ext in relevant_extensions)
    images = soup.find_all('img', src=is_relevant_extension)

    # Download and save each image
    index = 0
    for img in images:
        img_url = img['src']

        if img_url.startswith('//'):
            img_url = 'https://' + img_url
            img_url = img_url.replace('////', '//')
        elif not img_url.startswith('http://') and not img_url.startswith('https://'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            img_url = base_url + '/' + img_url

        response = requests.get(img_url)

        if response.status_code != 200:
            continue

        # Extract the image filename from the URL
        if prefix:
            img_filename = os.path.join(folder_down_path, str(index).zfill(3) + '-' + os.path.basename(img_url))
        else:
            img_filename = os.path.join(folder_down_path, os.path.basename(img_url))
        index += 1

        # Save the original image
        with open(img_filename, 'wb') as f:
            f.write(response.content)
        print(f"{img_filename} downloaded", end='')

        # Compress and optionally convert to webp
        compress_and_convert(img_filename, makewebp, quality)


def compress_and_convert(img_filename, makewebp, quality):
    if makewebp:
        format_param = 'WEBP'
        target_filename = os.path.splitext(img_filename)[0] + '.webp'
    else:
        format_param = None
        target_filename = img_filename
    target_filename = target_filename.replace('-down', '-compressed')

    try:
        image = Image.open(img_filename)

        image.save(
            target_filename,
            format_param,
            quality=quality,
            method=6
        )

        print(f", converted")
    except Exception as e:
        print(f", skipped because of error: {type(e)}: {e}")


class MyParser(ap.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

if __name__ == '__main__':
    p = MyParser(description="Configuration", formatter_class=ap.ArgumentDefaultsHelpFormatter)
    p.add_argument("--url", help="URL")
    p.add_argument("--quality", type=int, default=75, help="Quality level - 75 is default and sufficient, max is 100") # default is printed
    p.add_argument("--prefix", type=bool, default=False, help="Should the script add a prefix to the compressed files so that it's clear in which order they appeared on the original page?")
    p.add_argument("--no_webp", type=bool, default=False, help="Should the script NOT convert all to webp after compressing?")
    p.add_argument("--user_agent", default='python-requests/2.31.0', help="Specify your own user agent if needed")
    p.add_argument("--file", help="File mode: convert just one file")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
    args = p.parse_args()
    print("Command line arguments are:")
    print(sys.argv[1:])

    if args.url is not None:
        url_without_http = args.url.replace('http://', '').replace('https://', '')
        url_cleaned = url_without_http.replace('/', '_')
        url_cleaned = url_cleaned.replace(':', '-')

        download_png_images(args.url, url_cleaned + '-images-' + str(args.quality), args.quality, args.prefix, not args.no_webp, args.user_agent)
    elif args.file is not None:
        print(args.file, end='')
        compress_and_convert(args.file, not args.no_webp, args.quality)
    else:
        print('Either url or file has to be specified! exiting ...')
