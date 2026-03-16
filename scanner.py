import socket
import threading
from datetime import datetime

print("="*50)
print("TCP PORT SCANNER")
print("="*50)

target = input("Enter target host: ")
start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname resolve nahi ho paya")
    exit()

print(f"\nScanning Target: {target_ip}")
print(f"Start Time: {datetime.now()}")
print("-"*50)

lock = threading.Lock()

log_file = open("scan_results.txt", "w")

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target_ip, port))

        with lock:
            if result == 0:
                msg = f"Port {port}: OPEN"
            else:
                msg = f"Port {port}: CLOSED"

            print(msg)
            log_file.write(msg + "\n")

        s.close()

    except socket.timeout:
        with lock:
            msg = f"Port {port}: TIMEOUT"
            print(msg)
            log_file.write(msg + "\n")

threads = []

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

log_file.close()

print("\nScanning Completed")