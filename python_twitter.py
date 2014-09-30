"""
Module: Module to get tweets.
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

TODO:
    Set alert functions.
    seems the info only for one month...
    remove the double quotes, user have to input double quote itself.

"""

import os, re, sys, time, datetime, copy, calendar
from twython import Twython

class TweetsReader(object):
    """ Class to get tweets for specific objects"""
    def __init__(self, search_list, exclude_list = []):
        """ Initialize the class. Take in the search list and exclude list and manipulate it to fit to search paramters
            The API key and access token are read from file. User need to create and specify the files to read.
            Args:
                search_list (list): list of search key phrases. (joined with OR eg A OR B).
            Kwargs:
                exclude_list (list): list of phrases to exclude (joined with - eg -C). Default empty.
        """
        self.search_list = search_list
        self.exclude_list = exclude_list

        ## user parameters
        self.app_key_file = r'c:\data\key_info\twitter_api_key.txt' 
        self.token_file = r'c:\data\key_info\twitter_token.txt' # store in file for access token.
        self.__load_api_and_access_token()

        ## twitter object and parameters.
        self.twitter_obj = Twython(self.app_key, access_token=self.access_token)

        ## paramters for twitter objects
        self.lang = 'en'
        self.result_type = 'mixed' #mixed, recent, popular
        self.result_count = 100 #max 100 per page, default 15
        #self.until ##for setting the date until YYYY-MM-DD

        ## form_search_str method
        self.twitter_search_query = ''
        self.form_seach_str_query() #form the search str at initialization

        ## Results storge
        self.search_results = [] # list of list with 1st item as date and 2nd item as results.
        
    def __load_api_and_access_token(self):
        """ Load the access token from file in self.token_file.
            Set to self.access_token.
        """
        with open(self.app_key_file, 'r') as f:
            self.app_key = f.read()

        with open(self.token_file, 'r') as f:
            self.access_token = f.read()

    def form_seach_str_query(self):
        """ Form the full query that is going to input to twitter object.
        """
        self.twitter_search_query = self.join_all_search_list() + ' ' + self.join_all_exclude_list()

    def join_all_search_list(self):
        """ Take all the items in self.search_list and concat it with "OR".
            Leave a space between items.
            For each item, treat it as one word so add the open and close quotes "".
            Returns:
                (str): concatenated str.
        """
        return " OR ".join(self.search_list)

    def join_all_exclude_list(self):
        """ Take all the items in self.exclude_list and concat it with "-".
            Leave a space for the previous item and no space for next item.
            For each item, treat it as one word so add the open and close quotes "".
            Returns:
                (str): concatenated str.
        """
        if self.exclude_list ==[]:
            return ''
        else:
            return '-' + " -".join(self.exclude_list)

    def set_num_result_to_retrieve(self, count):
        """ Set the twitter object number of results to return.
            Args:
                count (int): num of results.
        """
        self.result_count = count

    def convert_date_str_to_date_key(self, date_str):
        """ Convert the date str given by twiiter [created_at] to date key in format YYYY-MM-DD.
            Args:
                date_str (str): date str in format given by twitter. 'Mon Sep 29 07:00:10 +0000 2014'
            Returns:
                (int): date key in format YYYYMMDD
        """
        date_list = date_str.split()
        
        month_dict = {v: '0'+str(k) for k,v in enumerate(calendar.month_abbr) if k <10}
        month_dict.update({v:str(k) for k,v in enumerate(calendar.month_abbr) if k >=10})

        return int(date_list[5] + month_dict[date_list[1]] + date_list[2])

    def perform_twitter_search(self):
        """ Perform twitter search by calling the self.twitter_obj.search function.
            Ensure the setting for search such as lang, count are being set.
            Will store the create date and the contents of each tweets.
        """
        for n in self.twitter_obj.search(q=self.twitter_search_query, lang = self.lang,
                                         count= self.result_count, result_type = self.result_type)["statuses"]:
            # store the date
            date_key =  self.convert_date_str_to_date_key(n['created_at'])
            contents = n['text'].encode(errors = 'ignore')
            self.search_results.append([date_key, contents])

    def print_results(self):
        """ Print results."""
        for n in self.search_results:
            print 'Date: ', n[0]
            print n[1]
            print '#'*18

    def count_num_tweets_per_day(self):
        """ Count the number of tweets per day present. Only include the days where there are at least one tweets,.
        """
        day_info = [n[0] for n in self.search_results]
        date_df = pandas.DataFrame(day_info)
        grouped_date_info = date_df.groupby(0).size()
        date_group_data = zip(list(grouped_date_info.index), list(grouped_date_info.values))
        for date, count in date_group_data:
            print date,' ', count
        

if __name__ == '__main__':

    """ Running the twitter 
    """
    
    choice = 2

    if choice ==1:
        search_list = ['apple','meat','kiwi',]
        exclude_list = ['orange','kok']

        hh = TweetsReader(search_list, exclude_list)
        print hh.twitter_search_query
        hh.perform_twitter_search()
        hh.print_results()
    
    if choice == 2:
        """Particularly for stocks. """        
        search_list = ['sheng siong shares']
        exclude_list = []

        hh = TweetsReader(search_list, exclude_list)
        print hh.twitter_search_query
        hh.perform_twitter_search()
        hh.print_results()
        print
        hh.count_num_tweets_per_day()



