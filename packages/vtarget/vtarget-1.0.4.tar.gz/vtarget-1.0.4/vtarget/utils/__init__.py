import os as __os
from typing import Union

TEMP_DIR = __os.environ.get("TMPDIR")
if TEMP_DIR is None:
    TEMP_DIR = __os.environ.get("TEMP")
if TEMP_DIR is None:
    TEMP_DIR = __os.environ.get("TMP")
if TEMP_DIR is None:
    TEMP_DIR = "."


def dprint(*args, **kwargs):
    import traceback

    """
    Pre-pends the filename and linenumber to the print statement
    """
    try:
        stack = traceback.extract_stack()[:-1]
        last = stack[-1]

        # Handle different versions of the traceback module
        if hasattr(last, "filename"):
            _filename = last.filename.split("lib")
            filename = "lib".join(_filename[1:])[1:] if len(_filename) >= 2 else last.filename
            out_str = f"\t\033[90m{filename}:{last.lineno}\033[0m"
        else:
            _filename = last[0].split("lib")
            filename = "lib".join(_filename[1:])[1:] if len(_filename) >= 2 else last[0]
            out_str = f"\t\033[90m{filename}:{last[1]}\033[0m"

        # Prepend the filename and linenumber
        __builtins__["oldprint"](*args, out_str, **kwargs)
    except:
        __builtins__["oldprint"](*args, **kwargs)


def override():
    if "oldprint" not in __builtins__:
        __builtins__["oldprint"] = __builtins__["print"]

    __builtins__["print"] = dprint


def regpid(target: str = None):
    import os

    id = 0

    if target is None or len(target) == 0:
        vtarget_pids_path = os.path.join(TEMP_DIR, "vtarget-pids")

    else:
        vtarget_pids_path = os.path.join(TEMP_DIR, f"vtarget-{target}-pids")

    print(vtarget_pids_path)

    with open(vtarget_pids_path, "a+") as f:
        id = os.getpid()
        f.write(f"{id}\n")
    return id


def syspath():
    import sys

    if getattr(sys, "frozen", False):
        import os

        current_path = os.path.dirname(sys.executable)
        sys.path.insert(0, os.path.join(current_path, "python"))
        sys.path.insert(0, os.path.join(current_path, "python", "lib"))
        sys.path.insert(0, os.path.join(current_path, "python", "lib", "site-packages"))
        sys.path.insert(0, os.path.join(current_path, "python", "lib", "python3", "site-packages"))
        sys.path.insert(0, os.path.join(current_path, "python", "lib", "python3.10", "site-packages"))
        sys.path.insert(0, os.path.join(current_path, "python", "lib", "python3.11", "site-packages"))
        sys.path.insert(0, os.path.join(current_path, "python", "lib", "python3.12", "site-packages"))
        sys.path.insert(0, os.path.join(current_path, "python", "DLLs"))


__serial_number: Union[bytes, None] = None

def get_serial_number() -> Union[bytes, None]:
    global __serial_number
    if __serial_number is not None:
        return __serial_number
    
    import platform
    import subprocess
    import uuid

    os_type = platform.system()
    try:
        if os_type == "Windows":
            result = subprocess.check_output("wmic bios get serialnumber", shell=True)
            result = result.decode("utf-8").strip().split("\n")[1]
            __serial_number = result
            return result
        elif os_type == "Linux":
            result = subprocess.check_output("dmidecode -s system-serial-number", shell=True)
            result = result.decode("utf-8").strip()
            __serial_number = result
            return result
        elif os_type == "Darwin":
            result = subprocess.check_output("system_profiler SPHardwareDataType", shell=True)
            result = result.decode("utf-8").strip()
            lines = result.split("\n")
            serial_number_line = [line for line in lines if "Serial Number" in line][0]
            serial_number = serial_number_line.split(":")[-1].strip()
            __serial_number = serial_number
            return serial_number
        else:
            raise Exception(os_type)
    except:
        mac_address = hex(uuid.getnode()).replace("0x", "").upper()
        mac_address = ":".join(mac_address[i : i + 2] for i in range(0, 11, 2))
        __serial_number = f"Dirección MAC en uso: {mac_address}"
        return __serial_number


def normpath(path: str) -> str:
    import os

    parts = path.split(r"[\\\/]")

    return os.path.join(*parts)


def trace_error():
    import sys
    import traceback

    c, e, t = sys.exc_info()
    error = f"{c.__name__}: {e}"
    tb = [f"{s.filename}:{s.lineno}" for s in traceback.extract_tb(t)]
    return error, tb
