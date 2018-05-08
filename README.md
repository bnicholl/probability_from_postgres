# probability_from_postgres
Kaggle competition where the goal is to create an algorithm that detects the probability that an app was downloaded given an add was clicked

You can download the data here https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/data

As of right now, this algorithm counts the words in a given text, and than calculates the probability of each individual word in the given text.
We have a couple million rows of testing data. Lets go ahaed and print our 20 rows to give an idea of what it is composed of:

![input](https://github.com/bnicholl/probability_from_postgres/blob/master/Screen%20Shot%202018-05-07%20at%2011.15.08%20PM.png)

Now here is an example of what our training data looks like:
