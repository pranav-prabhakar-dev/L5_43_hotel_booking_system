# Identified Issues

Line numbers refer to the original `hotel_booking_system.py`. Rows are ordered by severity: Bandit High and Medium first, then bugs, then style.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605) | Security – High | 58 | `os.system("echo ... " + filename)` passes the filename to a shell, so a crafted filename such as `x & del *` would run extra commands. | Removed the shell call and used `print()` to report the export. |
| Weak MD5 hash (Bandit B324) | Security – High | 47 | `hashlib.md5` is broken and should not be used to identify guests. | Switched to `hashlib.sha256`. |
| Use of `eval` (Bandit B307, Pylint W0123) | Security – Medium | 40–43 | `eval(rate_expr)` runs any text it is given as Python code. | Changed the function to take a numeric `multiplier` and compute `base_price * float(multiplier)`. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `booking_log=[]` is created once and shared by every call, so bookings leak between calls. The log was also never shown. | Default changed to `None` and a new list is created inside the function. `main()` now passes its own log and prints it. |
| Bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) | Bug / Security – Low | 24–27 | Every error, including typos and interrupts, was hidden, and cancelling an unknown room gave no feedback. | Replaced with an explicit check for the room. The function returns `False` for unknown rooms and `True` on success. |
| Hardcoded secret (Bandit B105) | Security – Low | 62, 70 | The admin token was in the source code and printed to the console. | Read from the `HOTEL_SECRET_KEY` environment variable. Only whether a key is set is printed, never its value. |
| Insecure random (Bandit B311) | Security – Low | 51 | `random` is predictable, so booking references could be guessed. | Used `1000 + secrets.randbelow(9000)`, which gives the same 1000–9999 range. |
| File not closed safely (Pylint R1732, W1514) | Bug | 55–57 | `open()`/`close()` leaks the file handle if `write()` fails, and the encoding depends on the platform. | Used a `with` block and `encoding="utf-8"`. |
| Unused variables (Pylint W0612, Flake8 F841) | Code smell | 31, 41 | `cleaning_deposit` was never used. `base_price` only appeared to be unused because it was referenced inside the `eval` string. | Removed `cleaning_deposit`. `base_price` is now used directly. |
| Unused import (Pylint W0611, Flake8 F401) | Style | 6 | `math` was imported but never used. | Removed the import. |
| `== None` comparison (Pylint C0121, Flake8 E711) | Style | 32 | Comparisons to `None` should use `is`. | Rewrote `check_room_status` to use `is not None`. |
| Overly complex if/else (Pylint R1703, R1705) | Style | 34–37 | An `if`/`else` that returns `True` or `False` can be a single expression. | Replaced with `return room is not None and not room["is_booked"]`. |
| Naming convention (Pylint C0103) | Style | 15 | `bookRoom` is camelCase, which breaks PEP 8. | Renamed to `book_room`. |
| Missing docstrings (Pylint C0116) | Style | 15–61 | None of the functions were documented. | Added a docstring to each function. |
| `%` string formatting, line too long (Pylint C0209, Flake8 E501) | Style | 19 | The 80-character line used old-style formatting. | Used an f-string, which also brings the line under 79 characters. |
| Missing final newline (Pylint C0304, Flake8 W292) | Style | 73 | The file did not end with a newline. | Added the trailing newline. |
| `main()` runs on import | Bug (not flagged by tools) | 73 | Importing the module ran the whole demo and wrote a file. | Wrapped the call in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.32/10 (22 messages) | 10.00/10 (0 messages) |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 7 issues | 0 issues |
