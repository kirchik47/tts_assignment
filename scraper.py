from bs4 import BeautifulSoup
import requests


# Define headers to avoid being blocked by the website
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Referer': 'https://softwareengineeringdaily.com'
}

# Base sitemap url with links to all posts
base_url = "https://softwareengineeringdaily.com/sitemap-2.xml"
response = requests.get(base_url, headers=headers)
bs = BeautifulSoup(response.content, 'html.parser')
links = []
for loc in bs.findAll('loc'):
    loc_text = loc.text
    # Filter out non-post links
    if '2023' in loc_text or '2024' in loc_text:
        links.append(loc_text)

i = 0
links = links[33:]
for link in links:
    response = requests.get(link, headers=headers)
    bs = BeautifulSoup(response.content, 'html.parser')
    # Find <a> tag with href to post
    audio_tag = bs.find('a', class_='powerpress_link_d')
    if audio_tag:
        transcript_div = bs.find('div', class_='post__content')
        a_tags = transcript_div.findAll('a')
        transcript_url = None
        # Find the link to the transcript
        for a in a_tags:
            href = a.get('href')
            if href and href.endswith('.txt'):
                transcript_url = href
                break
        if transcript_url and transcript_url.endswith('.txt'):
            i += 1
            # Handle possible unicode and other issues with the transcript
            try:
                transcript = requests.get(transcript_url, headers=headers).content.decode()
                if i < 32:
                    continue
                with open(f'data/audios/{i - 32}.txt', 'w') as f:
                    f.write(transcript)
                audio_url = audio_tag['href']
                audio = requests.get(audio_url, headers=headers).content
                with open(f'data/audios/{i - 32}.mp3', 'wb') as f:
                    f.write(audio)
            except Exception as e:
                print(e)
                i -= 1

        print(i)
