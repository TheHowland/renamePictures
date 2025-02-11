from PIL import Image
import os
from tqdm import tqdm


def convert_png_to_jpg(input_path, output_path, quality=100):
    # Open the PNG image
    with Image.open(input_path) as img:
        # Convert image to RGB (removes alpha channel)
        img = img.convert("RGB")
        # Save as JPEG with specified quality
        img.save(output_path, "JPEG", quality=quality)

# Example usage
def convert_files_to_jpg(path, log):
    files = os.listdir(path)
    log.write("Converting files to jpg\n")
    for file in tqdm(files, desc="Converting files to jpg"):
        input_path = os.path.join(path, file)
        fileName = os.path.splitext(file)[0]
        output_path = os.path.join(path, fileName + ".jpg")
        try:
            convert_png_to_jpg(input_path, output_path)
            if os.path.splitext(input_path)[1].lower() != os.path.splitext(output_path)[1].lower():
                os.remove(input_path)
            log.write(f"Converted {input_path} to {output_path}")
        except Exception as e:
            log.write(f"Failed to convert {input_path}")