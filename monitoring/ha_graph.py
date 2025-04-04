from datetime import datetime, timedelta
import csv


def get_csv_data():
    day = datetime.today().strftime('%Y-%m-%d')
    path = f"logs/{day}.csv"
    with open(path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def last_x(mode):
    current_time = datetime.now()
    print(f'mode = {mode}')
    
    if mode == "1h":
        start_time = current_time - timedelta(hours=1)
        minute_range = [start_time]
        while start_time <= current_time:
            minute_range.append(start_time + timedelta(minutes=6))
            start_time = minute_range[-1]
    elif mode == "12h":
        start_time = current_time - timedelta(hours=12)
        minute_range = [start_time]
        while start_time <= current_time:
            minute_range.append(start_time + timedelta(hours=2))
            start_time = minute_range[-1]
    elif mode == "1j":
        start_time = current_time - timedelta(days=1)
        minute_range = [start_time]
        while start_time <= current_time:
            minute_range.append(start_time + timedelta(hours=3))
            start_time = minute_range[-1]
    elif mode == "1w":
        start_time = current_time - timedelta(days=7)
        minute_range = [start_time]
        while start_time <= current_time:
            minute_range.append(start_time + timedelta(days=1))
            start_time = minute_range[-1]
    
    else :
        start_time = current_time - timedelta(minutes=15)
        minute_range = [start_time]
        while start_time <= current_time:
            minute_range.append(start_time + timedelta(minutes=1))
            start_time = minute_range[-1]
        
    return minute_range


def ha_last_min(db, mode):
    data = {"labels": [], "ips": {}}
    minute_range = last_x(mode)  # Assuming last_x() is correctly defined elsewhere
    ips = db.get_ip_time_range(minute_range[0], minute_range[-1])
    for i in range(0, len(minute_range) - 1):
        # Append the formatted time range to the labels list
        data['labels'].append(minute_range[i].strftime("%m-%d %H:%M"))
        for ip in ips:
            nbr_packets = db.get_packets_nbr_time_range(minute_range[i], minute_range[i + 1], ip)
            if ip not in data['ips']:
                data['ips'][ip] = []  # Initialize the list if the IP is not present
                
            data['ips'][ip].append(int(nbr_packets))  # Append the packet count for this time slot

    print(f"data : {data}")
    return data