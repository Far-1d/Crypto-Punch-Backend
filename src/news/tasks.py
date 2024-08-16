import requests
from bs4 import BeautifulSoup
from django.utils.html import mark_safe
import bleach

def news_update():
    response = requests.get('https://crypto.news/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.select("main[id='content']")[0]
        try:
            swiper_divs = main.select("div[class*='press-releases'] div[class*='swiper-wrapper']")[0].find_all('div', recursive=False)
            print("swipers are ",len(swiper_divs))
            for div in swiper_divs:
                image = div.find('figure').find('img')['src']
                link = div.find('figure').find('a')['href']
                title = div.find('p').get_text(strip=True)
        
                content = ''
        
                inner_response = requests.get(link)
                if inner_response.status_code == 200:
                    inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
                    text_content = []
                    inner_main = inner_soup.select("main[id='content']")[0]
                    inner_article = inner_main.select("div[id='ajax-load-more'] article")[0]
                    main_div = inner_article.select("div[class*='post-detail__container'] div[class*='blocks']")[0].find('html')
                    # print('main div opened', main_div)
                    for tag in main_div.children:
                        # Check if the tag is a <p> or <h2> and not an inner <div>
                        if tag.name in ['p', 'h2']:
                            # text_content.append(f"{tag.name}<"+tag.get_text(strip=True)+">")
                            text_content.append(str(tag))
                    content = get_sanitized_content(''.join(text_content))
                news = {'title': title, 'image':image,
                        'content': content, 'tags':[]}
                if news['title'] and news['content'] and news['image']:
                    yield news
        except Exception as e:
            print('swiper failed')
            print(e)
            
def get_sanitized_content(content):
        allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'a', 'img']
        allowed_attrs = {'a': ['href', 'target'], 'img': ['src', 'alt']}
        return mark_safe(bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs))