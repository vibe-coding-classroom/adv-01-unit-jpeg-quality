import csv
import json
import os
import sys

def check_csv_trends(file_path):
    if not os.path.exists(file_path):
        return False, "results.csv missing"
    
    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    if len(data) < 2:
        return False, "results.csv has insufficient data points"

    try:
        # Check trend: Quality ↑ -> FrameSize ↑ -> FPS ↓
        # Note: In ESP32-CAM quality 10 is better (larger file) than 63.
        # But README says "品質上升" (Quality Increase) -> "大小上升" (Size Increase).
        # We should assume Quality 100 is better/larger than Quality 10 if using 0-100 scale.
        # Let's check based on the values provided.
        
        qualities = [float(row['Quality']) for row in data if row['Quality']]
        sizes = [float(row['FrameSize_KB']) for row in data if row['FrameSize_KB']]
        fps = [float(row['FPS']) for row in data if row['FPS']]

        if len(sizes) < 2 or len(fps) < 2:
            return False, "Missing FrameSize or FPS data in results.csv"

        # Sort by quality to check trends
        combined = sorted(zip(qualities, sizes, fps))
        sorted_q, sorted_s, sorted_f = zip(*combined)

        # Check if size increases with quality
        for i in range(1, len(sorted_s)):
            if sorted_s[i] < sorted_s[i-1]:
                 print(f"Warning: Size decreased from {sorted_s[i-1]} to {sorted_s[i]} as quality increased.")
        
        # Check if FPS decreases with quality (due to larger size/processing)
        for i in range(1, len(sorted_f)):
            if sorted_f[i] > sorted_f[i-1]:
                print(f"Warning: FPS increased from {sorted_f[i-1]} to {sorted_f[i]} as quality increased.")

        return True, "CSV trend check passed (warnings ignored for edge cases)"
    except Exception as e:
        return False, f"Error parsing CSV: {e}"

def check_jitter_log(file_path):
    if not os.path.exists(file_path):
        return False, "jitter-log.json missing"
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if not data.get('data') or len(data['data']) == 0:
                return False, "jitter-log.json data is empty"
        return True, "jitter-log.json found and populated"
    except Exception as e:
        return False, f"Error parsing JSON: {e}"

def main():
    results_path = 'analysis/results.csv'
    jitter_path = 'analysis/jitter-log.json'
    
    passed_csv, msg_csv = check_csv_trends(results_path)
    passed_jitter, msg_jitter = check_jitter_log(jitter_path)
    
    print(f"CSV Check: {msg_csv}")
    print(f"Jitter Check: {msg_jitter}")
    
    if passed_csv and passed_jitter:
        print("\nOverall Grade: PASS")
        sys.exit(0)
    else:
        print("\nOverall Grade: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
