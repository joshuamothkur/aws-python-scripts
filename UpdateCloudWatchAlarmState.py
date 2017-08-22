# Script to change the status of CloudWatch Alarm
# Note that EC2 instance where the script is executed should have IAM role with CloudWatch Access
# Available alarm options 'OK'|'ALARM'|'INSUFFICIENT_DATA'
# Command ++++ python nameofthescript.py

import boto3, argparse, sys
client = boto3.client('cloudwatch', region_name='us-east-1') # Change the region accordingly

alarmName = raw_input('\n'+'Enter the name of the CloudWatch alarm: ')
alarmState = raw_input('Enter the value of the new alarm state: ').strip()
alarmReason = raw_input('Enter the reason why this alarm is set to this specific state: ')
print " "

class textFormat:
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'

if (alarmState == 'OK') or (alarmState == 'ALARM') or (alarmState == 'INSUFFICIENT_DATA'):
  try:
      payload = client.set_alarm_state(
        AlarmName = alarmName,
        StateValue = alarmState,
        StateReason = alarmReason)

  except Exception as e:
      print textFormat.FAIL + ("Alarm state update failed due to: " + '%s' % e + "\n") + textFormat.END
      exit()
  print textFormat.SUCCESS + ("Successfully updated the state of '{}' CloudWatch alarm to '{}'\n").format(alarmName, alarmState) + textFormat.END
  
else:
  print textFormat.FAIL + ("ERROR: Invalid Alarm State input, CloudWatch only supports 'OK', 'ALARM', 'INSUFFICIENT_DATA' alarm states\n") + textFormat.END
  exit()
