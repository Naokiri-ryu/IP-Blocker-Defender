import time, config
import os

class C:
    YELLOW="\033[93m"; END="\033[0m"

def monitor():
    

    if not os.path.exists(config.APP_LOG):
        open(config.APP_LOG, "w").close()

    with open(config.APP_LOG, "r") as f:
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            ts = time.strftime("%H:%M:%S")
            print(f"{C.YELLOW}[{ts}] APP EVENT {line.strip()}{C.END}")

if __name__ == "__main__":
    monitor()

def main():
    print("🟢 Application Event Monitor started")
    monitor()

if __name__ == "__main__":
    main()
