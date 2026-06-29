import os
import json
import shutil
import time
import argparse
from datetime import datetime
from send2trash import send2trash

VERSION = "1.2.0"


# ---------------------------
# CONFIG
# ---------------------------

def load_config():
    default_config = {
        "file_types": {},
        "ignore_files": [".ini", ".tmp", ".part"],
        "ignore_names": ["desktop.ini", "thumbs.db"],
    }

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            user_config = json.load(f)
    except Exception:
        user_config = {}

    # merge safely
    for key, value in default_config.items():
        user_config.setdefault(key, value)

    if "file_types" not in user_config or not user_config["file_types"]:
        raise ValueError("Config missing 'file_types'")

    return user_config


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

    parser.add_argument("--path", help="Target folder")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--no-recycle", action="store_true", help="Disable recycle bin")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    return parser.parse_args()


# ---------------------------
# LOGGING (FILE BASED)
# ---------------------------

def setup_logger(base_path):
    log_dir = os.path.join(base_path, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "downloadsort.log")

    return log_file


def log(message, log_file, verbose=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    if verbose:
        print(line)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------------------
# SETUP
# ---------------------------

def create_folders(base_path, file_types):
    for folder in file_types.keys():
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)


# ---------------------------
# FILTERING
# ---------------------------

def should_ignore(file_name, config):
    if file_name.startswith("~$"):
        return True

    if file_name.lower() in config["ignore_names"]:
        return True

    for ext in config["ignore_files"]:
        if file_name.lower().endswith(ext):
            return True

    return False


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

def organise_files(downloads, config, args, log_file, summary):
    files = os.listdir(downloads)

    for item in files:
        source = os.path.join(downloads, item)

        if not os.path.isfile(source):
            continue

        if should_ignore(item, config):
            continue

        category = get_category(item, config["file_types"])

        try:
            if category:
                target_folder = os.path.join(downloads, category)
                new_name = unique_filename(target_folder, item)
                destination = os.path.join(target_folder, new_name)

                if args.dry_run:
                    print(f"[DRY RUN] {item} → {category}")
                else:
                    shutil.move(source, destination)

                summary[category] += 1

            else:
                if args.dry_run:
                    print(f"[DRY RUN] Recycle {item}")
                else:
                    if args.no_recycle:
                        os.remove(source)
                    else:
                        send2trash(source)

                summary["recycled"] += 1

        except Exception as e:
            summary["errors"] += 1
            log(f"ERROR {item}: {e}", log_file, args.verbose)


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

    print("\nDownloadSort v1.2.0\n")

    config = load_config()
    downloads = get_downloads_folder(config, args.path)

    log_file = setup_logger(downloads)

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

    organise_files(downloads, config, args, log_file, summary)

    print_summary(summary, start_time)


if __name__ == "__main__":
    main()