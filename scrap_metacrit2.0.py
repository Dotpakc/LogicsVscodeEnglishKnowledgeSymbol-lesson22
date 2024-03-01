import time
import random
import json
import requests

from bs4 import BeautifulSoup


url = "https://www.metacritic.com/browse/game/pc/all/all-time/metascore/?releaseYearMin=2015&releaseYearMax=2022&platform=pc&page={}"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_html(url):
    response = requests.get(url, headers=headers)
    return response.text



def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all("span", class_="c-navigationPagination_itemButton u-flexbox u-flexbox-alignCenter u-flexbox-justifyCenter g-text-xsmall g-inner-spacing-left-small g-inner-spacing-right-small g-inner-spacing-top-small g-inner-spacing-bottom-small")[-1].text.strip()
    print(int(pages))
    return int(pages)

def get_game_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_games = soup.find_all("div", class_="c-finderProductCard c-finderProductCard-game")
    
    page_games_data = []
    for game in all_games:# Цикл для перебору всіх ігор на сторінці
        # print(game)
        img_game = game.find("div" , class_="c-finderProductCard_img g-height-100 g-width-100").find("img")
        if not img_game:
            continue
        title_game = game.find("h3", class_="c-finderProductCard_titleHeading").find_all("span")[1].text

        meta_score = game.find("div", class_="c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall").text
        # print(meta_score)
        description = game.find("div", class_="c-finderProductCard_description").text
        
        game_data ={
            'title': title_game,
            "img": img_game.get("src"),
            "meta_score": meta_score,
            "description": description
        }
        page_games_data.append(game_data)
    return page_games_data


def save_file(items, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)

def main():
    all_games_data = []
    all_pages = get_total_pages(get_html(url.format(1)))   
    for i in range(1, all_pages+1): # Цикл для перебору всіх сторінок
        html = get_html(url.format(i)) # Отримуємо html сторінки
        
        all_games_data.extend(get_game_data(html)) # Отримуємо дані зі сторінки та додаємо до загального списку
        
        save_file(all_games_data, "metacritic.json")
        
        print(f"Cторінка {i}/{all_pages} пройдена")
        time.sleep(random.randint(1, 2))
    print("Робота завершена")

main()



# soup = BeautifulSoup(html_doc, 'html.parser')

# 

# all_games = soup.find_all("div", class_="c-finderProductCard c-finderProductCard-game")
# print(len(all_games))
# for game in all_games:
#     # print(game)
#     img_game = game.find("div" , class_="c-finderProductCard_img g-height-100 g-width-100").find("img")
#     if not img_game:
#         continue
#     title_game = game.find("h3", class_="c-finderProductCard_titleHeading").find_all("span")[1].text

#     meta_score = game.find("div", class_="c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall").text
#     # print(meta_score)
#     description = game.find("div", class_="c-finderProductCard_description").text
    
#     game_data ={
#         'title': title_game,
#         "img": img_game.get("src"),
#         "meta_score": meta_score,
#         "description": description
#     }
    
#     all_games_data.append(game_data)
    
# with open("metacritic.json", "w") as file:
#     json.dump(all_games_data, file, indent=4)