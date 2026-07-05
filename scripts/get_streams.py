"""This file gets the streams from a list that is updated by others."""
import requests

def main():
    url = "https://iptv-org.github.io/iptv/countries/do.m3u"
    output_file = "../DR_channels.m3u"
    download_m3u(url, output_file)


def download_m3u(url:str, output_file:str) -> None:
    """Extracts the m3u file from the link."""
    response = requests.get(url)
    if response.status_code == 200:
        print("code is good.")
        with open(output_file, 'wb') as file:
            file.write(response.content)
            file.close()
        with open(output_file, 'r+') as file:
            count = 1
            lines = list()
            for line in file.readlines():
                if "EXTINF" in line:
                    print(line)
                    line = line.replace("-1", str(count))
                    count += 1
                    lines.append(line)
                else:
                    lines.append(line)
            file.seek(0)
            file.writelines(lines)
            file.close()
            
    else:
        print("the link did not function properly.")
    return None


if __name__ == "__main__":
    main()