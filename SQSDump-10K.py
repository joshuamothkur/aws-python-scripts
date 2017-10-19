# Runs on an EC2 instance with SQS access.
# Used for reading more than 10000+ messages from an SQSQueue and dump them in a text file
# Command ++++ python nameofthescript.py

import os, boto.sqs
conn = boto.sqs.connect_to_region("eu-west-1") # Change the region accordingly

dlq = conn.get_queue('DummyDeadLetterQueue') # Change the SQS Queue accordingly
size = dlq.count()

print "Total message in the Queue:", int(size)
print "\nGetting messages from the", dlq

dumpfile = open("backupdump.txt", "w")
ProcessedCount = 0

while True:
    
    messages = dlq.get_messages(num_messages=10, wait_time_seconds = 10, visibility_timeout = 500) # wait_time for long polling and visibility_timeout to make sure we don't read the same message again and again
    
    if len(messages) == 0:
	print "\nNo messages to read!\n"
        break
    
    for message in messages:
        dumpfile.write(message.get_body() + '\n')
	ProcessedCount += 1
	print "Processed Messages: ",int(ProcessedCount)

dumpfile.close()
print "\ndone!\n"

# You can copy the output file to an S3 bucket using "aws s3 cp backupdump.txt s3://bucket-name/folder/backupdump.txt"
