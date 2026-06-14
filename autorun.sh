#!/bin/bash
echo $(dirname $0)
cd $(dirname $0)/scripts/
python3 extract_direct_streams.py > ../dailymotion.m3u
python3 dlguide.py
python3 get_streams.py
echo m3u grabbed
