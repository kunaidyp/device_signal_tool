from pathlib import Path
import read_file
from devices import *


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input."""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    file_contents = read_file.read_input_file(input_file_path)  # check if file exists
    contents_dict = read_file.append_contents(file_contents)  # returns dictionary of lists organizing alert info
    length = contents_dict["length"]
    time = TimeLine(contents_dict["events"], contents_dict["length"], contents_dict["devices"])

    while True:
        result = time.pop_event()
        if not result:
            break
    print(f"@{length}: END")


if __name__ == '__main__':
    main()