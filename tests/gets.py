# from typing import Literal
from requests import Response, get

# type Simple_URL = Literal["http://..."]


def main() -> None:
    home = "http://127.0.0.1:5000"
    get_notes = home + "/notes"

    notes: Response = get(url=get_notes)
    print(notes.json())

if __name__ == "__main__":
    main()