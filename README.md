# masLookup-ng
A simple python script to perform a forward DNS look up against a list of IPs.

# Usage
```
python3 massLookup-ng -i <hostnames/IPs> -o <results.txt>
```

# Help
```
usage: masslookup-ng.py [-h] -i INPUT -o OUTPUT

Perform parallel massLookup-ng operations on a list of IP addresses or domain names.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specify the input file path. The file should contain one IP address or domain name per line.
  -o OUTPUT, --output OUTPUT
                        Specify the output file path where resolved hostnames will be saved.

Example usage: python massLookup-ng -i ips.txt -o hostnames.txt
```
