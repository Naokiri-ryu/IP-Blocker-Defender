import time, subprocess, re, statistics, os
import config

class C:
    CYAN="\033[96m"; GREEN="\033[92m"; RED="\033[91m"; YELLOW="\033[93m"
    BOLD="\033[1m"; END="\033[0m"

# History untuk menghitung Jitter
latency_history = []
loss_count = 0
total_pings = 0

def get_qos_data(target_ip):
    global loss_count, total_pings
    
    # Perintah Ping Windows (hanya 1 paket, timeout 1000ms)
    command = f"ping {target_ip} -n 1 -w 1000"
    
    try:
        # Jalankan ping dan tangkap outputnya
        output = subprocess.check_output(command, shell=True).decode()
        total_pings += 1
        
        # Cari angka 'time=xxms' menggunakan Regex
        match = re.search(r"time[=<](\d+)ms", output)
        
        if match:
            latency = int(match.group(1))
            return latency
        else:
            # Jika tidak ada "time=", berarti RTO/Loss
            loss_count += 1
            return None
            
    except subprocess.CalledProcessError:
        loss_count += 1
        total_pings += 1
        return None

def monitor():
    os.system("title QoS MONITORING SYSTEM")
    print(f"{C.BOLD}{C.CYAN}📡 QoS MONITORING STARTED...{C.END}")
    print(f"Target: {config.SERVER_IP} (Self/Gateway Analysis)\n")
    print(f"{'TIMESTAMP':<10} | {'LATENCY (ms)':<15} | {'JITTER (ms)':<15} | {'LOSS (%)':<10} | {'STATUS'}")
    print("-" * 75)

    last_latency = 0

    while True:
        ts = time.strftime("%H:%M:%S")
        
        # Lakukan Ping
        current_latency = get_qos_data(config.SERVER_IP) # Bisa diganti IP Gateway jika mau
        
        # Hitung Jitter (Selisih absolut latensi sekarang vs sebelumnya)
        if current_latency is not None:
            jitter = abs(current_latency - last_latency) if last_latency > 0 else 0
            last_latency = current_latency
            lat_str = f"{current_latency} ms"
            jit_str = f"{jitter} ms"
            status = f"{C.GREEN}EXCELLENT{C.END}"
            
            # Logika Warna & Status
            if current_latency > 100 or jitter > 50:
                status = f"{C.YELLOW}DEGRADED{C.END}"
            if current_latency > 500:
                status = f"{C.RED}CRITICAL{C.END}"
                
        else:
            lat_str = f"{C.RED}TIMEOUT{C.END}"
            jit_str = "-"
            status = f"{C.RED}DOWN{C.END}"
            jitter = 0

        # Hitung Packet Loss
        if total_pings > 0:
            loss_pct = (loss_count / total_pings) * 100
        else:
            loss_pct = 0.0

        # Tampilkan
        print(f"{ts:<10} | {lat_str:<15} | {jit_str:<15} | {loss_pct:.1f}%{'':<5} | {status}")
        
        time.sleep(1)

if __name__ == "__main__":
    monitor()