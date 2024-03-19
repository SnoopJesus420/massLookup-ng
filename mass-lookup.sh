#!/bin/bash

# Input file 
input_file="ip_list.txt"

# Output file
output_file="nslookup_hostnames.txt"

while IFS= read -r ip; do
    hostname=$(nslookup "$ip" | awk '/name =/{print $NF}')
    
    hostname="${hostname%.}"
    
    if [[ -n $hostname ]]; then
        echo "$hostname" >> "$output_file"
    fi
done < "$input_file"

echo "NSLookup completed. Results saved in $output_file"
