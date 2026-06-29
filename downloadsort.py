import os
import json
import shutil

VERSION = "1.0.0"


# ---------------------------
# Config
# ---------------------------

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_downloads_folder(config):
    path = config.get("downloads_folder")

    if path and os.path.exists(path):
        return path

    return os.path.join(os.path.expanduser("~"), "Downloads")


# ---------------------------
# UI
# ---------------------------

def banner():
    print("=" * 50)
    print("             DownloadSort")
    print(f"                v{VERSION}")
    print("=" * 50)
    print()


def log(msg):
    print(msg)


# ---------------------------
# Setup folders
# ---------------------------

def create_folders(base_path, file_types):
    for folder in file_types.keys():
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)


# ---------------------------
# File utilities
# ---------------------------

def get_category(file_name, file_types):
    file_name = file_name.lower()

    for category, extensions in file_types.items():
        if file_name.endswith(tuple(extensions)):
            return category

    return None


def unique_filename(folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1

    new_name = filename

    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name} ({counter}){ext}"
        counter += 1

    return new_name


# ---------------------------
# Core engine
# ---------------------------

def organise_files(downloads, file_types):
    moved = 0

    for item in os.listdir(downloads):
        source = os.path.join(downloads, item)

        if not os.path.isfile(source):
            continue

        category = get_category(item, file_types)

        if category:
            target_folder = os.path.join(downloads, category)

            new_name = unique_filename(target_folder, item)
            destination = os.path.join(target_folder, new_name)

            shutil.move(source, destination)

            log(f"✓ Moved {item} → {category}")
            moved += 1

    return moved


# ---------------------------
# Main
# ---------------------------

def main():
    banner()

    print("Loading configuration...")
    config = load_config()
    print("✔ Configuration loaded\n")

    downloads = get_downloads_folder(config)

    print("Checking folders...")
    create_folders(downloads, config["file_types"])

    print("\nOrganising files...\n")
    moved = organise_files(downloads, config["file_types"])

    print("\nReady.")
    print(f"Files moved: {moved}")


if __name__ == "__main__":
    main()