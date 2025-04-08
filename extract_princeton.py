from pathlib import Path
import shutil

def find_and_copy_princeton_files(directory, destination="/tmp/foo"):
    """
    Recursively finds all files in the given directory (including subdirectories)
    that start with 'princeton' and copies them to the specified destination.

    :param directory: The root directory to search in.
    :param destination: The directory where files will be copied. Default is '/tmp/foo'.
    """
    source_directory = Path(directory)
    destination_directory = Path(destination)
    destination_directory.mkdir(parents=True, exist_ok=True)  # Ensure destination exists

    for file in source_directory.rglob("princeton*"):
        if file.is_file():
            shutil.copy2(file, destination_directory / file.name)  # Copy file

# Example usage:
# directory_path = "/path/to/search"
# find_and_copy_princeton_files(directory_path)



pod_file_dir = Path("pod") / Path("file")
princeton_files = pod_file_dir.rglob("princeton*")

def main():
    pod_file_dir = Path("/Users/wulfmanc/gh/pulibrary/Google_Books/pod/file")
    find_and_copy_princeton_files(pod_file_dir)


if __name__ == "__main__":
    main()
