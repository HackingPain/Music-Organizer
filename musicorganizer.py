import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from mutagen import File as MutagenFile

# Allowed file extensions
ALLOWED_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".ogg"}

def sanitize(s):
    """Remove characters that are problematic in file/folder names."""
    return "".join(c for c in s if c.isalnum() or c in " -_").strip()

def get_metadata(file_path):
    """
    Read metadata from a music file using mutagen.
    Returns a dictionary with artist, title, album, and genre.
    """
    try:
        audio = MutagenFile(file_path, easy=True)
        if not audio:
            return {}
        artist = audio.get("artist", ["Unknown Artist"])[0]
        title = audio.get("title", ["Unknown Title"])[0]
        album = audio.get("album", ["Singles"])[0]
        genre = audio.get("genre", ["Unknown Genre"])[0]
        return {
            "artist": sanitize(artist) if artist else "Unknown Artist",
            "title": sanitize(title) if title else "Unknown Title",
            "album": sanitize(album) if album else "Singles",
            "genre": sanitize(genre) if genre else "Unknown Genre"
        }
    except Exception:
        return {
            "artist": "Unknown Artist",
            "title": "Unknown Title",
            "album": "Singles",
            "genre": "Unknown Genre"
        }

def organize_music_files(source_dir, recursive=False, logger=print):
    """
    Organize music files by reading their metadata. Files are renamed to 
    "Artist - Title.ext" and moved into a folder structure: 
    source_dir/Genre/Artist/Album (or "Singles" if album is missing).
    """
    logger("Starting organization...")
    # Gather music files
    files_to_process = []
    if recursive:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                    files_to_process.append(os.path.join(root, file))
    else:
        for file in os.listdir(source_dir):
            if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                files_to_process.append(os.path.join(source_dir, file))
    
    logger(f"Found {len(files_to_process)} music files.")
    
    for file_path in files_to_process:
        metadata = get_metadata(file_path)
        artist = metadata.get("artist", "Unknown Artist")
        title = metadata.get("title", "Unknown Title")
        album = metadata.get("album", "Singles")
        genre = metadata.get("genre", "Unknown Genre")
        ext = os.path.splitext(file_path)[1].lower()
        
        # Standardize file name: "Artist - Title.ext"
        base_filename = f"{artist} - {title}"
        new_filename = f"{base_filename}{ext}"
        
        # Determine target folder: source_dir/Genre/Artist/Album
        target_dir = os.path.join(source_dir, genre, artist, album)
        os.makedirs(target_dir, exist_ok=True)
        
        target_path = os.path.join(target_dir, new_filename)
        count = 1
        # Avoid name collisions
        while os.path.exists(target_path):
            new_filename = f"{base_filename} ({count}){ext}"
            target_path = os.path.join(target_dir, new_filename)
            count += 1
        
        try:
            shutil.move(file_path, target_path)
            logger(f"Moved '{os.path.basename(file_path)}' to '{target_path}'")
        except Exception as e:
            logger(f"Error moving {file_path}: {e}")
    logger("Organization complete.")

def compute_file_hash(file_path, chunk_size=4096):
    """Compute MD5 hash for a given file."""
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None

def deduplicate_music(source_dir, recursive=True, logger=print):
    """
    Identify and remove duplicate music files based on their MD5 hash.
    """
    logger("Starting deduplication...")
    file_hashes = {}
    duplicates = []
    
    if recursive:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    file_hash = compute_file_hash(full_path)
                    if not file_hash:
                        continue
                    if file_hash in file_hashes:
                        duplicates.append(full_path)
                    else:
                        file_hashes[file_hash] = full_path
    else:
        for file in os.listdir(source_dir):
            if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                full_path = os.path.join(source_dir, file)
                file_hash = compute_file_hash(full_path)
                if not file_hash:
                    continue
                if file_hash in file_hashes:
                    duplicates.append(full_path)
                else:
                    file_hashes[file_hash] = full_path

    logger(f"Found {len(duplicates)} duplicate files.")
    for dup in duplicates:
        try:
            os.remove(dup)
            logger(f"Removed duplicate: {dup}")
        except Exception as e:
            logger(f"Error removing duplicate {dup}: {e}")
    logger("Deduplication complete.")

class MusicOrganizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ultimate Music Organizer")
        
        # Music folder selection
        self.dir_label = tk.Label(master, text="Select Music Folder:")
        self.dir_label.pack(pady=5)
        self.dir_entry = tk.Entry(master, width=60)
        self.dir_entry.pack(pady=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        # Recursive option
        self.recursive_var = tk.BooleanVar(value=True)
        self.recursive_checkbox = tk.Checkbutton(master, text="Include subdirectories", variable=self.recursive_var)
        self.recursive_checkbox.pack(pady=5)
        
        # Buttons for organization and deduplication
        self.organize_button = tk.Button(master, text="Organize Music", command=self.organize)
        self.organize_button.pack(pady=5)
        self.deduplicate_button = tk.Button(master, text="Deduplicate Music", command=self.deduplicate)
        self.deduplicate_button.pack(pady=5)
        
        # Log output area
        self.log_text = scrolledtext.ScrolledText(master, state="disabled", width=80, height=20)
        self.log_text.pack(pady=10)
    
    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select Music Folder")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)
    
    def organize(self):
        source_dir = self.dir_entry.get().strip()
        if not source_dir:
            messagebox.showerror("Error", "Please select a music folder.")
            return
        recursive = self.recursive_var.get()
        self.log(f"Starting organization in '{source_dir}' (recursive={recursive})...")
        organize_music_files(source_dir, recursive, logger=self.log)
        messagebox.showinfo("Complete", "Music organization complete!")
    
    def deduplicate(self):
        source_dir = self.dir_entry.get().strip()
        if not source_dir:
            messagebox.showerror("Error", "Please select a music folder.")
            return
        recursive = self.recursive_var.get()
        self.log(f"Starting deduplication in '{source_dir}' (recursive={recursive})...")
        deduplicate_music(source_dir, recursive, logger=self.log)
        messagebox.showinfo("Complete", "Deduplication complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicOrganizerGUI(root)
    root.mainloop()
