import os
import psutil

# Function to get information about mounted USB drives
def get_usb_info():
    usb_info = []
    for partition in psutil.disk_partitions(all=False):
        if partition.fstype:  # Check if the partition is formatted
            usage = psutil.disk_usage(partition.mountpoint)
            usb_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
    return usb_info

# Function to check if a file contains suspicious content
def is_malicious(file_path):
    # Patterns to look for in the file content
    suspicious_patterns = ['malware', 'virus', 'trojan', 'ransomware']
    
    try:
        with open(file_path, 'r', errors='ignore') as file:
            content = file.read().lower()
            for pattern in suspicious_patterns:
                if pattern in content:
                    return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return False

# Function to list and scan files in the USB drive
def scan_files(mountpoint):
    print(f"Scanning files in {mountpoint}...")
    safe = True
    file_count = 0
    malicious_count = 0
    
    for root, dirs, files in os.walk(mountpoint):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Skip default files
            if filename.lower() in ['autorun.inf', 'desktop.ini']:
                continue
            
            file_size = os.path.getsize(filepath)
            file_count += 1
            print(f"Scanning file: {filepath} | Size: {file_size / (1024**2):.2f} MB")

            if is_malicious(filepath):
                print(f"Malicious content detected in: {filepath}")
                malicious_count += 1
                safe = False
        
        # Display progress
        print(f"Scanning progress: {file_count} files checked, {malicious_count} malicious files found")
        break  # Only list files in the root of the mountpoint for progress display

    return safe

# Main function to execute the script
def main():
    usb_info = get_usb_info()
    if not usb_info:
        print("No USB drives detected.")
        return

    for info in usb_info:
        print(f"Scanning USB Drive: {info['device']} ({info['mountpoint']})")
        safe = scan_files(info['mountpoint'])
        
        if safe:
            print(f"The USB drive {info['device']} is safe to use.")
        else:
            print(f"The USB drive {info['device']} is NOT safe to use.")

if __name__ == "__main__":
    main()
