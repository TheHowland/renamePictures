import os
import filedate
from tqdm import tqdm
import piexif
import re
from datetime import datetime

path = "C:\\Users\\YannickWieland\\Desktop\\Edit"

log = open("logs\\creationDate"+datetime.now().strftime("_%Y%m%d_%H%M%S")+".log", "a")
files = os.listdir(path)
for file in tqdm(files, desc="Setting creation and modifide date"):
    filePath = os.path.join(path, file)
    try:
        exif_dict = piexif.load(filePath)
        keys = exif_dict["Exif"].keys()

        if piexif.ExifIFD.DateTimeOriginal in keys:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        elif piexif.ExifIFD.DateTimeDigitized in keys:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized].decode('utf-8')
        elif 306 in keys:
            date_str = exif_dict[306].decode('utf-8')
        elif re.match(".*[0-9]{8}_[0-9]{6}.*", file):
            match = re.match(r".*([0-9]{8}_[0-9]{6}).*", file).group(1)
            date_str = f"{match[0:4]}:{match[4:6]}:{match[6:8]} {match[9:11]}:{match[11:13]}:{match[13:15]}"

        day = date_str[8:10]
        month = date_str[5:7]
        year = date_str[0:4]

        hour = date_str[11:13]
        minute = date_str[14:16]
        second = date_str[17:19]

        date_str = f"{day}/{month}/{year} {hour}:{minute}:{second}"
        filedate.File(filePath).set(
            created = date_str,
            modified = date_str
        )
        log.write(f"Adjusted creation and modified date in: {file}\n")
    except Exception as e:
        log.write(f"Failed to adjusted creation and modified date in: {file}\n")
        continue

log.close()