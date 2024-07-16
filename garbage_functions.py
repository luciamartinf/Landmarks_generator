#!/usr/bin/env python3

import os

def check_file_options(file):
    """
    Checks if a file exists and prompts the user for action if it does.
    """

    # Check if the file exists
    if os.path.isfile(file):
        # Enhanced error message
        print(f"WARNING: The file '{file}' already exists.")
        print("What do you want to do about it?")
        print("1. Override the existing file")
        print("2. Create a new version of the model")
        print("3. Exit training")

        # Get user input
        choice = input("Enter your choice (1/2/3): ")

        # Handle user choice
        if choice == '1':
            print(f"Overriding the existing file '{file}'...")
            # Remove the existing file
            os.remove(file)
            # Optionally create an empty file or handle accordingly
            open(file, 'a').close()
            print(f"File '{file}' has been overridden.")
        elif choice == '2':
            # Generate a new filename
            base, ext = os.path.splitext(file)
            new_file = base + "_new" + ext
            print(f"Creating a new version of the file '{new_file}'...")
            # Optionally create the new file or handle accordingly
            open(new_file, 'a').close()
            print(f"New version of the file '{new_file}' has been created.")
            return new_file
        elif choice == '3':
            print("Exiting training")
        else:
            print("Invalid choice. Going with default and creating a new version")
            sys.exit()
    else:
        print(f"Proceeding with training. Generating {file} model. ")