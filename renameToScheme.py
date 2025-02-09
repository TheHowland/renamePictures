import piexif
import re
import os
from datetime import datetime
from tqdm import tqdm

path = "C:\\Users\\YannickWieland\\Desktop\\Edit"


skipped = 0
failed = 0
renamed = 0

log = open("log"+datetime.now().strftime("_%Y%m%d_%H%M%S")+".txt", "a")

files = os.listdir(path)
for file in tqdm(files, desc="Renaming pictures"):
    if not (file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg")):
        continue

    filename = os.path.splitext(file)[0]
    if re.match("IMG_[0-9]{8}_[0-9]{6}", filename):
        log.write(f"Skipped {filename}\n")
        skipped += 1
    else:
        date_str = None
        exif_dict = piexif.load(os.path.join(path, file))
        keys = exif_dict["Exif"].keys()
        if piexif.ExifIFD.DateTimeOriginal in keys:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]
        elif piexif.ExifIFD.DateTimeDigitized in keys:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized]
        elif 306 in keys:
            date_str = exif_dict[306]
        elif re.match(".*[0-9]{8}_[0-9]{6}.*", file):
            match = re.match(r".*([0-9]{8}_[0-9]{6}).*", file).group(1)
            date_str = f"{match[0:4]}:{match[4:6]}:{match[6:8]} {match[9:11]}{match[11:12]}{match[12:13]}{match[13:15]}"
            date_str = date_str.encode('utf-8')

        if date_str:
            newName = "IMG_"+date_str.decode().replace(":", "").replace(" ","_")+".jpg"

            iteration = 1
            while os.path.exists(os.path.join(path, newName)):
                newName = "IMG_" + date_str.decode().replace(":", "").replace(" ", "_") + "_" + str(iteration) + ".jpg"
                iteration += 1

            os.rename(os.path.join(path, file), os.path.join(path, newName))
            renamed += 1
            log.write(f"Renamed {filename} to {newName}\n")
        else:
            log.write(f"Failed {filename}, no meta information to rename file\n")
            failed += 1
log.write(f"Renamed {renamed}; Skipped {skipped}; failed {failed}\n")
log.close()