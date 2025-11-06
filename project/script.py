#!/usr/bin/env python3
"""
Script to filter KDEF images based on the CSV file.
Only keeps images that are listed in the CSV file.
"""

import os
import csv
import shutil
from pathlib import Path

# Paths
CSV_FILE = "Supplementary Material KDEF.PT_Revised2021.csv"
KDEF_DIR = "KDEF"
DATA_DIR = "data"
BACKUP_DIR = "KDEF_removed"  # Optional: backup removed files instead of deleting

def read_valid_image_codes(csv_path):
    """
    Read the CSV file and extract valid image codes (Picture_Code column).
    Returns a set of image codes (without file extension).
    """
    valid_codes = set()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        # Skip the first header row
        next(f)
        
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            picture_code = row.get('Picture_Code', '').strip()
            if picture_code:
                valid_codes.add(picture_code)
    
    print(f"Found {len(valid_codes)} valid image codes in CSV")
    return valid_codes

def get_all_images(kdef_dir):
    """
    Get all JPG images in the KDEF directory structure.
    Returns a list of Path objects.
    """
    kdef_path = Path(kdef_dir)
    if not kdef_path.exists():
        print(f"Error: KDEF directory '{kdef_dir}' not found")
        return []
    
    images = list(kdef_path.glob("*/*.JPG"))
    print(f"Found {len(images)} images in KDEF directory")
    return images

def filter_images(valid_codes, kdef_dir, backup=True):
    """
    Filter images: keep only those in valid_codes, remove or backup others.
    
    Args:
        valid_codes: Set of valid image codes from CSV
        kdef_dir: Path to KDEF directory
        backup: If True, move removed images to backup dir; if False, delete them
    """
    images = get_all_images(kdef_dir)
    
    if not images:
        print("No images found to process")
        return
    
    kept_count = 0
    removed_count = 0
    
    # Create backup directory if needed
    if backup:
        backup_path = Path(BACKUP_DIR)
        backup_path.mkdir(exist_ok=True)
    
    for image_path in images:
        # Get the image code (filename without extension)
        image_code = image_path.stem
        
        if image_code in valid_codes:
            # Keep this image
            kept_count += 1
        else:
            # Remove or backup this image
            removed_count += 1
            
            if backup:
                # Create backup subdirectory structure
                backup_subdir = backup_path / image_path.parent.name
                backup_subdir.mkdir(exist_ok=True)
                backup_file = backup_subdir / image_path.name
                
                # Move to backup
                shutil.move(str(image_path), str(backup_file))
                print(f"Moved to backup: {image_path.name}")
            else:
                # Delete the image
                image_path.unlink()
                print(f"Deleted: {image_path.name}")
    
    print(f"\nSummary:")
    print(f"  Images kept: {kept_count}")
    print(f"  Images removed: {removed_count}")
    
    # Remove empty directories
    cleanup_empty_dirs(kdef_dir)

def cleanup_empty_dirs(kdef_dir):
    """
    Remove empty subdirectories in KDEF directory.
    """
    kdef_path = Path(kdef_dir)
    removed_dirs = []
    
    for subdir in kdef_path.iterdir():
        if subdir.is_dir():
            # Check if directory is empty
            if not any(subdir.iterdir()):
                subdir.rmdir()
                removed_dirs.append(subdir.name)
    
    if removed_dirs:
        print(f"\nRemoved {len(removed_dirs)} empty directories:")
        for dir_name in removed_dirs:
            print(f"  - {dir_name}")

def copy_to_data_dir(kdef_dir, data_dir):
    """
    Copy filtered images to the data directory, maintaining structure.
    """
    kdef_path = Path(kdef_dir)
    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)
    
    images = get_all_images(kdef_dir)
    
    for image_path in images:
        # Create corresponding data subdirectory
        data_subdir = data_path / image_path.parent.name
        data_subdir.mkdir(exist_ok=True)
        
        # Copy image to data directory
        dest_file = data_subdir / image_path.name
        shutil.copy2(str(image_path), str(dest_file))
    
    print(f"\nCopied {len(images)} images to '{data_dir}' directory")

def main():
    """
    Main function to orchestrate the filtering process.
    """
    print("KDEF Image Filter")
    print("=" * 50)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found")
        return
    
    # Read valid image codes from CSV
    valid_codes = read_valid_image_codes(CSV_FILE)
    
    if not valid_codes:
        print("No valid image codes found in CSV")
        return
    
    # Ask user what to do
    print("\nOptions:")
    print("1. Filter images in KDEF directory (move removed to backup)")
    print("2. Filter images in KDEF directory (delete removed)")
    print("3. Copy only valid images to data directory (keep KDEF intact)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        filter_images(valid_codes, KDEF_DIR, backup=True)
    elif choice == "2":
        confirm = input("WARNING: This will permanently delete images. Continue? (yes/no): ")
        if confirm.lower() == "yes":
            filter_images(valid_codes, KDEF_DIR, backup=False)
        else:
            print("Cancelled")
    elif choice == "3":
        # First filter KDEF temporarily or work with a copy
        print("\nFiltering and copying to data directory...")
        
        # Get all images and filter
        images = get_all_images(KDEF_DIR)
        data_path = Path(DATA_DIR)
        data_path.mkdir(exist_ok=True)
        
        copied_count = 0
        for image_path in images:
            image_code = image_path.stem
            if image_code in valid_codes:
                # Create corresponding data subdirectory
                data_subdir = data_path / image_path.parent.name
                data_subdir.mkdir(exist_ok=True)
                
                # Copy image to data directory
                dest_file = data_subdir / image_path.name
                shutil.copy2(str(image_path), str(dest_file))
                copied_count += 1
        
        print(f"\nCopied {copied_count} valid images to '{DATA_DIR}' directory")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
