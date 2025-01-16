@echo off

echo Creating your playlist...
cd scripts
python extract_direct_streams.py > ../dailymotion.m3u

pause
