# Music Organizer

## Overview
This Music Organizer is a Python-based application that organizes and deduplicates music files based on metadata. It provides a GUI for ease of use and supports recursive file organization. The application utilizes the `mutagen` library to extract metadata and organize files into a structured folder hierarchy.

## Features
- Organizes music files by **Artist**, **Album**, and **Genre**.
- Renames files to a standard format: `Artist - Title.ext`.
- Removes duplicate music files based on MD5 hash comparison.
- Supports multiple file formats, including **MP3, FLAC, M4A, WAV, and OGG**.
- Provides a graphical user interface (GUI) using **Tkinter**.
- Allows optional recursive file processing.

## Installation
### Prerequisites
Ensure you have Python installed (version 3.7+ recommended). You also need to install the required dependencies:


pip install mutagen


## Usage
### Running the Application
Run the script using the following command:

python musicorganizer.py


### GUI Usage
1. **Select a Music Folder**: Click the "Browse" button to select the directory containing your music files.
2. **Enable/Disable Recursive Processing**: Check the "Include subdirectories" option if you want to process files within subdirectories.
3. **Organize Music**: Click the "Organize Music" button to start sorting your music files.
4. **Deduplicate Music**: Click the "Deduplicate Music" button to remove duplicate files.
5. The log window will display the status and progress of each operation.

### Command-line Usage
If you prefer to use it without the GUI, modify and run the script directly:

organize_music_files("/path/to/music", recursive=True)
deduplicate_music("/path/to/music", recursive=True)


## File Organization Structure
The script organizes files into the following structure:

Music Folder/
 ├── Genre/
 │   ├── Artist/
 │   │   ├── Album/
 │   │   │   ├── Artist - Title.mp3
 │   │   │   ├── Artist - Title (1).mp3  # If duplicate exists

If metadata is missing, files are placed in `Unknown Genre`, `Unknown Artist`, or `Singles` folders.

## Duplicate Detection
- The script calculates an **MD5 hash** for each file and removes duplicates if an identical hash is found.
- Deleted duplicates are logged for reference.

## Limitations
- Files without metadata are placed in default folders (`Unknown Artist`, `Unknown Genre`, etc.).
- The deduplication process only removes exact file duplicates, not similar tracks.

## License
This project is licensed under the **MIT License**. Feel free to modify and distribute as needed.

## Acknowledgments
- Developed using **Python 3** and **Tkinter**.
- Metadata processing via the **mutagen** library.

## Contact
For questions or improvements, feel free to contribute or reach out!

