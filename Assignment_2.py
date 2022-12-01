import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import re
import spacy
from nltk.stem.snowball import SnowballStemmer
import seaborn as sns
nlp = spacy.load('en_core_web_lg')
# Data visualization libraries is from Alex The Analyst: https://github.com/AlexTheAnalyst/PythonCode
# Youtube video link: https://www.youtube.com/watch?v=MpIi4HtCiVk

# My keys
api_key = '9wms5HEYDQE1GN1SlmmD1kQx8'
api_key_secret = '8KJemWNwgBGnoTwGhfWRWgWxrtVbV27MomTYVT3TjW6vUdK4II'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAER5hgEAAAAARFKp0c63ZIDx3cj2lYOue9cZkGg%3DMAxqHVpi1coHadnGhWNh7ux9zg2pNFKA9FSpw079U3mhkAOFb6'
access_token = '1575447678602862593-Mp59GyrjnYF5QZeITQL4Hmv9T17UC0'
access_token_secret = '2EXJZatdlCK6snWtbIMcszJm3guImfT3ysmPgOsenaXbg'
# Setting my keys
author = tweepy.OAuthHandler(api_key, api_key_secret)
author.set_access_token(access_token, access_token_secret)
api = tweepy.API(author)
client = tweepy.Client(bearer_token=bearer_token)
'''
# Last 100 twitter accounts that mentioned Elon Musk starting from the date 2022/10/03
users=client.get_users_mentions(id='44196397',max_results=100,start_time='2022-10-03T00:00:01Z')
for user in users.data:
    print(user['id'],user['text'])
# Getting Elon Musk's latest tweets
tweets=client.get_users_tweets(id='44196397',max_results=100,start_time='2022-10-03T00:00:01Z')
for tweet in tweets.data:
    print(tweet['id'],tweet['text'])
# People who liked Elon Musk's last tweet
users = client.get_liking_users(id='1576998577758666752')
for user in users.data:
    print(user.username)
'''
# Data visualization from all the Elon Musk's tweets
# Getting all the Elon Musk's tweets posted until today
total_tweets = 20000
ptr = tweepy.Cursor(api.user_timeline, screen_name="elonmusk",
                    tweet_mode="extended").items(total_tweets)
# Creating list for the tweet, likes for the tweets and the date tweets are posted.
tweets = []
likes = []
date = []
for i in ptr:
    tweets.append(i.full_text)
    likes.append(int(i.favorite_count))
    date.append(i.created_at)
# Creating data frame from the lists
data_frame = pd.DataFrame({'tweets': tweets, 'likes': likes, 'post day': date})
# Deleting all the retweets from the data frame
data_frame = data_frame[~data_frame.tweets.str.contains("RT")]
# Printing the data frame existing up to 3200 tweets (no retweets included)
print(data_frame)
# Most 10 liked tweets of Elon Musk for the past 20,000 tweets in my data frame
most_liked_tweets = data_frame.loc[data_frame.likes.nlargest(10).index]
# Printing most 10 liked tweets of Elon Musk
print("\n\nMost 10 liked tweets of Elon Musk\n")
print(most_liked_tweets)
# Here I wanted to visulize data from all the data I gained from the Elon Musk's twitter account
# Extracting all the individial words from the tweets
list_of_sentences = list(data_frame.tweets)
lines = []
for sentence in list_of_sentences:
    words = sentence.split()
    for word in words:
        lines.append(word)
lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]
# Deleting empty words
lines2 = []
for word in lines:
    if word != '':
        lines2.append(word)
# Here I use an external library to get rid of the short words such as 'a' 'ab' 'on' 'the' etc.
# Also getting rid of the most used words in english such as 'okay', 'yes', 'n', 'and' etc.
s_stemmer = SnowballStemmer(language='english')
stem = []
for word in lines2:
    stem.append(s_stemmer.stem(word))
stem2 = []
for word in stem:
    if word not in nlp.Defaults.stop_words:
        stem2.append(word)
df2 = pd.DataFrame(stem2)
df2 = df2[0].value_counts()
# Visualizing the data for the top words using external visualizing graph (it looks cool)
df2 = df2[:20,]
plt.figure(figsize=(10,5))
sns.barplot(x=df2.values, y=df2.index, alpha=1)
plt.title('Top Words Used by Elon Musk')
plt.ylabel('Word from Tweet',fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()
# This time visualizing the data for the top organization used in the tweets
def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text + ' - ' + ent.label_ + ' - ' + str(spacy.explain(ent.label_)))
str1 = " "
stem2 = str1.join(lines2)
stem2 = nlp(stem2)
label = [(X.text, X.label_) for X in stem2.ents]
df6 = pd.DataFrame(label, columns = ['Word','Entity'])
df7 = df6.where(df6['Entity'] == 'ORG')
df7 = df7['Word'].value_counts()
# Plotting
dfx = df7[:20,]
plt.figure(figsize=(10,5))
sns.barplot(x=dfx.values, y=dfx.index, alpha=1)
plt.title('Top Organizations Mentioned by Elon Musk')
plt.ylabel('Word from Tweet',fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()
# Here I visualize the data for the top people used in the tweets
str1 = " "
stem2 = str1.join(lines2)
stem2 = nlp(stem2)
label = [(X.text, X.label_) for X in stem2.ents]
df10 = pd.DataFrame(label, columns = ['Word','Entity'])
df10 = df10.where(df10['Entity'] == 'PERSON')
df11 = df10['Word'].value_counts()
# Plotting
dfy = df11[:20,]
plt.figure(figsize=(10,5))
sns.barplot(x=dfy.values, y=dfy.index, alpha=1)
plt.title('Top People Mentioned by Elon Musk')
plt.ylabel('Word from Tweet',fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()
