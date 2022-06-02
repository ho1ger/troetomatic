# troetomatic

A simple script by https://muenchen.social/@holger that troets random photos from a folder.
If the image is geotagged, the script finds the nearest Wikipedia article, uses the name of this article as an "guessed" image description, and links to that article.
If there are EXIF tags, the script will extract some meta data about camera, lens, settings and add it to the image description.

## Install

- `git clone https://github.com/ho1ger/troetomatic.git`
- run `setup.sh` from the repo to create a virtual environment where a couple of dependancies are installed, and to create a folder for images
- fill in the `settings_CHANGEME.py` file with your Mastodon account details and rename to `settings.py`
- change the path to the virtual environment in the `troetomatic.py` file (very top)
- put a couple of images to the images folder
- add a cronjob that fires the script every day at, e.g., 7:30

        crontab -e

        30 7 * * * /path/to/troetomatic/poster.py

## Licence

Do whatever you want.
