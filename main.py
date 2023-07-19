import os
import argparse
from PIL import Image

def resize_and_convert_image(file_path, output_path, size):
    # Open the image file.
    with Image.open(file_path) as img:
        # Calculate the target height to maintain aspect ratio.
        target_height = int(size * (img.height / img.width))
        
        # Resize the image based on width.
        img = img.resize((size, target_height))
        
        # Create a new white 'background' image.
        background = Image.new('RGBA', (size, size), (255, 255, 255, 255))
        
        # Paste the resized image onto the background.
        bg_w, bg_h = background.size
        img_w, img_h = img.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(img, offset)
        
        # Save the new image to the output path.
        background.save(output_path)
        

def convert_images_in_folder(folder_path, output_folder, size, base_name=1000):
    # Ensure the output directory exists.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get a list of all files in the folder.
    files = os.listdir(folder_path)
    
    # Sort the list of files to ensure consistent output.
    files.sort()
    
    # Loop over all files.
    for i, filename in enumerate(files, start=base_name):
        # Create the full file path.
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image.
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.webp')):
            # Create the output file path.
            output_path = os.path.join(output_folder, f'{i}.png')
            
            # Resize and convert the image.
            resize_and_convert_image(file_path, output_path, size)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Resize images in a given folder to a specified size and save in a subfolder named 'converted'")

    # Add an argument for folder path
    parser.add_argument("-p", "--path", type=str, default=os.getcwd(), help="The folder containing the images to resize. Defaults to current directory if not specified.")

    # Add an argument for size
    parser.add_argument("-s", "--size", type=int, default=512, help="The target width for the resized images. Default is 512 if not specified.")

    # Parse the arguments
    args = parser.parse_args()

    # Exclude the output folder from the files to search
    if 'converted' in os.listdir(args.path):
        os.listdir(args.path).remove('converted')

    # Use the function to convert images in a folder.
    convert_images_in_folder(args.path, os.path.join(args.path, 'converted'), args.size)


if __name__ == "__main__":
    main()
