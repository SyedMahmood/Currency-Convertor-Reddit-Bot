#This is a bot for Reddit. Upon seeing the phrase "PleaseConvert" the bot will convert an 
#amount to a certain desired currency. An example format to use the bot is: "PleaseConvert: 10 USD to CAS"

#This bot uses the Fixer.io JSON API to get the latest currency rates. 

import praw
import time
import urllib2
import json


#User specifications:

MAX_NUMBER_COMMENTS = 10
USER_AGENT = "/u/csstudent72 reddit bot to convert currency"
USER_NAME = ""
PASSWORD = ""
DESIRED_SUBREDDIT = "test"


#Parameters: 
#base - the currency that we are stating
#newCurrency - the currency we want to convert to 
#amount - the amount we are stating in our base currency
# return the amount converted to new currency
def convert_currency(amount, base, newCurrency):
    link = 'http://api.fixer.io/latest?base=' + base
    jsonObject = urllib2.urlopen(link)
    
    currencies = json.load(jsonObject)

    conversion_rates = currencies['rates']
    conversion_factor = conversion_rates[newCurrency]

    return amount * conversion_factor


#Logging into reddit using entered Username and password.
r = praw.Reddit(USER_AGENT)
if USER_NAME == "" and PASSWORD == "":
    r.login()
else: 
    r.login(USER_NAME, PASSWORD)

#A list to store comments that have already been replied to or read.
comment_memory = []


#The currency covertor bot method.
def curr_convertor_bot():
    print("Setting up the appropriate subreddit...")

    #Getting the desired subreddit whose comments the bot will reply to.
    subreddit = r.get_subreddit(DESIRED_SUBREDDIT)

    print("Getting the comments now...")

    #Obtaining a list of the comments.
    comment_list = subreddit.get_comments(limit = MAX_NUMBER_COMMENTS)

    for comment in comment_list:
        comment_text = comment.body
        comment_text_list = comment_text.split(" ")
    
        if 'PleaseConvert:' in comment_text_list and comment.id not in comment_memory:
            print("We have found a comment that wants us to do a conversion!")
            indexOfAmount = comment_text_list.index('PleaseConvert:') + 1
            
            #Gather information from each comment that wants the bot to do a conversion. 
            base_amount = int(comment_text_list[indexOfAmount])
            base_currency = comment_text_list[indexOfAmount + 1]
            desired_currency = comment_text_list[indexOfAmount + 3]

            desired_amount = convert_currency(base_amount, base_currency, desired_currency)

            comment.reply('That is ' + str(desired_amount) + " " + desired_currency)

            print('We have replied to the comment.')

            comment_memory.append(comment.id)
    print("We have finished replying to this set of comments. Time to start again in 10 seconds")


#Run the bot and have it sleep for 10 seconds at a time.
while True:
	curr_convertor_bot()
	time.sleep(10)
