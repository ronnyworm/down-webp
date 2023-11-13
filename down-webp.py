import os, sys, requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Function to download and save PNG images from a URL to a folder
def download_png_images(url, folder_path, quality):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags with the ".png" extension
    png_images = soup.find_all('img', src=lambda x: x and (x.endswith('.png') or x.endswith('.jpeg') or x.endswith('.jpg')))


    # Download and save each PNG image
    index = 0
    for img in png_images:
        img_url = img['src']

        if img_url.startswith('//'):
            img_url = 'https://' + img_url
            img_url = img_url.replace('////', '//')
        elif not img_url.startswith('http://') and not img_url.startswith('https://'):
            img_url = url + '/' + img_url

        response = requests.get(img_url)

        if response.status_code == 200:
            # Extract the image filename from the URL
            img_filename = os.path.join(folder_path, str(index).zfill(3) + '-' + os.path.basename(img_url))
            index += 1

            # Save the image as PNG
            with open(img_filename, 'wb') as f:
                f.write(response.content)

            # Save the image as PNG
            print(f"{img_filename} downloaded", end='')

            # Convert the PNG image to WebP
            webp_filename = os.path.splitext(img_filename)[0] + '.webp'
            image = Image.open(img_filename)
            image.save(
                webp_filename,
                'WEBP',
                quality=quality,
                method=6
            )
            print(f", converted")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Gib bitte die URL an")
        sys.exit(0)

    url = sys.argv[1]

    if len(sys.argv) >= 3:
        quality = int(sys.argv[2])
    else:
        quality = 75

    url_without_http = url.replace('http://', '').replace('https://', '')
    url_cleaned = url_without_http.replace('/', '_')

    download_png_images(url, url_cleaned + '-images-' + str(quality), quality)