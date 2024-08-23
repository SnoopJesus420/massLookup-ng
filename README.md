# masLookup-ng
A simple python script to perform a forward/reverse DNS A record look up against a list of IPs/hostnames... with multithreading... >:)

# Usage
```
python3 massLookup-ng.py [-h] -i INPUT -o OUTPUT [-t THREADS]
```

# Help
```
Perform parallel nslookup operations on a list of IP addresses or domain names.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specify the input file path. The file should contain one IP address or domain name per line.
  -o OUTPUT, --output OUTPUT
                        Specify the output file path where resolved hostnames will be saved.
  -t THREADS, --threads THREADS
                        Specify the number of threads to use for parallel lookups (default: 10).

Example usage: python3 massLookup-ng -i ips.txt -o hostnames.txt -t 20
```
