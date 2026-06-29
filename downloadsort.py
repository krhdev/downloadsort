import os
import json
import shutil
import time
import argparse
from datetime import datetime
from send2trash import send2trash

VERSION = "1.1.0"


# ---------------------------
# CONFIG
# ---------------------------

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_downloads_folder(config, override_path=None):
    if override_path:
        return override_path

    path = config.get("downloads_folder")

    if path and os.path.exists(path):
        return path

    return os.path.join(os.path.expanduser("~"), "Downloads")


# ---------------------------
# CLI
# ---------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="DownloadSort CLI")

    parser.add_argument("--path", help="Target folder (default: Downloads)")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions only")
    parser.add_argument("--no-recycle", action="store_true", help="Disable recycle bin")
    parser.add_argument("--verbose", action="store_true", help="Show detailed logs")

    return parser.parse_args()


# ---------------------------
# LOGGING
# ---------------------------

def log(msg, verbose=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] {msg}"

    if verbose:
        print(line)
    else:
        print(msg)


# ---------------------------
# SETUP
# ---------------------------

def create_folders(base_path, file_types):
    for folder in file_types.keys():
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)


# ---------------------------
# HELPERS
# ---------------------------

def get_category(file_name, file_types):
    lower = file_name.lower()

    for category, extensions in file_types.items():
        if lower.endswith(tuple(extensions)):
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
# ENGINE
# ---------------------------

def organise_files(downloads, file_types, args, summary):
    for item in os.listdir(downloads):
        source = os.path.join(downloads, item)

        if not os.path.isfile(source):
            continue

        category = get_category(item, file_types)

        try:
            if category:
                target_folder = os.path.join(downloads, category)
                new_name = unique_filename(target_folder, item)
                destination = os.path.join(target_folder, new_name)

                if args.dry_run:
                    print(f"[DRY RUN] Move: {item} → {category}")
                else:
                    shutil.move(source, destination)

                summary[category] += 1

            else:
                if args.dry_run:
                    print(f"[DRY RUN] Recycle: {item}")
                else:
                    if args.no_recycle:
                        os.remove(source)
                    else:
                        send2trash(source)

                summary["recycled"] += 1

        except Exception as e:
            summary["errors"] += 1
            print(f"[ERROR] {item}: {e}")


# ---------------------------
# SUMMARY
# ---------------------------

def print_summary(summary, start_time):
    print("\n" + "=" * 40)
    print("Summary")
    print("=" * 40)

    for k, v in summary.items():
        print(f"{k:<15} {v}")

    print("\nTime:", round(time.time() - start_time, 2), "seconds")


# ---------------------------
# MAIN
# ---------------------------

def main():
    start_time = time.time()
    args = parse_args()

    print("\nDownloadSort v1.1.0\n")

    config = load_config()
    downloads = get_downloads_folder(config, args.path)

    create_folders(downloads, config["file_types"])

    summary = {
        "PDFs": 0,
        "Images": 0,
        "Installations": 0,
        "Archives": 0,
        "Documents": 0,
        "Spreadsheets": 0,
        "Presentations": 0,
        "Videos": 0,
        "Music": 0,
        "Code": 0,
        "recycled": 0,
        "errors": 0
    }

    organise_files(downloads, config["file_types"], args, summary)

    print_summary(summary, start_time)


if __name__ == "__main__":
    main()