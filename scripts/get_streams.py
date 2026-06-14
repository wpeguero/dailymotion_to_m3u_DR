"""This file gets the streams from a list that is updated by others."""
import requests

def main():
    url = "https://iptv-org.github.io/iptv/countries/do.m3u"
    output_file = "DR_channels.m3u"
    download_m3u(url, output_file)


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


if __name__ == "__main__":
    main()