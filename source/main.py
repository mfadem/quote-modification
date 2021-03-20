# Imports for relevant libraries
import json
import random
import sys
import tweepy
import os
import re

# DEBUG = True
DEBUG = False

class Bot:
    def __init__(self, json_file):
        """
            Grab all of the keys/tokens
        """
        self.api_key = ''
        self.api_client = None

        # Grab the user config from the json file
        with open(json_file, 'r') as json_config:
            dict_config = json.load(json_config)
            self.api_key = dict_config["api-key"]
            self.api_secret_key = dict_config["api-secret-key"]
            self.bearer_token = dict_config["bearer-token"]
            self.access_token = dict_config["access-token"]
            self.access_token_secret = dict_config["access-token-secret"]

        # Authenticate with tweepy, use pin based auth if necessary
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        if len(self.access_token) == 0 and len(self.access_token_secret) == 0:
            self.authStandaloneApp(auth)
            # Update config.json file with tokens from the pin based auth
            with open(json_config, "r") as json_config:
                config = json.load(json_config)

                config["access-token"] = self.access_token
                config["access-token-secret"] = self.access_token_secret

                with open(json_config, "w") as json_config:
                    json.dump(config, json_config)

                print("Config file has been updated with the new access tokens")

        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api_client = tweepy.API(auth, wait_on_rate_limit=True)

    def authStandaloneApp(self, auth):
        """
            Authenticate the standalone app using PIN based auth requires human interaction to auth
        """
        # get access token from the user and redirect to auth URL
        auth_url = auth.get_authorization_url()
        print ('Authorization URL: ' + auth_url)
        print ('Open the authorization url in a browser and authenticate the standalone app')

        # ask user to verify the PIN generated in broswer
        verifier = input('Enter the PIN generated in the broswer: ').strip()
        auth.get_access_token(verifier)
        print ('ACCESS_KEY = "{}"' .format(auth.access_token))
        print ('ACCESS_SECRET = "{}"'.format(auth.access_token_secret))
        self.access_token = auth.access_token
        self.access_token_secret = auth.access_token_secret

    def getAuthUserData(self):
        """
            Output the authenticated accounts information to the auth.json file
        """
        with open('config/auth.json', 'w') as auth_json:
            json.dump(self.api_client.me(), auth_json, indent=4)

    def updateBotStatus(self, status_text=""):
        """
            Push a new status to Twitter with generated text
        """
        self.api_client.update_status(status_text)

    def slideIntoDM(self, user="", msg_text="", media_id=""):
        """
            Send a DM to a specified user along with media
        """
        self.getUserData(user)
        with open('config/user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        if msg_text is not None and media_id is not None:
            self.api_client.send_direct_message(user_dict["id"], msg_text, attachment_type="media", attachment_media_id=media_id)
        elif msg_text is not None:
            self.api_client.send_direct_message(user_dict["id"], msg_text)
        elif media_id is not None:
            self.api_client.send_direct_message(user_dict["id"], "", attachment_type="media", attachment_media_id=media_id)

    def getUserData(self, user=""):
        """
            Get the data for a specified user (i.e. user ID, name, tweets, pfp, etc.)
        """
        user_data = self.api_client.get_user(screen_name=user)
        with open('config/user.json', 'w') as user_json:
            json.dump(user_data._json, user_json, indent=4)

    def pullQuote(self):
        """
            Grab a random quote from the quote file, do some clean up and verification
        """
        with open("input/used_quotes.txt", 'r') as used_quotes:
            burned_quotes = used_quotes.read().splitlines()
            burned_quotes_len = len(burned_quotes)

        with open('input/quotes.txt', 'r') as quote_file:
            quote_file_len = len(quote_file.readlines())

        if burned_quotes_len >= quote_file_len:
            return("ERROR - NO MORE QUOTES! CONTACT MY HUMAN!")

        noun_list = []
        while len(noun_list) == 0:
            with open('input/quotes.txt', 'r') as quote_file:
                random_quote = random.choice(quote_file.read().splitlines())

                if random_quote in burned_quotes:
                    continue

                # I'm sure this logic will hold forever
                if len(random_quote.split('-')) >= 2:
                    quote = random_quote.split('-')[0].strip()
                    author = random_quote.split('-')[1].strip()
                else:
                    quote = random_quote
                    author = "Unknown"

            with open('input/nouns.txt', 'r') as noun_file:
                nouns = noun_file.read().splitlines()
                for noun in nouns:
                    noun_caps = noun.title()
                    if noun in re.findall(r"[\w']+", quote) and noun not in noun_list:
                        noun_list.append(noun)
                    elif noun_caps in re.findall(r"[\w']+", quote) and noun_caps not in noun_list:
                        noun_list.append(noun_caps)

            if noun_list == 0:
                with open("input/bad_quotes.txt", "a") as bad_quotes:
                    bad_quotes.write(quote + "\n")

        if DEBUG:
            print("Author: {}\nQuote: {}\nNouns: {}".format(author, quote, noun_list))
        return [author, quote, noun_list]

    def penisReplacement(self, quote):
        """
            Replace a random noun from the quote with penis
        """
        with open("input/used_quotes.txt", "a") as used_quotes:
            used_quotes.write(quote[1] + "\n")

        random_noun = random.choice(quote[2])
        if DEBUG:
            print("Random Noun: {}".format(random_noun))

        if random_noun[0].isupper():
            improved_quote = quote[1].replace(random_noun, 'Penis')
        else:
            improved_quote = quote[1].replace(random_noun, 'penis')

        # Build some custom tags or tag the author
        additional_tags = ''
        starwars_characters = ["Skywalker", "Kenobi", "Yoda", "Windu", "Palpatine", "Dooku", "Vader", "Amidala", "Organa", "Solo", "Jinn", "Fett", "C3PO", "R2D2", "Îmwe", "Gunray", "Watto", "Ackbar"]
        fast_and_furious_characters = ["Toretto", "Lue", "Pearce", "Tran", "Jesse", "O'Conner"]

        if quote[0] == "Elon Musk":
            quote[0] = "@elonmusk"
        elif quote[0] == "Bill Gates":
            quote[0] = "@BillGates"
        elif quote[0].split()[-1] in starwars_characters:
            additional_tags += " #starwars"
        elif quote[0].split()[-1] in fast_and_furious_characters:
            additional_tags += " #fastandfurious"

        # assemble tweet
        return ["\"{}\" - {}\n#penis #quote #motivational{}".format(improved_quote, quote[0], additional_tags), random_noun]

def main():
    try:
        bot = Bot("config/config.json")

        if not os.path.isfile("input/used_quotes.txt"):
            os.mknod("input/used_quotes.txt")

        if not os.path.isfile("input/bad_quotes.txt"):
            os.mknod("input/bad_quotes.txt")

        quote = bot.pullQuote()

        if(quote == "ERROR - NO MORE QUOTES! CONTACT MY HUMAN!"):
            if DEBUG:
                print(quote)
            else:
                bot.updateBotStatus(quote)
        else:
            improved_quote = bot.penisReplacement(quote)
            if DEBUG:
                print("Penis Quote: {}".format(improved_quote))
            else:
                bot.updateBotStatus(improved_quote[0])

        # Reply to most recent tweet with additional info
        if not DEBUG:
            recent_tweet = bot.api_client.user_timeline(id = bot.api_client.me().id, count = 1)[0]
            bot.api_client.update_status('@PenisQuoteBot Original Quote: {}\nPossible Replacements: {}\nSelected Replacement: {}'.format(quote[1], quote[2], improved_quote[1]), recent_tweet.id)
    except Exception as err:
        print("Hey bud, you got an error. ¯\_(ツ)_/¯ \n {0}\n\t{1}".format(err.with_traceback, err))
        sys.exit(-1)

# Program Entry Point
if __name__ == '__main__':
    main()