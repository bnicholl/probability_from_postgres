# probability_from_postgres
Kaggle competition where the goal is to create an algorithm that detects the probability that an app was downloaded given an add was clicked

You can download the data here https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/data

As of right now, this algorithm counts the words in a given text, and than calculates the probability of each individual word in the given text.
We have a couple million rows of testing data. Lets go ahaed and print our 20 rows to give an idea of what it is composed of:

![input](https://github.com/bnicholl/probability_from_postgres/blob/master/Screen%20Shot%202018-05-07%20at%2011.15.08%20PM.png)

Our training data has 186 million rows!!! Lets go ahead and print out a few rows to get a glimpse at what our traingin data looks like:

![input](https://github.com/bnicholl/probability_from_postgres/blob/master/Screen%20Shot%202018-05-07%20at%2011.27.22%20PM.png)
is_attributed cooresponds to whether an app has been downloaded or not. 0 means no downlad, 1 means app has been downloaded. This algorithm looks up an ip adress from the testing data in our postgres DB, gets the rows from the training data with the same IP adress, which is also in our postgres DB, then calcualtes the probability of that app being downloaded. The probability function is: P(APP DOWNLOADED | GIVEN IP ADRESS) * P(APP WAS DOWNLOADED).  Our output should be a csv file. Lets take a look at what the values look like:

![input](https://github.com/bnicholl/probability_from_postgres/blob/master/Screen%20Shot%202018-05-07%20at%2011.37.58%20PM.png)
