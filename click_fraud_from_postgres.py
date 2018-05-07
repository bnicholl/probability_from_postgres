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

#df = psql.read_sql("SELECT * FROM ads_sample WHERE click_time = '2017-11-07' " , connection)

#data = psql.read_sql("SELECT * FROM ads_sample WHERE attributed_time IS NOT NULL " , connection)

offset = 0
limit = 100
#dframe = pd.read_sql_query("SELECT * FROM ads_tracker limit {} offset {}".format(limit,offset), connection)
#dframe = pd.read_sql_query("SELECT * FROM ads_sample WHERE attributed_time IS NOT NULL", connection)

#test_jern = pd.read_sql_query("SELECT * FROM ads_sample WHERE ip = {}".format(5281), connection)


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
    
    



"""this returns ip adress as the key, a value pertaining to amount of times an ip adress clicked on an add
as the first value, the amount of times an ip adress downloaded an app as the second value, a list of the 
channels per ip adress as the third value, and a list pertaining to the amount of times a respective channel
was called as the 4th value. The 3rd and 4th list are element wise cooresponded"""
def dic():
    
    offset = 0
    limit = 10
    """dictionary all our information goes into"""
    ip_occurence = {}
        
    dframe = pd.read_sql_query("SELECT * FROM ads_sample limit 500 offset 0", connection)
    
    
    """add whatever our limit is to our offest in our DB"""
    offset += limit
    
    for e,i in enumerate(dframe['ip']):
        """if our ip adress is already in our dictionary"""
        if i in ip_occurence:
            """add 1 to how many times our ip adress clicked on an add"""
            ip_occurence[i][0] += 1
                                                
            """if our app_downloaded column == 1, than an app was downloaded!"""
            if dframe['is_attributed'][e] != 0:
                """add one to our app downloaded value"""                    
                ip_occurence[i][1] += 1  
                
                """check if our channel is not in our dicitonary"""
                if dframe['channel'][e] not in ip_occurence[i][2]:
                    """append the channel to the channel list"""
                    ip_occurence[i][2].append(dframe['channel'][e])
                    """append a 1 to the countof channels to app downloads list"""
                    ip_occurence[i][3].append(1)
                
                    """if our channel is in our dicitonary"""
                else:# dframe['channel'][e] in ip_occurence[i][2]:
                    """gets the location of where our channel is in our channels list"""
                    for i in dframe['channel']:
                        """this itrates through ip_occurences key's"""
                        for e, ii  in enumerate(ip_occurence):
                            """Example of ip_occurence[ii][2] : ip_occurence[224120][2]"""
                            if i == ip_occurence[ii][2]:
                                print(e)
                                """add 1 to the count of channels to app downloads list"""
                                ip_occurence[ii][3] += 1
                                break             
            else:
                """append the channel to the channel list"""
                ip_occurence[i][2].append(dframe['channel'][e])  
                """append a 0 to the countof channels to app downloads list"""
                ip_occurence[i][3].append(0)                               
            
        else:
            """this instates our first occurence as 1"""
            ip_occurence[i] = [1]
            """this appends the 0 or 1 pertaining to whether an app was downloaded""" 
            ip_occurence[i].append(dframe['is_attributed'][e])
            """this appends the respectve channel"""
            ip_occurence[i].append([dframe['channel'][e]])
            """checks if the current ip[key] value associated with whether a app was
            downloaded or not is == 1, thus an app was downloaded"""
            if ip_occurence[i][1] == 1:
                """this appends a 1, signifiying, the newly appended channel is associated 
                with an app that was downloaded"""
                ip_occurence[i].append([1])
            else:
                ip_occurence[i].append([0])
                               
    return ip_occurence



# count number of times a channel appears in our dic object
#aa = [a[i][2][0] for i in a]
#cnt = Counter(aa)
    
        
        
        
        
        
        
        


