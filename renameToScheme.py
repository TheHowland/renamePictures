import piexif
import re
import os


path = "C:\\Users\\YannickWieland\\Desktop\\Edit"


skipped = 0
failed = 0
renamed = 0

files = os.listdir(path)
for file in files:
    if not (file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg")):
        continue

    filename = os.path.splitext(file)[0]
    if re.match("IMG_[0-9]{8}_[0-9]{6}", filename):
        print(f"Skipped {filename}")
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

        if date_str:
            newName = "IMG_"+date_str.decode().replace(":", "").replace(" ","_")+".jpg"

            iteration = 1
            while os.path.exists(os.path.join(path, newName)):
                newName = "IMG_" + date_str.decode().replace(":", "").replace(" ", "_") + "_" + str(iteration) + ".jpg"
                iteration += 1

            os.rename(os.path.join(path, file), os.path.join(path, newName))
            renamed += 1
            print(f"Renamed {file} to {newName}")
        else:
            print(f"Failed {filename}")
            failed += 1

print(f"Renamed {renamed}; Skipped {skipped}; failed {failed}")