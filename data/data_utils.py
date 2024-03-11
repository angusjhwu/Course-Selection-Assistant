import os


def save_list_to_file(lst: list, filename: str, verbose: bool = False) -> None:
    try:
        with open(filename, 'w') as file:
            for item in lst:
                file.write(f"{item}\n")
        if verbose:
            print(f"List saved to {filename}")
    except IOError as e:
        print(f"Error saving list to file: {e}")


def load_list_from_file(filename: str) -> list:
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except IOError as e:
        print(f"Error loading list from file: {e}")
        return []
