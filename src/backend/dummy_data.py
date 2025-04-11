# Generate valid dummy data for graphs with time tracking

import math
import random
import datetime
from datetime import timedelta

bpm_data = []
spo2_data = []
time_data = []
ecg_data = []  # Added ECG data list for storage
last_get_times = {
    'bpm': None,
    'spo2': None,
    'time': None,
    'ecg': None  # Added ECG to time tracking
}

def get_bpm():
    last_get_times['bpm'] = datetime.datetime.now()
    return bpm_data

def get_spo2():
    last_get_times['spo2'] = datetime.datetime.now()
    return spo2_data

def get_time():
    last_get_times['time'] = datetime.datetime.now()
    return time_data

def get_ecg():
    last_get_times['ecg'] = datetime.datetime.now()
    return ecg_data

def get_time_since_last(metric):
    if metric not in last_get_times or last_get_times[metric] is None:
        return None
    return datetime.datetime.now() - last_get_times[metric]

def fake_data_generator():
    #Get last BPM or use initial value if empty
    last_bpm = bpm_data[-1] if bpm_data else 80
    
    #Generate new BPM that's within ±5 of last BPM, but locked between 60-100
    bpm_change = random.uniform(-5, 5)
    curr_bpm = max(60, min(100, last_bpm + bpm_change))
    
    #Generate other data as before
    spo2_change = random.uniform(-1, 1)
    curr_spo2 = max(95, min(100, math.floor(random.uniform(95, 100)) + spo2_change))
    curr_time = datetime.datetime.now()

    #Generate simple ECG data
    curr_ecg = [math.sin(2 * math.pi * i/50) + random.uniform(-0.1, 0.1) for i in range(100)]

    bpm_data.append(curr_bpm)
    spo2_data.append(curr_spo2)
    time_data.append(curr_time)
    ecg_data.append(curr_ecg)

    return {
        'bpm_data': bpm_data,
        'spo2_data': spo2_data,
        'time_data': time_data,
        'ecg_data': ecg_data,
        'time_since_last_bpm': get_time_since_last('bpm'),
        'time_since_last_spo2': get_time_since_last('spo2'),
        'time_since_last_time': get_time_since_last('time'),
        'time_since_last_ecg': get_time_since_last('ecg')
    }
# Generate static JSON data when run directly
if __name__ == "__main__":
    import json
    import os

    # Generate 15 data points
    for _ in range(15):
        fake_data_generator()
    
    # Format data for JSON
    output_data = {
        'bpm_data': get_bpm(),
        'spo2_data': get_spo2(),
        'time_data': [dt.strftime('%H:%M:%S') for dt in get_time()],
        'ecg_data': get_ecg()  # Include ECG data in output
    }
    
    # Save to frontend directory
    output_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dummy_data.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=4)
        print(f"Data saved to {output_path}")
    except IOError as e:
        print(f"Error: {e}")

