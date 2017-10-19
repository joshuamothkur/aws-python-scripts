# Runs on EC2 server with permissions to access RDS Instance
# Script needs boto3, if its missing run $ sudo pip install boto3 -y

import boto3

client = boto3.client('rds', region_name='eu-west-1') # Change the region accordingly

class textFormat:
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

FAILED = textFormat.FAIL
BOLD = textFormat.BOLD
ENDBOLD = textFormat.END

db_identifier = 'rdsdbreplica' # Change the DB Identifier accordingly

try:
    response = client.describe_db_instances(DBInstanceIdentifier=db_identifier)

except Exception, e:
    print FAILED + ("\nUnable to get instance details: %s" %e) + ENDBOLD + "\n"
    exit()
    
db_instance = response['DBInstances'][0] # Loading value returned from API call to a variable

# Printing few details of the DB Instance to which we've connected to
print BOLD + "\nHere are few details of %s DBInstance: " % db_identifier + ENDBOLD
print "\n", BOLD + "MasterUsername" + ENDBOLD, "=", db_instance['MasterUsername']
print BOLD + "EngineVersion" + ENDBOLD, "=", db_instance['EngineVersion']
print BOLD + "DBInstanceClass"  + ENDBOLD, "=", db_instance['DBInstanceClass']
temp = db_instance['StatusInfos'][0] # Loading the StatusInfos dictionary into variable so I can parse it below
for key, value in temp.iteritems():
    print BOLD + key + ENDBOLD, '=', value
print BOLD + "Engine" + ENDBOLD, "=", db_instance['Engine']
print BOLD + "EngineVersion" + ENDBOLD, "=", db_instance['EngineVersion']
print BOLD + "DBInstanceStatus" + ENDBOLD, "=", db_instance['DBInstanceStatus']
print BOLD + "DBName" + ENDBOLD, "=", db_instance['DBName']
print BOLD + "ReadReplicaSourceDBInstanceIdentifier" + ENDBOLD, "=", db_instance['ReadReplicaSourceDBInstanceIdentifier'], "\n"
