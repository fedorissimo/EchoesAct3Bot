from youdotcom import Chat

chat = Chat.send_message(message="how is your day?", api_key="YOUR API KEY HERE") # send a message to YouChat. passing the message and your api key.

# you can get an api key form the site: https://api.betterapi.net/ (with is also made by me)

print(chat)  # returns the message and some other data