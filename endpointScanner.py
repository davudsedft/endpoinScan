import random
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_ipv4():
    iplist = 40  # Increased number of IPs to scan
    temp = []
    while len(temp) < iplist:
        temp.append(f"162.159.192.{random.randint(0, 255)}")
        temp.append(f"162.159.193.{random.randint(0, 255)}")
        temp.append(f"162.159.195.{random.randint(0, 255)}")
        temp.append(f"188.114.96.{random.randint(0, 255)}")
        temp.append(f"188.114.97.{random.randint(0, 255)}")
        temp.append(f"188.114.98.{random.randint(0, 255)}")
        temp.append(f"188.114.99.{random.randint(0, 255)}")
    return list(set(temp))[:iplist]

def generate_ipv6():
    iplist = 40  # Increased number of IPs to scan
    base_ip = "2606:4700:d0::"
    temp = []
    while len(temp) < iplist:
        temp.append(f"{base_ip}{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}")
    return list(set(temp))[:iplist]

def test_single_ip(ip, port):
    start = time.time()
    result = subprocess.run(["nc", "-zvu", ip, str(port)], capture_output=True, text=True)
    end = time.time()
    delay = (end - start) * 1000  # Convert to milliseconds
    return ip, port, result.returncode, delay

def test_connectivity(ip_list):
    ports = [880, 7156, 7103, 7552, 7281, 987, 2608, 1001, 1018, 1070]
    best_ip = None
    best_port = None
    best_delay = float('inf')
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for ip in ip_list:
            port = random.choice(ports)  # Randomly select a port for each IP
            futures.append(executor.submit(test_single_ip, ip, port))

        for future in as_completed(futures):
            ip, port, returncode, delay = future.result()
            if returncode == 0:
                if ':' in ip:  # Check if it's an IPv6 address
                    ip_port = f"[{ip}]:{port}"
                else:
                    ip_port = f"{ip}:{port}"
                print(f"\033[0;31mpurkow is free\033[0m {ip_port} - Delay: {delay:.2f} ms")
                if delay < best_delay:
                    best_delay = delay
                    best_ip = ip
                    best_port = port
            else:
                print(f"\033[0;31mpurkow is free\033[0m {ip}:{port}")
            if time.time() - start_time > 10:  # Stop after 10 seconds
                break

    if best_ip and best_port:
        if ':' in best_ip:  # Check if it's an IPv6 address
            best_ip_port = f"[{best_ip}]:{best_port}"
        else:
            best_ip_port = f"{best_ip}:{best_port}"
        print_best_ip_port(best_ip_port)
    else:
        print("No successful connections.")

def print_best_ip_port(ip_port):
    print("\033[0;32m" + "*" * 50)
    print(f"\n{'Best IP:Port: ' + ip_port:^50}\n")
    print("*" * 50 + "\033[0m")

def main():
    print("1. Generate IPv4")
    print("2. Generate IPv6")
    choice = input("Enter your choice: ")
    if choice == '1':
        ipv4_list = generate_ipv4()
        print("Generated IPv4 addresses:")
        for ip in ipv4_list:
            print(ip)
        test_connectivity(ipv4_list)
    elif choice == '2':
        ipv6_list = generate_ipv6()
        print("Generated IPv6 addresses:")
        for ip in ipv6_list:
            print(ip)
        test_connectivity(ipv6_list)
    else:
        print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
