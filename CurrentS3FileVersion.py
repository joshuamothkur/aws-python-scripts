# Author @joshua-mothkur
# Runs on an EC2 instance with S3 access.
# Used for printing current version of an object present in S3 Bucket
# Command ++++ python nameofthescript.py

import boto, os, sys

connection = boto.connect_s3()
bucket = connection.get_bucket('sampletestbucket') # Mention the S3 bucket name here

RawS3Key = raw_input('\n'+'Enter the name of the S3 object: ')
S3Key = RawS3Key.strip()

# To get the size of the object
#object = bucket.lookup (S3Key, ) # Mention the object present in the S3 bucket
#print object.size

# To retrive all the objects in the bucket
#print "\n Listing all the objects in the bucket"
#for objects in bucket:
#    print objects

print "\n Retrieving all versions for " + S3Key
versions = bucket.list_versions(prefix=S3Key)
for version in versions:
    print version.version_id

notify = "\n Current version of {} present in the bucket"
print notify.format(S3Key)
current =  bucket.get_key(S3Key)
print current.version_id + '\n'
