consumer_key= 'ODvJ1KPeOx94XV079rObrmCsn'
consumer_secret= 'ss56CMap6hlBBVpPAc8W06SchB3nzKcJvE555qLotBChqHZ0rp'
access_token='113446949-8QAaLJin0pDS1htsG6f7Gd7UAH5vAX3RmCCEHitP'
access_token_secret='tQnKIUIMZobrDTK8zlja0XqQN7cOHHbvdrAtLanW02fnF'

import tweepy
import csv

from textblob import TextBlob

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class Candidate(object):
	name = ""
	polarity = 0
	subjectivity = 0
	tweets = ""
	
	def __init__(self, name, polarity=0, subjectivity=0):
        	self.name	=	name
        	self.polarity = polarity
        	self.subjectivity = subjectivity
        	self.tweets = api.search("#"+name)	

Candidates = [Candidate('Trump'),Candidate('Hillary')]


with open('election_sentiment.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"',	quoting=csv.QUOTE_MINIMAL)
                            
    i=0
    a=0
    polarity = 0
    subjectivity = 0
    for Candidate in Candidates:	
		for	tweet in Candidate.tweets:	
			analysis = TextBlob(tweet.text)
    			writer.writerow([
    			Candidate.name,	
    			i,
    			analysis.sentiment.subjectivity,	
    			analysis.sentiment.polarity,	
    			tweet.text.encode('utf-8').replace(","," ").replace('\n', ' ').replace('\r', '')	
    			])
    			i+=1
    			subjectivity+=analysis.sentiment.subjectivity
    			polarity+=analysis.sentiment.polarity			
		Candidate.polarity = (polarity/i)
		Candidate.subjectivity = (subjectivity/i)
		print("")
		print("Candidate : "+Candidate.name)
		print("Average Tweet Polarity : ",Candidate.polarity)
		print("Average Tweet Subjectivity : ",Candidate.subjectivity)
		print("Results based on ",(i)," tweets")
		i=0
		a+=1

Max = 0
Winner = ""
for Candidate in Candidates:
	if Candidate.polarity > Max:
		Max = Candidate.polarity 
		Winner = Candidate.name

print("")
print("The winner of the 2016 Election based on Twitter sentiment is "+Winner)
print("")
print("The results can be found in election_sentiment.csv")
print("")