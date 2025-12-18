# ================= NETWORK =================
INTERFACE = "Wi-Fi"     # cek dengan get_if_list()
SERVER_IP = "192.168.110.201"

# ================= LIMIT ===================
SYN_LIMIT = 100
UDP_LIMIT = 200
HTTP_LIMIT = 80
BLOCK_DURATION = 120

# ================= PATH ====================
APACHE_LOG = r"C:\xampp\apache\logs\access.log"
APP_LOG = r"C:\xampp\htdocs\app_events.log"

# ================= MODE ====================
ENABLE_FIREWALL = True
ENABLE_QOS = True
QOS_WINDOW = 10  

