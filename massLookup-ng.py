import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor

def perform_nslookup(query):
    try:
        # Perform nslookup using subprocess
        result = subprocess.run(['nslookup', query], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Check for errors in the output
        if "Can't find" in output or "No answer" in output:
            return None

        # Extract IP address
        ip_address = None
        for line in output.split('\n'):
            if 'Address:' in line and '#' not in line:
                # Get the IP address (skipping the line with the DNS server address)
                ip_address = line.split('Address:')[-1].strip()
                # Only return the IP address if it is not an IPv6 address
                if ':' not in ip_address:
                    return ip_address
                else:
                    # Store the IPv6 address in case no IPv4 address is found
                    ip_v6_address = ip_address

        # If no IPv4 address was found, return the stored IPv6 address
        return ip_v6_address if 'ip_v6_address' in locals() else None

    except Exception as e:
        print(f"Error processing {query}: {e}")
    return None

def main():
    # Setup command line argument parser
    parser = argparse.ArgumentParser(
        description='Perform parallel massLookup-ng operations on a list of IP addresses or domain names.',
        epilog='Example usage: python massLookup-ng -i ips.txt -o hostnames.txt',
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
        help='Specify the output file path where resolved hostnames will be saved.'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Number of parallel nslookup operations
    max_workers = 10

    # Read all IPs/Domains from the input file
    with open(args.input, 'r') as f:
        queries = [line.strip() for line in f if line.strip()]

    # Use ThreadPoolExecutor to execute nslookup in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(perform_nslookup, queries))

    # Write results to the output file
    with open(args.output, 'w') as out_f:
        for result in results:
            if result:
                out_f.write(result + '\n')

    print("NSLookup completed. Results saved in", args.output)

if __name__ == '__main__':
    main()
