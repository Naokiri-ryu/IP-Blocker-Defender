import subprocess
import time
import sys
import os

class C:
    CYAN="\033[96m"; BOLD="\033[1m"; END="\033[0m"
    GREEN="\033[92m"

def launch_new_console(script_name):
    """Membuka jendela CMD baru dan menjalankan script python"""
    print(f"🚀 Launching {script_name}...")
    # Perintah 'start' adalah perintah Windows untuk membuka window baru
    # 'cmd /k' artinya window tetap terbuka setelah script selesai (agar bisa lihat error)
    subprocess.Popen(f'start cmd /k "python {script_name}"', shell=True)

if __name__ == "__main__":
    # Bersihkan layar
    os.system("cls")
    
    print(f"{C.BOLD}{C.CYAN}")
    print("==========================================")
    print("   🛡️  HYBRID DEFENDER CONTROL CENTER")
    print("==========================================")
    print(f"{C.END}")
    print("Sistem akan membuka 4 jendela terpisah:")
    print(f"1. {C.GREEN}Hybrid Defender Core{C.END} (Firewall & Traffic)")
    print(f"2. {C.GREEN}Apache HTTP Monitor{C.END} (Web Log)")
    print(f"3. {C.GREEN}App Event Monitor{C.END} (Login/Upload)")
    print(f"4. {C.GREEN}QoS Network Monitor{C.END} (Latency/Jitter/Loss)")
    print("\nTekan Enter untuk memulai semua modul...")
    input()

    # Eksekusi satu per satu
    launch_new_console("hybrid_defender.py")
    time.sleep(1) # Jeda sedikit biar window tidak bertumpuk kacau
    
    launch_new_console("apache_monitor.py")
    time.sleep(0.5)
    
    launch_new_console("app_event_monitor.py")
    time.sleep(0.5)

    launch_new_console("qos_monitor.py")

    print(f"\n{C.BOLD}✅ SEMUA MODUL BERJALAN.{C.END}")
    print("Tutup jendela launcher ini jika sudah selesai.")