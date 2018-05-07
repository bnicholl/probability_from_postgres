#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 23:17:59 2018

@author: bennicholl
"""

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
from collections import Counter 


# get connected to the database
connection = pg.connect("dbname=mydb user=bennicholl")

test_set = pd.read_sql_query("SELECT * FROM test LIMIT 1000000", connection)   
"""this simply gets the probability of an app downloaded after a click on an add has occured""" 
def probability_app_downloaded(test_set = test_set):
    get_number_downloaded_apps = len(pd.read_sql_query("SELECT * FROM ads_sample WHERE is_attributed = 1",connection))
    get_number_data = len(pd.read_sql_query("SELECT * FROM ads_sample",connection))
    probability_app_downloaded = get_number_downloaded_apps / get_number_data
    return probability_app_downloaded

"""this function iterates through our test set based on ip address, and extracts all the training examples that
have the same ip adress as our current iterative. we than calculate P (APP DOWNLOADED | GIVEN IP ADRESS) * P(IP APP DOWNLOADED),
and save it in a csv file"""   
"""prob_app_downloaded argument should be the ouput of probability_app_downloaded() function above"""
def bayes(prob_app_downloaded, test_set = test_set):
    
    df = pd.DataFrame(columns = ['click_id', 'is_attributed'])
    """this is simply to ensure our prob_app_downloaded_given_id variable doesnt have a 
    0 in the numerator"""
    alpha = .01    
    
    for e,i in enumerate(test_set['ip']):
        """get all the ip's in the current iteration of the training set"""
        get_data = pd.read_sql_query("SELECT * FROM ads_sample WHERE ip = {}".format(i), connection)

        total_ip_returned = len(get_data)
        """ensures an ip cooresponding to the test data is found within our training data"""
        if total_ip_returned > 0:
            """gets rows where an app was downloaded"""
            get_number_of_downloads = get_data[get_data['is_attributed'] == 1]
            #P(APP DOWNLOADED | GIVEN IP ADRESS)
            prob_app_downloaded_given_ip = (len(get_number_of_downloads)+ alpha)/total_ip_returned
            #P(APP DOWNLOADED | GIVEN IP ADRESS) * P(IP APP DOWNLOADED)
            is_attributed = prob_app_downloaded_given_ip * prob_app_downloaded
            click_id = test_set.loc[e]['click_id']

            df.loc[click_id] = click_id
            df.loc[click_id]['is_attributed'] = format(is_attributed, 'f')
              
    df.to_csv('/Users/bennicholl/Desktop/datasets/probabilities.csv', sep=',', index = False)
    
    
        
        
        


