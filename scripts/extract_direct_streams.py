import streamlink

M3U = "#EXTM3U\n"

def main():
    print(M3U)
    with open('dailymotion_channel_info.txt') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('~~'):
                continue
            if not line.startswith('http'):
                line = line.split('|')
                ch_name = line[0].strip()
                grp_title = line[1].strip().title()
                tvg_logo = line[2].strip()
                tvg_id = line[3].strip()
                print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
            else:
                grab(line)

def grab(link:str):
    """Extract the url link to view the show."""
    session = streamlink.Streamlink()
    streams = session.streams("https://livestream.com/accounts/27456795/events/10633780")
    best = streams['best']
    print(f'{best.url}')


if __name__ == "__main__":
    main()