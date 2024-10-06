import threading


clients_lock = threading.Lock()
clients = set()

id_clients_lock = threading.Lock()
id_clients = {}

ip_clients_lock = threading.Lock()
ip_clients = {}