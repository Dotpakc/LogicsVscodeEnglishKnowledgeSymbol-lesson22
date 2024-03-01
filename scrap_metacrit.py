import json
import requests

from bs4 import BeautifulSoup


url = "https://www.metacritic.com/browse/game/pc/all/all-time/metascore/?releaseYearMin=2015&releaseYearMax=2022&platform=pc&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)
print(response.status_code)
# print(response.text)

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

all_games_data = []

all_games = soup.find_all("div", class_="c-finderProductCard c-finderProductCard-game")
print(len(all_games))
for game in all_games:
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
    
    all_games_data.append(game_data)
    
with open("metacritic.json", "w") as file:
    json.dump(all_games_data, file, indent=4)