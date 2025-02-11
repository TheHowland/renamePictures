Those scripts are build to achive the following tasks:
  * **addDateToExif.py** -> add a date to the meta information of the jpg file, the date is picked from the picture if it matches the regex .*[0-9]{8}_[0-9]{6}.* wich indicates a date in most picture (20251230_123040 -> 30.12.2025 12:30:40)
  or set to the dateString defined on the terminal input when skript is started  
  * **changeCreationDate** -> sets the creation date to the date in the meta information of the picture
  * **changeFileFormat** -> is used in addDateToExif sometimes old pictures fail and succeed if saved as a new jpg
  * **renameToScheme** -> renaems pictures into IMG_YYYYMMDD_HHmmss from meta information of picture e.g. IMG_20251230_123040
