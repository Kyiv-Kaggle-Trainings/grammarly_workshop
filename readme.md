# Description

This is an approximate implementation of the article https://www.researchgate.net/publication/220812054_Web-Scale_N-gram_Models_for_Lexical_Disambiguation

# Tasks

 - Try to understand the implementation
 - Print the most common preposition itself
 - Try different values of 'C' parameter for LinearSVC (0.01, 0.001)
 - Try replacing LinearSVC with RandomForestClassifier
 - Plot quality depending on train data size
 - Try implementing SumLM (simply sum all the frequency logarithms for each preposition and choose maximum without LinearSVC)
 - Try SumLM starting with n-grams of order 3
