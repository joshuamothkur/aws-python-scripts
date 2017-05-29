# Author @joshua-mothkur
# Runs on an EC2 instance with SQS access.
# Used for reading messages from an SQSQueue and dump them in a text file
# Command ++++ python nameofthescript.py

import boto.sqs
conn = boto.sqs.connect_to_region("eu-west-1") # Connects to a specified region

dlq = conn.get_queue('DummyDeadLetterQueue') # Connects to a Queue
size = dlq.count() # Will print out the no of messages present in the queue

print "Total message in the Queue:", int(size)
print "\nGetting messages from the", dlq

# Dumps all of the messages present in the queue to a file which is stored locally
dlq.dump('messages.txt', sep='\n------------------\n')
print "\nMessages were successfully copied to a file"
