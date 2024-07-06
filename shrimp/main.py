from PIL import Image, ImageEnhance, ImageFilter
from stdio.stdin.stdin import Char
import os
from os import system
from sys import argv
import re
import time
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
from PyPDF2 import PdfMerger
from PIL.ExifTags import TAGS


def clear():
    system("clear")


def strt():
    try:
        os.chdir(argv[1])
    except:
        print("Please provide a path to the folder containing the images.")
    clear()
    path = input(
        "Enter the path to the folder having the folder containing the images: "
    )
    return path


def start(path=strt()):
    if path:
        os.chdir(path)
    else:
        return 0


def reduce_image_size(input_image_path, output_image_path, max_size, quality):
    with Image.open(input_image_path) as img:
        # Get current width and height
        width, height = img.size

        # Calculate the new dimensions while maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int((max_size / width) * height)
        else:
            new_height = max_size
            new_width = int((max_size / height) * width)

        # Resize the image
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Save the image with the specified quality
        img.save(output_image_path, quality=quality, optimize=True)
        print(f"Image saved to {output_image_path}")


def photocopy_image(input_image, output_image):
    # Open the input image
    img = Image.open(input_image)

    # Convert the image to grayscale
    img = img.convert("L")

    # Increase the contrast of the image
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2.0)

    # Apply a sharpening filter to the image
    img = img.filter(ImageFilter.SHARPEN)

    # Add a border to the image to simulate a photocopy
    width, height = img.size
    new_width = width + 40
    new_height = height + 40
    new_img = Image.new("L", (new_width, new_height), color=255)
    new_img.paste(img, (20, 20))

    # Save the output image
    new_img.save(output_image)


def get_img_path(folder_path):
    image_files = [
        f
        for f in os.listdir(folder_path)
        if f.endswith((".jpg", ".png", ".gif", ".JPG"))
    ]
    for i in range(len(image_files)):
        image_files[i] = os.path.join(folder_path, image_files[i])

    return image_files


def extract_number(filename):
    match = re.search(r"(\d+)", filename)
    if match:
        return int(match.group(1))
    else:
        return 0


def images_to_pdf_batch(folder_path, output_pdf_name, batch_size=20):
    def get_image_files():
        return [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"))
        ]

    image_files = sorted(get_image_files())  # Sort files to maintain order
    merger = PdfMerger()

    def process_batch(batch_files, batch_index):
        batch_pdf_path = os.path.join(folder_path, f"batch_{batch_index + 1}.pdf")
        with Image.open(os.path.join(folder_path, batch_files[0])) as first_image:
            first_image.load()
            if first_image.mode == "RGBA":
                first_image = first_image.convert("RGB")
            first_image.save(
                batch_pdf_path,
                save_all=True,
                append_images=[
                    Image.open(os.path.join(folder_path, image_file)).convert("RGB")
                    for image_file in batch_files[1:]
                ],
            )
        return batch_pdf_path

    batch_pdfs = []
    for i in range(0, len(image_files), batch_size):
        batch_files = image_files[i : i + batch_size]
        batch_pdf_path = process_batch(batch_files, i // batch_size)
        if batch_pdf_path:
            batch_pdfs.append(batch_pdf_path)

    final_pdf_path = os.path.join(folder_path, output_pdf_name)
    with open(final_pdf_path, "wb") as final_pdf:
        for batch_pdf_path in batch_pdfs:
            with open(batch_pdf_path, "rb") as batch_pdf:
                merger.append(batch_pdf)
        merger.write(final_pdf)
    merger.close()

    for pdf in batch_pdfs:
        os.remove(pdf)

    print(f"All images converted and merged into {final_pdf_path}")


def combine_images_vertically(image1, image2, output_image):
    # Open the input images
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    # Get the width and height of the images
    width1, height1 = img1.size
    width2, height2 = img2.size

    # Create a new image with the combined height and the maximum width
    max_width = max(width1, width2)
    combined_height = height1 + height2
    new_image = Image.new("RGB", (max_width, combined_height))

    # Paste the first image at the top of the new image
    new_image.paste(img1, (0, 0))

    # Paste the second image below the first image
    new_image.paste(img2, (0, height1))

    # Save the combined image
    new_image.save(output_image)


def fphotocopy(folder_path, output_filename, output_path: str):
    print(os.getcwd())
    images = get_img_path(folder_path)
    for i, image in enumerate(images):
        photocopy_image(
            image,
            f"{output_path if not output_path.endswith('/') else output_path.strip('/')}/{output_filename}-{i}.jpg",
        )


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif()


def get_labeled_exif(exif):
    labeled = {}
    for key, val in exif.items():
        if key in TAGS:
            labeled[TAGS[key]] = val

    return labeled


def get_orientation(exif):
    if "Orientation" not in exif:
        return None
    return exif.get("Orientation", None)


def is_vertical(img):
    width, height = img.size
    return height > width


def rotate_image(img, orientation):
    if orientation == 3:
        return img.rotate(180, expand=True)
    elif orientation == 6:
        return img.rotate(270, expand=True)
    elif orientation == 8:
        return img.rotate(90, expand=True)
    else:
        return img


def rotate_vertical_photos(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Get a list of all image files in the source folder
    image_files = [
        f
        for f in os.listdir(source_folder)
        if f.lower().endswith((".jpg", ".png", ".gif", ".JPG"))
    ]

    # Iterate through all files in the source folder
    for image in image_files:
        image_path = os.path.join(source_folder, image)
        try:
            # Open the image file
            with Image.open(image_path) as img:
                # Get the EXIF data
                exif = get_exif(image_path)
                labeled = get_labeled_exif(exif)
                orientation = get_orientation(labeled)

                # Rotate the image based on the EXIF orientation
                rotated_img = rotate_image(img, orientation)

                # Check if the image is vertical and rotate it 90 degrees to the left
                if is_vertical(rotated_img):
                    rotated_img = rotated_img.rotate(90, expand=True)

                # Construct the destination file path
                destination_path = os.path.join(destination_folder, image)

                # Save the rotated image to the destination folder
                rotated_img.save(destination_path)
                print(f"Rotated and saved {image} to {destination_folder}")
        except IOError as e:
            print(f"Cannot open {image}. Skipping this file. Error: {e}")


def img_to_pdf():
    folder_path = input("Enter the path to the folder containing the images: ")
    output_filename = input("Enter the output filename (e.g., output.pdf): ")

    images_to_pdf_batch(folder_path, output_filename)
    menu()


def img_to_photocopy():
    folder_path = input("Enter the path to the folder containing the images: ")
    output_filename = input("Enter the output filename (e.g., output): ")
    output_path = input("Enter the output path (e.g., /path/to/output/): ")
    fphotocopy(folder_path, output_filename, output_path)
    menu()


def combine_two_images():
    image1 = input("Enter the path to the first image: ")
    image2 = input("Enter the path to the second image: ")
    output_image = input("Enter the output image path: ")
    combine_images_vertically(image1, image2, output_image)
    menu()


def red_img_sz():
    input_image = input("Enter the path to the input image: ")
    output_image = input("Enter the output image path: ")
    max_size = int(input("Enter the maximum size in pixels: "))
    quality = int(input("Enter a quality value between 1 and 95: "))

    reduce_image_size(input_image, output_image, max_size, quality)
    menu()


def rotate_vert_photos():
    source_folder = input("Enter the path to the source folder: ")
    destination_folder = input("Enter the path to the destination folder: ")

    rotate_vertical_photos(source_folder, destination_folder)


def menu():
    clear()
    start()
    print("1. Convert image to photocopy")
    print("2. Convert image to PDF")
    print("3. Combine images vertically")
    print("4. Reduce image size")
    print("5. Rotate vertical photos")
    print("6. Print current working directory")
    print("7. Exit")
    choice = Char().validin("Enter your choice: ", ["1", "2", "3", "4", "5", "6", "7"])
    if choice == "1":
        img_to_photocopy()
    elif choice == "2":
        img_to_pdf()
    elif choice == "3":
        combine_two_images()
    elif choice == "4":
        red_img_sz()
    elif choice == "5":
        rotate_vert_photos()
    elif choice == "6":
        print(os.getcwd())
        time.sleep(1)
        menu()
    elif choice == "7":
        exit()
    else:
        print("Invalid choice. Please try again.")
        menu()
