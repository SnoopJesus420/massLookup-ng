# Written by SnoopJesus420 -> https://github.com/SnoopJesus420/

import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os

def perform_nslookup(query, log_file):
    try:
        # Perform nslookup using subprocess
        result = subprocess.run(['nslookup', query], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Check for errors indicating no resolution
        if "Can't find" in output or "No answer" in output or "NXDOMAIN" in output:
            with open(log_file, 'a') as log:
                log.write(f"Failed to resolve {query}: {output.strip()}\n")
            return None

        # Extract IP address or hostname
        ip_address = None
        hostname = None
        for line in output.split('\n'):
            if 'Address:' in line and '#' not in line:
                # Get the IP address (skipping the DNS server address)
                ip_address = line.split('Address:')[-1].strip()
                # Only store IPv4 or IPv6
                if ':' not in ip_address:
                    return ip_address  # Return IPv4 immediately
                else:
                    ip_v6_address = ip_address  # Store IPv6 as fallback
            elif 'name =' in line:  # Handle reverse lookup hostname
                hostname = line.split('name =')[-1].strip().rstrip('.')
                return hostname  # Return hostname for reverse lookup

        # Return IPv6 address if no IPv4 or hostname was found
        return ip_v6_address if 'ip_v6_address' in locals() else None

    except Exception as e:
        # Log any subprocess or other errors
        with open(log_file, 'a') as log:
            log.write(f"Error processing {query}: {str(e)}\n")
        return None

def main():
    # Setup command line argument parser
    parser = argparse.ArgumentParser(
        description='Perform parallel nslookup operations on a list of IP addresses or domain names.',
        epilog='Example usage: python massLookup-ng.py -i ips.txt -o hostnames.txt -l unresolved.log -t 20',
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Input file argument
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Specify the input file path. The file should contain one IP address or domain name per line.'
    )

    # Output file argument
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Specify the output file path where resolved hostnames or IPs will be saved.'
    )

    # Log file argument
    parser.add_argument(
        '-l', '--log',
        default='unresolved.log',
        help='Specify the log file path for unresolved queries (default: unresolved.log).'
    )

    # Threads argument
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=10,
        help='Specify the number of threads to use for parallel lookups (default: 10).'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Number of parallel nslookup operations
    max_workers = args.threads
    log_file = args.log

    # Ensure log file is empty or created
    if os.path.exists(log_file):
        os.remove(log_file)  # Clear existing log file

    # Read all IPs/Domains from the input file
    with open(args.input, 'r') as f:
        queries = [line.strip() for line in f if line.strip()]

    # Use ThreadPoolExecutor to execute nslookup in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Pass log_file to perform_nslookup
        results = list(executor.map(lambda q: perform_nslookup(q, log_file), queries))

    # Write results to the output file
    with open(args.output, 'w') as out_f:
        for result in results:
            if result:
                out_f.write(result + '\n')

    print(f"NSLookup completed using {max_workers} threads. Results saved in {args.output}")
    if os.path.exists(log_file):
        print(f"Unresolved queries logged in {log_file}")

if __name__ == '__main__':
    main()
