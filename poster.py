#!/home/hk/script/troetomatic/myvenv/bin/python3

from mastodon import Mastodon
from PIL import Image
from fractions import Fraction
from math import sqrt
import exifread
import os
import random
import requests

### CONFIGURATION ###

from settings import *

####################

# log in, etc.
def __prepare():
    Mastodon.create_app(
        'pytooterapp',
        api_base_url=server,
        to_file=clientcred)
    mastodon = Mastodon(
        client_id=clientcred,
        api_base_url=server)
    mastodon.log_in(
        user,
        passwd,
        to_file=usercred)

def __getRandomFile(dir):
    files = os.listdir(dir)
    filesFiltered = []
    for file in files:
        if ("jpeg" in file) or ("jpg" in file) or ("JPEG" in file) or ("JPG" in file):
            filesFiltered.append(file)
    l = len(filesFiltered)
    if l > 0:
        ptr = random.randint(0, l-1)
        return os.path.join(dir, filesFiltered[ptr])
    else:
        return None

def __convert_to_degress(value):
    d = float(Fraction(str(value.values[0])))
    m = float(Fraction(str(value.values[1])))
    s = float(Fraction(str(value.values[2])))
    return d + (m / 60.0) + (s / 3600.0)

def __getInfo(photo):
    text = "Guten Morgen mit einem zufälligen Photo aus meinem Fundus!"

    try:

        f = open(photo, 'rb')
        tags = exifread.process_file(f)
        f.close()

        xns = str(tags["GPS GPSLatitudeRef"])
        x = tags["GPS GPSLatitude"]
        xdeg = __convert_to_degress(x)
        if xns == ("S"):
            xdeg = xdeg * (-1.0)

        ywe = str(tags["GPS GPSLongitudeRef"])
        y = tags["GPS GPSLongitude"]
        ydeg = __convert_to_degress(y)
        if ywe == ("W"):
            ydeg = ydeg * (-1.0)

        S = requests.Session()
        URL = "https://de.wikipedia.org/w/api.php"

        PARAMS = {
            "format": "json",
            "list": "geosearch",
            "gscoord": str(xdeg) + "|" + str(ydeg),
            "gslimit": "10",
            "gsradius": "10000",
            "action": "query"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        place = DATA['query']['geosearch'][0]
        id = str(place["pageid"])
        title = place["title"]

        text = text + " Laut Wikipedia zeigt das Photo {} bzw. wurde in der Nähe aufgenommen.".format(title)
        text = text + " Wenn du willst, kannst du hier etwas darüber lesen: https://de.wikipedia.org/?curid={}".format(id)
    except:
        pass

    try:
        make = str(tags["Image Make"])
        if "NIKON" in make:
            make = "Nikon"
        if "SONY" in make:
            make = "Sony"
    except:
        make = None

    try:
        model = str(tags["Image Model"])
        if "ILCE" in model:
            model = model.replace("ILCE-", "α")
        if "NIKON" in model:
            model = model.replace("NIKON ", "")
    except:
        model = None

    try:
        lens = str(tags["EXIF LensModel"])
    except:
        lens = None

    try:
        focallength = str(tags["EXIF FocalLength"])
    except:
        focallength = None

    try:
        shutterspeed = str(tags["EXIF ExposureTime"])
    except:
        shutterspeed = None

    try:
        aperture = str(tags["EXIF ApertureValue"])
        if "/" in aperture:
            a = int(aperture.split("/")[0])
            b = int(aperture.split("/")[1])
            f = round(sqrt(2**(a/b)), 1)
        else:
            a = int(aperture)
            f = round(sqrt(2 ** a), 1)
    except:
        f = None

    exif = ""
    if make and model:
        exif = exif + " Kamera: {} {}".format(make, model)
    if not ((lens == "----") or (lens == None)):
        exif = exif + ", Objektiv: {}".format(lens)
    if shutterspeed:
        exif = exif + ", Belichtung: {}sec".format(shutterspeed)
    if not ((focallength == "0") or (focallength == None)):
        exif = exif + ", Brennweite: {}mm".format(focallength)
    if f:
        exif = exif + ", ƒ{}".format(f)

    if exif:
        return text + " -- EXIF-Daten: {}".format(exif)
    else:
        return text


if not os.path.exists(clientcred):
    __prepare()

photo = __getRandomFile(photodir)

if photo:

    text = __getInfo(photo) + "\n\n(Dies ist ein automatischer Tröt, der aber trotzdem von ❤️ kommt!)\n\n#foto #fotos #photo #photos #photography"

    # load image, get sizes, compute rescale factor
    image = Image.open(photo)

    x = image.size[0]
    y = image.size[1]
    factor = width / x

    # resize image, save as tmp.jpeg
    resized_image = image.resize((width, int(y*factor)))
    tmp = os.path.join(photodir, "tmp.jpeg")
    resized_image.save(tmp)

    #post the image
    if not debug:
        mastodon = Mastodon(
            access_token=usercred,
            api_base_url=server
        )
        photoID = mastodon.media_post(tmp)
        mastodon.status_post(text,
                             media_ids=(photoID),
                             visibility="public",
                             )
    else:
        print(text)

    # remove posted image and tmp.jpeg
    #os.remove(photo)
    os.remove(tmp)

else:
    print("No more photos")
