from scapy.all import sniff
from scapy.layers.inet import IP
import time
from datetime import datetime
import threading
import os
from db import DB
from config import ha_ip, ha_port

class HANetworkMonitor:
    def __init__(self, sleep_time=60):
        self.sleep_time = sleep_time
        self.running = True
        self.sniffer_thread = None
        self.writer_thread = None
        self.packet_data = {}
        self.packet_data_lock = threading.Lock()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db = DB()

        self.last_write_time = time.time()
        self.current_minute = int(time.time() // 60)

        print("Starting network monitoring...")
        self.sniffer_thread = threading.Thread(target=self.run_sniffer)
        self.writer_thread = threading.Thread(target=self.write_packet_count_periodically)

        self.sniffer_thread.start()
        self.writer_thread.start()

    def packet_callback(self, packet):
        """
        Callback function to process packets and count packets per source IP.
        """
        if packet.haslayer(IP):
            src_ip = str(packet[IP].src)
            with self.packet_data_lock:
                if src_ip not in self.packet_data:
                    self.packet_data[src_ip] = 0
                self.packet_data[src_ip] += 1

    def write_packet_count_periodically(self):
        """
        This thread periodically writes the packet count for each IP for the past minute.
        """
        while self.running:
            time.sleep(self.sleep_time)

            current_minute = int(time.time() // 60)
            print(current_minute)
            if current_minute != self.current_minute:
                with self.packet_data_lock:
                    self.write_to_db(current_minute, self.packet_data)
                    self.packet_data.clear()
                self.current_minute = current_minute

    def write_to_db(self, current_minute, packet_data):
        """
        Write the packet_data of the current_minute to the database.
        """
        timestamp = datetime.fromtimestamp(current_minute * 60)
        timestamp = timestamp.replace(second=0, microsecond=0)
        print(f"Write to DB with timestamp : {timestamp}")
        try:
            for ip, count in packet_data.items():
                self.db.put_haIp(ip=ip, timestamp=timestamp, nbr_packets=count)
        except Exception as e:
            print(f"Error saving packet count to DB: {e}")

    def run_sniffer(self):
        """
        Runs the packet sniffer and processes the captured packets.
        """
        while self.running:
            sniff(prn=self.packet_callback, filter=f"ip dst {ha_ip} and tcp port {ha_port}",
                  timeout=self.sleep_time)

    def stop(self):
        """
        Stops the network monitor and gracefully terminates all threads.
        """
        print("Stopping network monitor...")
        self.running = False
        self.sniffer_thread.join()  # Wait for sniffer thread to complete
        self.writer_thread.join()   # Wait for writer thread to complete
        self.db.disconnect()
        print("Network monitor stopped.")

if __name__ == '__main__':
    monitor = HANetworkMonitor()
