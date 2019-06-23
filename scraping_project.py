# http://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import re


base_url = "http://quotes.toscrape.com"

def scrape_quotes():
    all_quotes = []
    page_url = "/page/1"
    while page_url:
        res = requests.get(f"{base_url}{page_url}")
        print(f"Now scraping {base_url}{page_url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_ = "quote")
        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_ = "text").get_text(),
                "author": quote.find(class_ = "author").get_text(),
                "link": quote.find("a")["href"],     #Taking advantage of the fact: bio-link is first anchor-tag
            })

        next_btn = soup.find(class_ = "next")

        page_url = next_btn.find("a")["href"] if next_btn else None
        # time.sleep(2)
    return all_quotes
    
def start_game(quotes):
    quote = random.choice(quotes)
    full_name = quote["author"].split(" ")

    if len(full_name) == 2:
        first_name = quote["author"].split(" ")[0]
        last_name = quote["author"].split(" ")[1]
    elif len(full_name) == 3:
        first_name = quote["author"].split(" ")[0]
        last_name = quote["author"].split(" ")[2]

    print("\nThis is the quote: " + quote["text"])
    remaining_guesses = 4
    guess = ""

    while guess.upper() != quote["author"].upper() and remaining_guesses:
        guess = input(f"Who's the author of this quote? Guesses remaining: {remaining_guesses}\n")
        remaining_guesses -= 1
        if guess.upper() == quote["author"].upper():
            print("You answered correctly!")
            break
        if remaining_guesses == 3:
            res = requests.get(f"{base_url}{quote['link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_ = "author-born-date").get_text()
            birth_place = soup.find(class_ = "author-born-location").get_text()
            print(f"Here's a hint: The author was born on {birth_date} {birth_place}.")
        elif remaining_guesses == 2:
            first_name_initial = first_name[0]
            last_name_initial = last_name[0]
            print(f"The author's first name starts with {first_name_initial} and last name starts with {last_name_initial[-1]}")
        elif remaining_guesses == 1:
            print("A little bit of trivia for the author:")
            desc_req = requests.get(f"{base_url}{quote['link']}")
            desc_soup = BeautifulSoup(desc_req.text, "html.parser")
            desc = desc_soup.find(class_ = "author-description").get_text()
            regex = re.compile(r'(\s*){}|{}(\s*)'.format(first_name, last_name))
            covered_desc = regex.sub(" $$$$ ", desc)
            for item in covered_desc.split(".")[1:4]:
                print("\n")
                print(item)
        else:
            print(f"Sorry, you're out of guesses. The author was {quote['author']}")

    again = ""
    again = input("Would you like to play again? (Y/N): ")
    while again.lower() not in ("y","yes","n","no"):
        again = input("Please give a valid answer (Y, N, Yes, No): ")
    if again.lower() in ("yes", "y"):
        return start_game(quotes)
    else:
        print("Thanks for playing. Goodbye.")

quotes = scrape_quotes()
start_game(quotes)


