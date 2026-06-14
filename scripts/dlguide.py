import requests
import gzip
import shutil

def main():
    url = "https://epgshare01.online/epgshare01/epg_ripper_DO1.xml.gz"
    output = "epg_ripper_DO1.xml.gz"
    uncompressed = "epg_ripper_DO1.xml"
    download_file(url, output)
    decompress_xml_gz(output, uncompressed)

def download_file(url:str, output:str)-> None:
    """Download the file for the guide."""
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
    except FileNotFoundError:
        print("Error: The Specified source file could not be found")
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

if __name__ == "__main__":
    main()