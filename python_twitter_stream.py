
"""
Module: Module for tweets streaming
Author: Tan Kok Hua

Requires:
    Twython
    Pandas (For further processing)

Learning:
    twitter function parameters
    https://dev.twitter.com/rest/reference/get/search/tweets

    Twython tutorial
    http://www.silkstream.net/blog/2014/06/retweeting-with-your-twython-twitter-bot.html

    using twitter keyword hacks (such as OR etc) in using OR or - to exclude kewyord

    Adv search with twitter
    https://support.twitter.com/articles/71577-using-advanced-search

    python twitter streamer
    http://www.kalisch.biz/2013/10/harvesting-twitter-with-python/

    twitter and encoding
    http://www.quartertothree.com/game-talk/showthread.php?73978-Data-mining-Twitter-for-sentiments-about-the-new-consoles
    
    preprint a file
    http://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file

    pandas creating dataframe , no index error
    http://stackoverflow.com/questions/17839973/construct-pandas-dataframe-from-values-in-variables
    
        

"""

import os, re, sys, time, datetime, copy, calendar
import fileinput
import pandas
from twython import Twython
from twython import TwythonStreamer

class TweetStreamer(TwythonStreamer):
    def __init__(self, *args):
        super(TweetStreamer, self).__init__(*args)

        self.counter = 3 #control the number of feeds
        self.data_save_file = r'c:\data\temp\tweets_save.csv' #try saving as csv format
        self.enable_counter = 0 #if 1, will limit the counter

    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')
            self.savetweet(data)
            
            self.counter = self.counter -1
            if self.counter == 0:
                sys.exit()

            #need a way to store all the feds

    def on_error(self, status_code, data):
        print status_code

    def savetweet(self, data):
        """ Save data to a csv.
            check if csv exists, if exists, append the data, if not create a new file.
            Use pandas for saving.
            Args:
                data (dict): dict of tweet.        
        """
        self.data = data

        #create data to a dataframe for storing
        #some might have multiple dict --> need to remove
        data.pop("user", None)
        data.pop("retweeted_status", None)
        data.pop("entities", None)
        
        data_df = pandas.DataFrame(data, index =[0])
        print len(data_df)
        self.data_df = data_df

        #set target column
        target_columns = ['created_at','geo','text','timestamp_ms']
        data_df = data_df[target_columns]

        if os.path.isfile(self.data_save_file):
            with open(self.data_save_file, 'a') as f:
                data_df.to_csv(f, header=False, index =False,  encoding='utf-8')
        else:
             data_df.to_csv(self.data_save_file, index =False, encoding='utf-8')
            

"""
['contributors', 'truncated', 'text', 'in_reply_to_status_id', 'id', 'favorite_c
ount', 'source', 'retweeted', 'coordinates', 'timestamp_ms', 'entities', 'in_rep
ly_to_screen_name', 'id_str', 'retweet_count', 'in_reply_to_user_id', 'favorited
', 'retweeted_status', 'user', 'geo', 'in_reply_to_user_id_str', 'possibly_sensi
tive', 'lang', 'created_at', 'filter_level', 'in_reply_to_status_id_str', 'place
', 'extended_entities']





contributors None
truncated False
text #GE2015
Her officials within her are roaring lions;
her rulers are evening wolves,who leave nothing for the morning.(Zephaniah3:3)
NO PEACE!
in_reply_to_status_id None
id 640386379361349632
favorite_count 0
source <a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>
retweeted False
coordinates None
timestamp_ms 1441514985300
entities {'user_mentions': [], 'symbols': [], 'trends': [], 'hashtags': [{'indic
es': [0, 7], 'text': 'GE2015'}], 'urls': []}
in_reply_to_screen_name None
id_str 640386379361349632
retweet_count 0
in_reply_to_user_id None
favorited False
user {'follow_request_sent': None, 'profile_use_background_image': True, 'defaul
t_profile_image': False, 'id': 3146015578L, 'verified': False, 'profile_image_ur
l_https': 'https://pbs.twimg.com/profile_images/585602376507228161/xLkCZqxS_norm
al.png', 'profile_sidebar_fill_color': '000000', 'profile_text_color': '000000',
 'followers_count': 177, 'profile_sidebar_border_color': '000000', 'id_str': '31
46015578', 'profile_background_color': 'B2DFDA', 'listed_count': 12, 'profile_ba
ckground_image_url_https': 'https://abs.twimg.com/images/themes/theme13/bg.gif',
 'utc_offset': None, 'statuses_count': 2015, 'description': 'Specialist Engineer
ing, Contracts, Claims & Legal Consultant. First tweeted on 7 April 2015', 'frie
nds_count': 268, 'location': 'UK, Singapore & Malaysia', 'profile_link_color': '
3B94D9', 'profile_image_url': 'http://pbs.twimg.com/profile_images/5856023765072
28161/xLkCZqxS_normal.png', 'following': None, 'geo_enabled': False, 'profile_ba
nner_url': 'https://pbs.twimg.com/profile_banners/3146015578/1431060881', 'profi
le_background_image_url': 'http://abs.twimg.com/images/themes/theme13/bg.gif', '
name': 'Daniel Greenwood', 'lang': 'en', 'profile_background_tile': False, 'favo
urites_count': 1924, 'screen_name': 'DGreenwood38', 'notifications': None, 'url'
: None, 'created_at': 'Wed Apr 08 00:34:07 +0000 2015', 'contributors_enabled':
False, 'time_zone': None, 'protected': False, 'default_profile': False, 'is_tran
slator': False}
geo None
in_reply_to_user_id_str None
possibly_sensitive False
lang en
created_at Sun Sep 06 04:49:45 +0000 2015
filter_level low
in_reply_to_status_id_str None
place None

c:\pythonuserfiles\Python_Twitter>

"""
if __name__ == '__main__':

    """ Running the twitter 
    """
    
    choice = 6


    if choice ==6:

        auth_file_path = {
                            'APP_KEY' : r'C:\data\key_info\streamer_api_key.txt',
                            'APP_SECRET' : r'C:\data\key_info\streamer_api_secret.txt',
                            'OAUTH_TOKEN' : r'C:\data\key_info\streamer_oauth_token.txt',
                            'OAUTH_TOKEN_SECRET' : r'C:\data\key_info\streamer_oauth_token_secret.txt'
                            }
        
        auth_key = {}
        for n in auth_file_path.keys():
            with open(auth_file_path[n],'r') as f:
                auth_key[n] =f.read()

        stream = TweetStreamer(auth_key['APP_KEY'], auth_key['APP_SECRET'],
                            auth_key['OAUTH_TOKEN'], auth_key['OAUTH_TOKEN_SECRET'])


        target_search_list = ['#ge2015','#GE2015','#PAP','#sgelections',\
                              '#sgelection','#SDP','#WP','#SPP','#SGelections',\
                              '#sgpolitics']
        stream.statuses.filter(track=target_search_list)




    if choice ==4:
        """
            Create a new app key and app key scret (based on consumer key and consumer key secret)
            Set the application to be able to read and write
            And obtain the corresponding token.
            Use the oauth1 method given in below site:
            https://twython.readthedocs.org/en/latest/usage/starting_out.html#oauth1
            retrieve temp oauth token and secret.
            Get the verification url and go to url to get verfication code
            and re-enter to obtain final oauth token and secret.

            Possible issues:
            http://stackoverflow.com/questions/17438943/twython-oauth1-issues-401-error-using-example-code
            use consumer key and consumer secret
            401 issues --> need to use the url to authorize the token and set the final autho token

            Code for oauth1 setup as below.
            
        """

        app_key_file = r'c:\data\key_info\twitter_api_key.txt' 
        token_file = r'c:\data\key_info\twitter_token.txt' # store in file for access token.
        
        with open(app_key_file, 'r') as f:
            APP_KEY = f.read()

            
        with open(token_file, 'r') as f:
            APP_SECRET = f.read()

            
        twitter = Twython(APP_KEY, APP_SECRET)
        auth = twitter.get_authentication_tokens()

        OAUTH_TOKEN = auth['oauth_token']
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

        print auth['auth_url'] #go to website to obtain the verification code

        oauth_verifier = ''#enter the number here

        twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        OAUTH_TOKEN = final_step['oauth_token']
        OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

        # save the final oauth token and secret.




    if choice ==7:
        """ Saving data to file.. Most updated data on top
            Use seek(0 to write to top??
            Not able to do

            try below for preprint
            http://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file

        """
        trial_name = r'C:\data\temp\trial_data.txt'
        sent1 = 'sent1'
        sent2 = 'sent2'

        def line_pre_adder(filename, line_to_prepend):
            f = fileinput.input(filename, inplace=1)
            for xline in f:
                if f.isfirstline():
                    print line_to_prepend.rstrip('\r\n') + '\n' + xline,
                else:
                    print xline
                    
        line_pre_adder(trial_name, sent1)
        line_pre_adder(trial_name, sent2)