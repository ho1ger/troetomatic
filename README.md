# troetomatic

A simple script by https://muenchen.social/@holger that troets random photos from a folder.
If the image is geotagged, the script finds the nearest Wikipedia article, uses the name of this article as an "guessed" image description, and links to that article.
If there are EXIF tags, the script will extract some meta data about camera, lens, settings and add it to the image description.

## Install

- run `setup.sh` to create a virtual environment where a couple of dependancies are installed and a folder for images
- fill in the settings template file with your detail and rename to `settings.py`
- change the path to the virtual environment in the poster.py file (very top)
- put a couple of images to the images folder
- add a cronjob that fires the script every day at, e.g., 7:30

    crontab -e

    30 7 * * * /path/to/troetomatic/poster.py

## Licence

Do whatever you want.
