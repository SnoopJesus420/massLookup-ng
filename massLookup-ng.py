import subprocess
from concurrent.futures import ThreadPoolExecutor

def perform_nslookup(ip):
    try:
        # Perform nslookup using subprocess
        result = subprocess.run(['nslookup', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Extract hostname
        for line in output.split('\n'):
            if 'name =' in line:
                # Remove the final dot and return the hostname
                return line.split('name =')[-1].strip().strip('.')
    except Exception as e:
        print(f"Error processing {ip}: {e}")
    return None

def main():
    input_file = 'hostnames/IPs.txt'
    output_file = 'nslookup_hostnames.txt'
    max_workers = 10  # Number of parallel nslookup operations

    # Read all IPs/Domains from the file
    with open(input_file, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    # Use ThreadPoolExecutor to execute nslookup in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(perform_nslookup, ips))

    # Write results to the output file
    with open(output_file, 'w') as out_f:
        for hostname in results:
            if hostname:
                out_f.write(hostname + '\n')

    print("NSLookup completed. Results saved in", output_file)

if __name__ == '__main__':
    main()
