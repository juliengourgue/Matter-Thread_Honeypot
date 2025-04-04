from scapy.all import sniff
from scapy.layers.inet import IP
import time
from datetime import datetime
import threading
from db import DB
import csv
import os
from config import ha_ip, ha_port

class HA_listen():
    startTime = -1
    sleep_time = 60
    running = True
    sniffer_thread = None
    shared_temp_csv = []
    ip_packets = {}
    
    def __init__(self):
        print("Starting network monitoring...")
        self.sniffer_thread = threading.Thread(target=self.run_sniffer)
        self.writter_thread = threading.Thread(target=self.ha_ip_mysql)

        self.sniffer_thread.start()
        self.writter_thread.start()
    
    def packet_callback(self,packet):
        print("Packet received ....")
        if packet.haslayer('IP'):
            if str(packet[IP].src) not in self.ip_packets.keys():
                self.ip_packets[str(packet[IP].src)] = 0
            self.ip_packets[str(packet[IP].src)] += 1
        
    def ha_ip_mysql(self):
        db = DB()
        while self.running:
            if len(self.shared_temp_csv) > 0:
                path = self.shared_temp_csv.pop(0)
                with open(path, 'r') as f:
                    csvFile = csv.reader(f)
                    for lines in csvFile:
                        db.put_haIp(ip=lines[1], timestamp=datetime.fromtimestamp(float(lines[0])), nbr_packets=lines[2])
                os.remove(path)
        db.disconnect()
            
    def save(self):
        path = f"monitoring/logs/temp_{self.startTime}.csv"
        with open(path, mode='+a') as f:
            for ip in self.ip_packets.keys() :
                f.write(f"{self.startTime},{ip},{self.ip_packets[ip]}\n")
        self.shared_temp_csv.append(path)

    def run_sniffer(self):
        while self.running:
            with open("monitoring/stop_signal.txt", "r") as file:
                signal = file.read().strip()
                if signal == "STOP":
                    self.stop()
                    break;
            self.ip_packets = {}
            self.startTime = time.time()
            sniff(prn=self.packet_callback, filter=f"ip dst {ha_ip} and tcp port {self.ha_port}", timeout=self.sleep_time)
            self.save()
            
    def stop(self):
        self.running = False  # Stop the loop
        print("HA Sniffer stopped")        


if __name__ == '__main__':
    ha = HA_listen()