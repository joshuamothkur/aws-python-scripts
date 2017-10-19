#!/usr/bin/env python
# Author @joshua-mothkur
# Runs on an EC2 instance with SNS access.
# Used to send messages present in an input file to SNS Topic. 
# Command ++++ python nameofthescript.py -i inputfile.txt

import argparse, time, sys, csv, os
import boto.sns
snsconn = boto.sns.connect_to_region("us-east-1") # Connects to a specified region
#topic = snsconn.get_topic_attributes('arn:aws:sns:us-east-1:123456:SNS-Topic') # Selecting an SNS Topic
#print topic # This will print out SNS Topic's attributes
topicARN = 'arn:aws:sns:us-east-1:123456:SNS-Topic'
chill = time.sleep(0.2)
count = 0 # To keep a track of progress

parser = argparse.ArgumentParser(description='Parsing input file location')
parser.add_argument('-i', '--input', help='Path to input file', required=True)   # So we can use -i to indicate input file location
args = parser.parse_args()
inputFile = open(args.input,'r')  # Opens the user provided file location which will contain messages which need to be pulished to SNS Topic.
errorFile = open('errorlogs.txt', 'w') # Errors are logged in this file

reader = csv.reader(inputFile)
for row in reader:
    if row:  # If an empty line is present in the file, it would be skipped
        rawMessage: = row[0].strip() # Making sure there are no leading / trailing spaces
        if rawMessage:
            try:
                sendMessage = snsconn.publish(topicARN, rawMessage)
                #print ("\n sendMessage \n") # Can be used to see the message which was sent to SNS Topic
                count += 1
                chill
            except Exception, e:
                errorFile.write ('%s' % e + "\n")
                continue   # This is needed for us to continue execution of this script even after an exception

inputFile.close()
errorFile.close()
if os.stat("errorlogs.txt").st_size == 0:
    print("\nNo errors after running this script :), deleting the log file" + '\n')
    os.remove("errorlogs.txt")

print ("\nDone! '{}' messages from input file were sent to SNS Topic").format(count)
