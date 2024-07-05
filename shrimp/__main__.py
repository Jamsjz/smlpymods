from PIL import Image, ImageEnhance, ImageFilter
import os
from os import system
from sys import argv
import re
from reportlab.platypus import SimpleDocTemplate, Image as RLImage


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
        f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png", ".gif"))
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


def covert_images_to_pdf(folder_path, output_filename):
    # Get a list of all image files in the folder
    image_files = [
        f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png", ".gif"))
    ]

    # Sort the image files based on the numeric part of the file name
    sorted_image_files = sorted(image_files, key=lambda x: extract_number(x))

    # Create a list to store the image objects
    images = []

    # Open each image file, resize it to fit the page size, and append it to the images list
    for image_file in sorted_image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        image.thumbnail((700, 900), Image.LANCZOS)
        images.append(RLImage(image_path, width=image.width, height=image.height))
    # Create a PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=(1920, 1080))
    doc.build(images)

    print(f"PDF created: {output_filename}")


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


def img_to_pdf():
    folder_path = input("Enter the path to the folder containing the images: ")
    output_filename = input("Enter the output filename (e.g., output.pdf): ")

    covert_images_to_pdf(folder_path, output_filename)
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


def menu():
    clear()
    start()
    print("1. Convert image to photocopy")
    print("2. Convert image to PDF")
    print("3. Combine images vertically")
    print("4. Reduce image size")
    print("5. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        img_to_photocopy()
    elif choice == "2":
        img_to_pdf()
    elif choice == "3":
        combine_two_images()
    elif choice == "4":
        red_img_sz()
    elif choice == "5":
        exit()
    else:
        print("Invalid choice. Please try again.")
        menu()


if __name__ == "__main__":
    menu()
