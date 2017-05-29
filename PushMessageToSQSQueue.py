# Author @joshua-mothkur
# Runs on an EC2 instance with SQS access.
# Used to send messages from a text file to an SQSQueue
# Command ++++ python nameofthescript.py -i inputfile.txt

import argparse, time, sys
import boto.sqs
from boto.sqs.message import RawMessage
chill = time.sleep(0.2)
sqsconn = boto.sqs.connect_to_region("eu-west-1") # Connects to a specified region
que = sqsconn.get_queue('DummyQueue') # Selecting a SQSQueue
count = 0 # To keep a track of progress

parser = argparse.ArgumentParser(description='Parsing input file location')
parser.add_argument('-i', '--input', help='Path to input file')   # So we can use -i to indicate input file location
args = parser.parse_args()
if args.input is None:
    sys.exit("Input file was not specified!")
f = open(args.input,'r')        # Opens the user provided file location.
f1 = open('errorlogs.txt', 'w') # Errors are logged in this file

# Function to display progress bar
def update_progress_bar():
    print '\b.',
    sys.stdout.flush()
print 'Running Script ',
sys.stdout.flush()

for line in iter(f):
    if len(line.strip()) != 0:    # If there are empty lines in the input text file, they will be ignored
        try:
            message = line.strip()
            msg = RawMessage()
            msg.set_body(message)
            que.write(msg) # Sending the message to the OrderUpdate queue
            count += 1
            update_progress_bar()
            chill
        except Exception as e:
            f1.write ('%s' % e + "\n")
            continue

f.close()
f1.close()
print "Sent " + str(count) +" messages to the Queue!"
