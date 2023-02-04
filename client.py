from subprocess import Popen
from psutil import process_iter

def check_client(process_name):
    found = False
    print(f"🟧 Checking if {process_name} is running...")
    for process in process_iter():
        if process_name in process.name():
            found = True
            break
    if found:
        print(f"🟩 {process_name} is running.")
    else:
        print(f"🟥 {process_name} is not running.")
    return found

def start_client(process_name, process_path):
    found = check_client(process_name)

    if not found:
        print(f"🟨 Starting {process_name}...")
        Popen(process_path)
        print(f"🟧 Waiting for {process_name} to start...")
        while not found:
            for process in process_iter():
                if process_name in process.name():
                    print(f"🟩 {process_name} started.")
                    found = True
                    break