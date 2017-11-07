# Simple function which can be called to upload a file into S3 bucket
# This function takes File name, S3 Bucket Name, S3 Bucket's Directory (Optional) as input

import boto, os  # imports all necessary modules
from boto.s3.key import Key
s3connection = boto.connect_s3()

def copy_file_to_s3(file, bucketname, directory=None):
  try:
    s3bucket = s3connection.get_bucket(bucketname)
    if directory != None:
        path = directory + '/' # If there is a sub-directory in S3 bucket
    else:
        path = ''
    full_key_path = os.path.join(path, file)
    s3Key = s3bucket.new_key(full_key_path)
    s3Key.set_contents_from_filename(file)
  except Exception, e:
    print ("\nUploading to S3 failed due to :" '%s' % e)

'''
# Following is a sample script which uses the above copy_file_to_s3 function
# Command ++++ python nameofthescript.py -f filetobeuploaded.txt -b S3Bucket -d Directory (Optional)

import argparse, S3FileUploadFunction

parser = argparse.ArgumentParser(description='The location of the file, S3 bucket and S3 directory')
parser.add_argument('-f', '--File', help='Path to the file', required=True)   # We need to use -f to indicate file location
parser.add_argument('-b', '--S3', help='S3 Bucket name', required=True)   # We need to use -b to indicate S3 bucket name
parser.add_argument('-d', '--Directory', help='S3 Bucket Directory name')   # We need to use -d to indicate S3 bucket's directory name

args = parser.parse_args()
inputFile = args.File
S3Bucket = args.S3
S3Directory = args.Directory

s3upload.copy_file_to_s3(inputFile, S3Bucket, S3Directory)
'''

if __name__ == '__main__':
    copy_file_to_s3()
