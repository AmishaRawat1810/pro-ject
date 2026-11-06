import sys


def get_file_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return input("Enter the file path: ")


def readFile():
    file_path = get_file_path()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print("\nFile read successfully.")
            return content
    except FileNotFoundError:
        print(
            f"\nError: The file at '{file_path}' could not be found. Please check and try again."
        )
        return None
    except Exception as e:
        print(f"\nUnexpected Error: '{e}'")
        return None

if __name__ == "__main__":
    text = readFile()
    if text:
        print("\nFile Content:\n", text)