# Author @joshua-mothkur
# This script helps extracting key value pairs from JSON blob present in a file

import json, sys
with open('sample.txt') as f:
    for line in f:
        j_content = json.loads(line)
        print j_content["sampleJSONKey"]

#Use this if key value pair is nested
        #print j_content(["sampleJSONUpperNest"]["sampleJSONKey"])
