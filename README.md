# Quote Modification
This code is for my twitter bot: [PenisQuoteBot](https://twitter.com/PenisQuoteBot)

Inspired by this wonderful [reddit post](https://www.reddit.com/r/AskReddit/comments/ls7s4o/change_a_single_word_in_a_famous_quote_with_penis/)

## Installation & Execution
* Clone this repo
* Pip install the `requirements.txt` file: `pip3 install -r requirements.txt`
    * I recommend using a virtual environment to keep everything kosher on your system
* Create a `config.json` file in the `config` directory following the directions below
* Run the code from the root of the project with `python3 source/main.py`

## Development
* This bot was developed on WSL Ubuntu `20.04` utilizing Python `3.8.5`

## Libraries
This Bot utilizes the following libraries:
* Tweepy: Easily interface with Twitter API

## Config File
Your `json/config.json` file should look like this, a template config file is provided:

    {
        "api-key": "Your Twitter Key Here!",
        "api-secret-key": "Your Twitter Key Here!",
        "bearer-token": "Your Twitter Token Here!",
        "access-token": "Your Twitter Token Here!",
        "access-token-secret": "Your Twitter Token Here!"
    }

## Input
This bot is using a collection of quotes and nouns that I found scatter around the web.

## Contributing
Feel free to open a PR for improvements to the bots functionality or to update/add new quotes and nouns.