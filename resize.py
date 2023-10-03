import os
from PIL import Image

def resize_images(source_dir, target_dir, target_size=(640, 640)):
    try:
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Loop through all files in the source directory
        for filename in os.listdir(source_dir):
            if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
                input_path = os.path.join(source_dir, filename)
                output_path = os.path.join(target_dir, filename)
                
                try:
                    # Open the image file
                    with Image.open(input_path) as img:
                        # Preserve aspect ratio and resize to fit within the specified dimensions
                        if hasattr(Image, "ANTIALIAS"):
                            img.thumbnail(target_size, Image.ANTIALIAS)
                        else:
                            img.thumbnail(target_size, Image.LANCZOS)
                        # Save the resized image to the target directory
                        img.save(output_path)
                        print(f"Resized and saved: {output_path}")
                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
if __name__ == "__main__":
    input_image_path = "D:\\photos"  # Replace with the path to your input image
    output_image_path = "data2"  # Replace with the desired output path

    # Call the function to resize the image
    resize_images(input_image_path, output_image_path)
