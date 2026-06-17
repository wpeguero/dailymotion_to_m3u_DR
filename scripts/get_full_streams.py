"""File set to consolidate the scripts into one python file."""
import requests
import gzip
import shutil
import xml.etree.ElementTree as ET
import re
import csv

import pandas as pd

def main():
    channels_url= "https://iptv-org.github.io/iptv/countries/do.m3u"
    out_channels = "../DR_channels.m3u"
    download_m3u(channels_url, out_channels)
    extract_tvg_id(out_channels, '../tvg_ids.csv')
    guide_url = "https://epgshare01.online/epgshare01/epg_ripper_DO1.xml.gz"
    
    out_guide = "../epg_ripper_DO1.xml.gz"
    uncompressed = "../epg_ripper_DO1.xml"
    download_file(guide_url, out_guide)
    decompress_xml_gz(out_guide, uncompressed)
    # Extract channel IDs from XML and save to CSV
    extract_channel_ids_from_xml(uncompressed, "../tv_ids.csv")
    switch_ids('lookup_ids.csv', out_channels)


# Set of functions for downloading the epg.
def download_file(url:str, output:str) -> None:
    """Donwload files from the link."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(output, 'wb') as file:
            file.write(response.content)
            file.close()
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    return None

def decompress_xml_gz(compressed_file:str, xml_file_path:str) -> None:
    """Decompresses xml files using gzip compression."""
    try:
        with gzip.open(compressed_file, 'rb') as input_file:
            with open(xml_file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)
                output_file.close()
    except FileNotFoundError:
        print("Error: The specified source file could not be found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_epg(url:str, output_filename:str):
    """Searches for the file based on the link provided by EPGSHARE"""
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(output_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
            file.close()

# Function for downloading the m3u file
def download_m3u(url:str, output_file:str) -> None:
    """Extracts the m3u file from the link."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            file.write(response.content)
            file.close()
    else:
        print("the link did not function properly.")
    return None

def extract_tvg_id(file_m3u:str, out_ids:str) -> None:
    """Extracts the tvg id."""
    pattern = re.compile(r'tvg-id="([^"]+)"')
    tvg_ids = list()
    with open(file_m3u, 'r') as file:
        for line in file:
            #tvg-id metadata is always located on the #EXTINF
            if line.startswith("#EXTINF"):
                hit = pattern.search(line)
                if hit:
                    tvg_ids.append(hit.group(1))
                else:
                    pass
        file.close()
        with open(out_ids, 'w') as cfile:
            writer = csv.writer(cfile)
            writer.writerow(["tvg_ids"])
            writer.writerows([[item] for item in tvg_ids])
            cfile.close()
        file.close()
    return None

#Cannot switch channel ids.
def switch_ids(csv_file:str, m3u_file:str) -> None:
    """Extracts the csv file information into a dictionary and switches
    the tvg-ids found in the m3u file."""
    lookup = dict()
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) #Skip the first row
        for row in reader:
            if len(row) >= 2:
                chid, tvgid = row[0].strip(), row[1].strip()
                lookup[tvgid] = chid
        file.close()
        print(lookup)
    updated_lines = list()
    with open(m3u_file, mode='r', encoding='utf-8') as f:
        count = 0
        for line in f:
            # Look for typical M3U tags like tvg-id="ID"
            
            for tvgid, chid in lookup.items():
                search_string = f'tvg-id="{tvgid}"'
                replace_string = f'tvg-id="{chid}"'
                if search_string in line:
                    count += 1
                    print(f"found {count}")
                    line = line.replace(search_string, replace_string)
            
            updated_lines.append(line)
        f.close()

    # --- Step 3: Save Updated M3U ---
    with open(m3u_file, mode='w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    return None

def extract_channel_ids_from_xml(xml_file_path: str, output_csv_path: str) -> None:
    """Extracts channel IDs from XML file and writes them to a CSV file."""
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Extract channel IDs from the 'id' attribute of each channel element
        channel_ids = []
        for channel in root.findall('channel'):
            channel_id = channel.get('id')
            if channel_id:
                channel_ids.append(channel_id)
        
        # Write to CSV file
        with open(output_csv_path, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['channel_id'])  # Header row
            for channel_id in channel_ids:
                writer.writerow([channel_id])
        print(f"Successfully extracted {len(channel_ids)} channel IDs to {output_csv_path}")
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


if __name__ == "__main__":
    main()