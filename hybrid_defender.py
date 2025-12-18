import time, threading, subprocess, os
from collections import defaultdict
from scapy.all import sniff, IP, TCP, UDP, conf
import config

os.system("color")

# MATIKAN PROMISCUOUS MODE (Agar XAMPP Aman)
conf.sniff_promisc = False

class C:
    RED="\033[91m"; GREEN="\033[92m"; BLUE="\033[94m"
    MAGENTA="\033[95m"; CYAN="\033[96m"; YELLOW="\033[93m"
    BOLD="\033[1m"; END="\033[0m"

# Reset stats setiap 1 detik
stats = defaultdict(lambda: {"syn":0,"udp":0,"last":time.time()})
blocked = {}
traffic_bytes = 0

# ============ FIREWALL ============
def block_ip(ip, reason):
    if ip in blocked or not config.ENABLE_FIREWALL:
        return
    # Jangan blokir diri sendiri atau server
    if ip == config.SERVER_IP or ip == "127.0.0.1": 
        return

    subprocess.run(
        f'netsh advfirewall firewall add rule name="BLOCK_PY_{ip}" dir=in action=block remoteip={ip}',
        shell=True, stdout=subprocess.DEVNULL
    )
    blocked[ip] = time.time() + config.BLOCK_DURATION
    # Tampilan Merah saat memblokir
    print(f"\n{C.RED}{C.BOLD}🛑 BLOCK {ip} | {reason}{C.END}\n")

def unblock_worker():
    while True:
        now = time.time()
        for ip in list(blocked):
            if now > blocked[ip]:
                subprocess.run(
                    f'netsh advfirewall firewall delete rule name="BLOCK_PY_{ip}"',
                    shell=True, stdout=subprocess.DEVNULL
                )
                del blocked[ip]
                print(f"{C.GREEN}✅ UNBLOCK {ip}{C.END}")
        time.sleep(1)

# ============ PACKET HANDLER (VISUAL VERSION) ============
def packet_handler(pkt):
    global traffic_bytes
    
    # Safety Check: Pastikan paket memiliki layer IP
    if IP not in pkt:
        return

    src = pkt[IP].src
    dst = pkt[IP].dst
    traffic_bytes += len(pkt)
    
    # Buat Timestamp untuk efek visual
    ts = time.strftime("%H:%M:%S")

    # Filter: Hanya proses paket yang menuju ke Server Kita (Biar tidak crash)
    if dst != config.SERVER_IP:
        return

    # Reset counter setiap 1 detik
    now = time.time()
    if now - stats[src]["last"] >= 1:
        stats[src].update({"syn":0,"udp":0,"last":now})

    # ---- TCP MONITOR (MATRIX STYLE) ----
    if TCP in pkt:
        # FIX ERROR 'int object is not iterable':
        # Kita paksa flags jadi string atau gunakan bitwise operation
        flags = pkt[TCP].flags
        
        # TAMPILAN VISUAL (Sesuai keinginanmu)
        # Ini akan membanjiri layar dengan teks hijau
        print(f"{C.GREEN}[{ts}] TCP {src} -> {dst} | Flags: {flags}{C.END}")

        # Deteksi SYN Flood (Menggunakan Bitwise 0x02 untuk SYN)
        # Ini lebih aman daripada mengecek string "S"
        if flags & 0x02:
            stats[src]["syn"] += 1
            if stats[src]["syn"] > config.SYN_LIMIT:
                block_ip(src, "TCP SYN Flood")

    # ---- UDP MONITOR ----
    elif UDP in pkt:
        stats[src]["udp"] += 1
        # Tampilan Biru untuk UDP
        print(f"{C.BLUE}[{ts}] UDP {src} -> {dst} | Len:{len(pkt)}{C.END}")
        
        if stats[src]["udp"] > config.UDP_LIMIT:
            block_ip(src, "UDP Flood")

# ============ STATUS MONITOR ============
def status_monitor():
    global traffic_bytes
    while True:
        time.sleep(1) 
        bw = (traffic_bytes * 8) / 1_000_000
        traffic_bytes = 0
        # Tampilkan status bandwidth
        if bw > 0.01:
            print(f"{C.CYAN}[STATUS] BW:{bw:.2f} Mbps | Blocked:{len(blocked)}{C.END}")

# ============ MAIN ============
def main():
    print(f"{C.BOLD}🛡️ HYBRID DEFENDER CORE ACTIVE (Visual Mode){C.END}")
    
    # Jalankan thread unblock & status
    t1 = threading.Thread(target=unblock_worker, daemon=True)
    t2 = threading.Thread(target=status_monitor, daemon=True)
    t1.start()
    t2.start()
    
    # Jalankan Sniffer
    # Filter "ip" memastikan kita hanya menangkap paket IPv4 yang valid
    sniff(iface=config.INTERFACE, prn=packet_handler, filter="ip", store=0)

if __name__ == "__main__":
    main()