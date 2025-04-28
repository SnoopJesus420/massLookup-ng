# masLookup-ng
A simple python script to perform a forward/reverse DNS A record look up against a list of IPs/hostnames... with multithreading... >:)

# Usage
```
python3 massLookup-ng.py [-h] -i INPUT -o OUTPUT [-l LOG] [-t THREADS]
```

# Help
```
Perform parallel nslookup operations on a list of IP addresses or domain names.

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     Specify the input file path. The file should contain one IP address or domain name per line.
  -o, --output OUTPUT   Specify the output file path where resolved hostnames or IPs will be saved.
  -l, --log LOG         Specify the log file path for unresolved queries (default: unresolved.log).
  -t, --threads THREADS
                        Specify the number of threads to use for parallel lookups (default: 10).

Example usage: python massLookup-ng.py -i ips.txt -o hostnames.txt -l unresolved.log -t 20
```
