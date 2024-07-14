import argparse
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
        ips = [line.strip() for line in f if line.strip()]

    # Use ThreadPoolExecutor to execute nslookup in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(perform_nslookup, ips))

    # Write results to the output file
    with open(args.output, 'w') as out_f:
        for hostname in results:
            if hostname:
                out_f.write(hostname + '\n')

    print("NSLookup completed. Results saved in", args.output)

if __name__ == '__main__':
    main()
