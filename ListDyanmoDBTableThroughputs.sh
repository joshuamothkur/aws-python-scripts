#!/bin/bash
# Author @joshua-mothkur
# Script to find list of Regions where DDB Tables are present for an AWS account and their corresponding read/write throughputs
# This script (AWS CLI Commands) needs permissions to access DDB
# Prerequisite: 'jq' unix tool which can be downloaded and installed by following the step mentioned below
## wget http://stedolan.github.io/jq/download/linux64/jq ; chmod +x ./jq ; sudo cp jq /usr/bin
## regions.txt file which lists all of the DDB regions

echo " "; echo "Querying for the list of Regions where DDB Tables are present:"

# Clearing any old output files
rm -rf output.txt

FILELENGTHCONSTANT=3

# File where list of regions are stored
for region in $(cat regions.txt);
do 
    aws dynamodb list-tables --region ${region} 2>/dev/null > tables.json

    # Temp file to store table data
    TEMPFILE=tables.json
    FILESIZE=$(wc -l "$TEMPFILE" | awk '{print $1}')
    
    # Empty tables in a region will have a file size of 3kb
    if (($FILESIZE != $FILELENGTHCONSTANT)); then
    echo ${region}; echo "" >> output.txt; echo "############################" >> output.txt; echo ${region} >> output.txt;
    aws dynamodb list-tables --region ${region} 2>/dev/null > tables.json
    fi
    
    for value in $(cat tables.json | jq -r '.TableNames'[]);
    do
        echo "*********" >> output.txt; echo ${value} >> output.txt; echo "" >> output.txt;
        aws dynamodb describe-table --table-name ${value} --region ${region} | grep -A5 "ProvisionedThroughput" >> output.txt
    done

done

# Removing the temp file where we've stored the tables data
rm -rf tables.json

echo ""; echo "All done! Provisioned capacity of tables were written to output.txt file"; echo ""
