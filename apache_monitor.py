import time, re, os
import config

class C:
    MAGENTA="\033[95m"; END="\033[0m"

def monitor():
    with open(config.APACHE_LOG, "r", encoding="utf8", errors="ignore") as f:
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            m = re.search(r'(\d+\.\d+\.\d+\.\d+).*"(GET|POST) (.*?) HTTP.*" \d+ (\d+)', line)
            if not m:
                continue

            ip, method, path, size = m.groups()
            ext = os.path.splitext(path)[1]
            ts = time.strftime("%H:%M:%S")

            action = "DOWNLOAD" if method=="GET" else "UPLOAD/LOGIN"
            print(f"{C.MAGENTA}[{ts}] HTTP {method} {ip} {path} | {size}B | {ext} | {action}{C.END}")

if __name__ == "__main__":
    monitor()

def main():
    print("🟢 Apache Monitor started")
    monitor()

if __name__ == "__main__":
    main()
