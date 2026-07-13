# DownloadSort

A lightweight Python CLI tool that automatically organises your Downloads folder into structured categories.

---

## 🚀 Features

- Automatic file categorisation
- Configurable file type mapping
- Safe file moving (no destructive deletes)
- Recycle fallback for unknown files
- Logging of all actions
- Installable CLI tool

---

## 📦 Installation

```bash
pip install -e .

or Install from GitHub:
git clone https://github.com/krhdev/downloadsort.git
cd downloadsort
pip install -e . 

```
--- 

## ⚙️ Usage

Run default sorting:

downloadsort

Specify a folder:

```downloadsort --path "C:\Users\YourName\Downloads"```

---

## 📁 Output Structure

```
Downloads/
├── PDFs/
├── Images/
├── Installations/
├── Archives/
├── Documents/
├── Spreadsheets/
├── Presentations/
├── Videos/
├── Music/
├── Code/
```
--- 

## ⚙️ Configuration

All file rules are controlled via config.json.

Example
```{
  "file_types": {
    "Images": [".png", ".jpg", ".jpeg"],
    "PDFs": [".pdf"],
    "Installations": [".exe", ".msi"]
  }
}
```
--- 

## 🛠 Requirements
Python 3.10+
Windows/Linux/MacOS

## Selling this on etsy
link tbd soon

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Version](https://img.shields.io/badge/version-v1.2.0-green)

