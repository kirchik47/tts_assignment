import os

# Path to the directory containing the segments
directory = "data/task1/wavs"

# Iterate over all the files in the directory
for filename in os.listdir(directory):
    # Check if the file is an mp3
    if filename.endswith(".mp3"):
        # Form the old and new file names
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, filename.replace(".mp3", ".wav"))
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f"Renamed: {old_file} -> {new_file}")