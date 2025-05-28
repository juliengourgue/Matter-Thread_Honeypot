from datetime import datetime, timedelta
import csv

def get_csv_data():
    """
    Reads CSV data from the current day's log file.
    """
    day = datetime.today().strftime('%Y-%m-%d')
    path = f"logs/{day}.csv"
    with open(path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def last_x(mode):
    """
    Returns a list of timestamps for the last X time period (1 hour, 12 hours, 1 day, 1 week).
    Ensures the current time is always included in the range.
    """
    current_time = datetime.now().replace(second=0, microsecond=0)
    minute_range = []
    if mode == "1h":
        start_time = current_time - timedelta(hours=1)
        minute_range = [start_time + timedelta(minutes=i) for i in range(0, 61, 1)]
    
    elif mode == "12h":
        start_time = current_time - timedelta(hours=12)
        minute_range = [start_time + timedelta(minutes=i*5) for i in range(0, 145, 5)]
    
    elif mode == "1j":
        start_time = current_time - timedelta(days=1)
        minute_range = [start_time + timedelta(minutes=i*15) for i in range(0, 97, 15)]
    
    elif mode == "1w":
        start_time = current_time - timedelta(days=7)
        start_time = start_time.replace(hour=0, minute=0)
        minute_range = [start_time + timedelta(days=i) for i in range(0, 8)]
    
    else:
        start_time = current_time - timedelta(minutes=15)
        minute_range = [start_time + timedelta(minutes=i) for i in range(0, 16)]
    
    if minute_range[-1] < current_time:
        minute_range.append(current_time)
    minute_range.append(current_time+timedelta(minutes=1))

    return minute_range

def ha_last_min(db, mode):
    """
    Fetches the packet data for the last X minutes, hours, days, or week and structures it for graphing.
    """
    data = {"labels": [], "ips": {}}

    minute_range = last_x(mode)  
    ips = db.get_ip_time_range(minute_range[0], minute_range[-1])

    # Loop through each time interval and fetch the packet count for each IP
    for i in range(len(minute_range)-1):
        
        data['labels'].append(minute_range[i].strftime("%m-%d %H:%M"))

        for ip in ips:
            nbr_packets = db.get_packets_nbr_time_range(minute_range[i], minute_range[i+1], ip)
            if ip not in data['ips']:
                data['ips'][ip] = []
                
            data['ips'][ip].append(int(nbr_packets))
    return data