import re
import subprocess
import sys
import unicodedata


def make_alpha_numeric(string: str) -> str:
    cleaned_string = ""
    for char in string:
        if char.isalnum():
            cleaned_string += char
    return cleaned_string


def remove_accents(text: str) -> str:
    normalized_text = unicodedata.normalize("NFKD", text)
    return "".join([c for c in normalized_text if not unicodedata.combining(c)])


def sanitize_filename(filename: str) -> str:
    filename = remove_accents(filename)
    filename = re.sub(r"[^\w\s-]", "", filename)
    filename = re.sub(r"[\s]+", "_", filename)
    return filename.strip()


def clear_terminal() -> None:
    if get_os_package_manager()[0] == "windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)


def get_os_package_manager() -> tuple:
    if sys.platform in ["win32", "win64"]:
        return "windows", "winget"
    elif sys.platform in ["linux"]:
        return "linux", "apt"


def verify_download_folders() -> None: ...
