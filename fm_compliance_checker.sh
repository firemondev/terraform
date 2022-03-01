#!/bin/bash

echo "Enter the json file name: "
read filename

file_path=`find $(pwd) -name $filename`

[ -z "$file_path" ] && echo "No JSON file found!" && exit 0


python ./Python-Cloud-Integration/orchestration_apis.py $file_path
cat final_result.json | json_pp > result.json


echo "PCA response is copied to \"result.json\" file!"

