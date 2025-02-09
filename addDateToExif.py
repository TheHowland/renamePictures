import piexif
from piexif import InvalidImageDataError
import os
import re
import changeFileFormat
from datetime import datetime
from tqdm import tqdm

dateAssumption = ""
while not re.match("[0-9]{4}:[0-9]{2}:[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", dateAssumption):
    dateAssumption = input("Enter the assumption date string like YYYY:MM:DD HH:mm:ss :\n")

path = "D:\\Eigene Dateien\\Bilder\\2018"

def adjust_date(exif_dict: dict) -> bool:
    keys = exif_dict["Exif"].keys()
    if not keys:
        return True
    if 36867 in keys or 36868 in keys:
        return False
    else:
        return True

def add_year_to_jpeg(filePath, dateAssumption):
    # Ensure the year is a valid four-digit number
    fileName = os.path.basename(filePath)
    dateStrType = ""

    # Construct EXIF date format with default month and day
    if bool(re.match(r"IMG_[0-9]{8}_[0-9]{6}", fileName)):
        year = fileName[4:8]
        month = fileName[8:10]
        day = fileName[10:12]
        hour = fileName[13:15]
        minute = fileName[15:17]
        second = fileName[17:19]
        date_str = f"{year}:{month}:{day} {hour}:{minute}:{second}"
        dateStrType = f"\tdate and time: {date_str}"
    elif bool(re.match(r"IMG-[0-9]{8}-WA[0-9]{4}", fileName)):
        year = fileName[4:8]
        month = fileName[8:10]
        day = fileName[10:12]
        date_str = f"{year}:{month}:{day} 00:00:00"
        dateStrType = f"\tdate: {date_str}"
    else:
        date_str = dateAssumption
        dateStrType = f"\tassumption: {date_str}"

    # Load existing EXIF data or create a new one
    exif_dict = piexif.load(filePath)
    if adjust_date(exif_dict):
        # Update the DateTimeOriginal and DateTimeDigitized fields
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_str.encode()
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_str.encode()

        # Convert back to binary
        exif_bytes = piexif.dump(exif_dict)

        # Save the updated EXIF data to the image
        piexif.insert(exif_bytes, filePath)
        logText = f"Adjusted Date: {filePath}\n{dateStrType}\n"
        log.write(logText)
    else:
        logText = f"Skipped: {filePath}\n"
        log.write(logText)



files = os.listdir(path)
failedFiles = []
otherError = []

log = open("log"+datetime.now().strftime("_%Y%m%d_%H%M%S")+".txt", "a")
# Example usage
log.write("Adjust date in jpg-Files\n")
for file in tqdm(files, desc="Adjust date in jpg-Files"):
    try:
        add_year_to_jpeg(os.path.join(path, file), dateAssumption)
    except InvalidImageDataError as e:
        failedFiles.append(file)
    except Exception as e:
        otherError.append(file)
        log.write(f"Failed to add year to: {file}")


if otherError:
    print("Failed to add year to: ", otherError)

# move failed files in separate folder
failPath = os.path.join(path, "Failed")
os.mkdir(failPath)
for file in failedFiles:
    os.rename(os.path.join(path, file), os.path.join(failPath, file))

# retry on converted files
if failedFiles:
    changeFileFormat.convert_files_to_jpg(failPath, log)
    failedFiles = os.listdir(failPath)
    finalFailedFiles = []

    log.write("Retry adjust date in failed jpg-Files\n")
    for file in tqdm(failedFiles, desc="Retry adjust date in failed jpg-Files"):
        try:
            add_year_to_jpeg(os.path.join(path,'Failed', file), dateAssumption)
        except Exception:
            log.write(f"Failed to add year to: {file}")
            finalFailedFiles.append(file)

    finalFailPath = os.path.join(path, "Failed", "Failed")
    if finalFailedFiles:
        os.mkdir(finalFailPath)
    for file in finalFailedFiles:
        os.rename(os.path.join(failPath, file), os.path.join(finalFailPath, file))

log.close()