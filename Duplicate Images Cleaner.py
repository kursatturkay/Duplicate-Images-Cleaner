# pip install pillow imagehash send2trash
#run this python command in images
import os
import shutil
import hashlib
from PIL import Image
import imagehash
import send2trash

def calculate_hash(image_path):
    """Calculates the perceptual hash for an image."""
    try:
        img = Image.open(image_path)
        
        return str(imagehash.phash(img))
    except Exception as e:
        print(f"Error: Unable to calculate hash for {image_path} - {e}")
        return None

def find_and_remove_duplicates(directory):
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    
    hashes = {}
    processed_count = 0
    duplicate_count = 0
    error_count = 0
    
    print(f"Scanning images in '{directory}'...")
    
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in image_extensions):
            try:
                
                file_hash = calculate_hash(file_path)
                
                if file_hash:
                    processed_count += 1
                    
                    
                    if file_hash in hashes:
                        
                        print(f"Duplicate found: '{filename}' -> '{os.path.basename(hashes[file_hash])}'")
                        send2trash.send2trash(file_path)
                        duplicate_count += 1
                    else:
                        
                        hashes[file_hash] = file_path
            except Exception as e:
                print(f"Error: An issue occurred while processing '{filename}' - {e}")
                error_count += 1
    
    
    print("\nProcess completed!")
    print(f"Total images processed: {processed_count}")
    print(f"Duplicate images found and moved to trash: {duplicate_count}")
    print(f"Files with errors: {error_count}")

if __name__ == "__main__":
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    print("Image Duplicate Cleaner")
    print("----------------------------")
    print(f"Scanning directory: {script_directory}")
    print("This program will detect visually similar image files in the script's directory,")
    print("keep only one copy, and move the duplicates to the trash.")
    print("Note: Files are not permanently deleted; they are sent to the trash.")
    print("----------------------------")
    
    confirmation = input("Do you want to continue? (y/n): ")
    
    if confirmation.lower() == 'y':
        find_and_remove_duplicates(script_directory)
    else:
        print("Operation canceled.")
