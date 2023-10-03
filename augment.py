import os
from PIL import Image, ImageEnhance
import random
import shutil

# Define the image augmentation function
def augment_image(image):
    # Randomly rotate the image (0, 90, 180, or 270 degrees)
    rotation_angle = random.choice([0, 90, 180, 270])
    rotated_image = image.rotate(rotation_angle)
    
    # Randomly adjust contrast
    contrast_factor = random.uniform(0.8, 1.2)
    enhanced_image = ImageEnhance.Contrast(rotated_image)
    adjusted_image = enhanced_image.enhance(contrast_factor)

    return adjusted_image

def resize_images_and_labels(source_dir, image_target_dir, labels_dir, labels_target_dir, target_size=(640, 640), num_augmentations=5):
    try:
        # Create the target directories if they don't exist
        if not os.path.exists(image_target_dir):
            os.makedirs(image_target_dir)
        if not os.path.exists(labels_target_dir):
            os.makedirs(labels_target_dir)

        # Determine the appropriate resampling filter based on Pillow version
        resampling_filter = Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.LANCZOS

        # Loop through all files in the source directory
        for filename in os.listdir(source_dir):
            if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
                input_path = os.path.join(source_dir, filename)
                
                try:
                    # Open and augment the image multiple times
                    with Image.open(input_path) as img:
                        if img is None:
                            print(f"Error opening image: {input_path}")
                            continue

                        for _ in range(num_augmentations):
                            augmented_img = augment_image(img.copy())

                            # Resize the augmented image
                            augmented_img.thumbnail(target_size, resampling_filter)

                            # Save the resized image to the image target directory
                            output_image_path = os.path.join(image_target_dir, f"{os.path.splitext(filename)[0]}_{_}.jpg")
                            augmented_img.save(output_image_path)
                            print(f"Resized and saved: {output_image_path}")

                            # Get the corresponding YOLO format label file name
                            label_filename = f"{os.path.splitext(filename)[0]}.txt"

                            # Load and modify the YOLO format label
                            label_path = os.path.join(labels_dir, label_filename)
                            with open(label_path, 'r') as label_file:
                                lines = label_file.readlines()
                            for line_num, line in enumerate(lines):
                                # Parse the YOLO format label
                                parts = line.strip().split()
                                if len(parts) == 5:
                                    class_id, x_center, y_center, width, height = parts
                                    x_center, y_center, width, height = map(float, [x_center, y_center, width, height])

                                    # Calculate the scaling factors for width and height
                                    width_scale = target_size[0] / img.width
                                    height_scale = target_size[1] / img.height

                                    # Adjust bounding box coordinates and dimensions
                                    x_center *= width_scale
                                    y_center *= height_scale
                                    width *= width_scale
                                    height *= height_scale

                                    # Create the new YOLO format label line
                                    new_line = f"{class_id} {x_center} {y_center} {width} {height}\n"
                                    lines[line_num] = new_line

                            # Save the modified YOLO format label to the labels target directory
                            output_label_path = os.path.join(labels_target_dir, f"{os.path.splitext(filename)[0]}_{_}.txt")
                            with open(output_label_path, 'w') as new_label_file:
                                new_label_file.writelines(lines)

                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    source_directory = "/mnt/newvolume/data/images"  # Replace with the path to your source image directory
    image_target_directory = "augmented_images"  # Replace with the desired target image directory
    labels_directory = "/mnt/newvolume/data/labels"  # Replace with the directory containing YOLO format labels
    labels_target_directory = "augmented_labels"  # Replace with the desired target labels directory

    # Call the function to augment images, resize labels, and save them in different directories
    resize_images_and_labels(source_directory, image_target_directory, labels_directory, labels_target_directory)
