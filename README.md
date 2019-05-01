# Final_Project
IS590PR Spring 2019

# Team Member(s)
Gaurav Dharra - gdharra2

# Background
Various voting systems are being studied to determine an effective system for selecting the most eligible and suitable candidate. The different systems include plurality, runoff, Borda, Condorcet, and score voting. The below description provides a brief understanding of the various systems stated:

1. Plurality: The simplest system wherein each person casts one vote for their favorite candidate and the candidate with the most votes wins.
2. Runoff: It is similar to plurality except that, after the first round of voting, the candidate with the least votes is eliminated and the election is repeated with the remaining candidates.
3. Borda: In this system, voters don’t vote for a single candidate, rather they rank the candidates and each candidate receives points respective to their rank.
4. Condocert: It runs pairwise popular elections between every possible pair of candidates. If a single candidate beats all others in these pairwise elections, that candidate is the winner.
5. Score Voting: A system in which each voter gives each candidate a score on some scale and the candidate with the highest average score wins. One noteworthy difference of this system is that it does not require any ranking of the candidates since a voter can give multiple candidates the same score.

# Hypothesis
1. The Condorcet system of voting may work the best in selecting a suitable candidate since every candidate is ranked with every other pair of candidates and the most favorable candidate gets to win.
2. The Score Voting is vulnerable to strategic manipulation since the score is very subjective and quantitative. 

# Libraries used
1. import random
2. import pandas as pd
3. import operator
4. import multiprocessing as mp

# Method used
1. Candidates – A random set of candidates are chosen that will be contesting for the election. Each candidate is assigned a random fame score that signifies popularity. (Created as class objects of class Candidates)

2. Voters – A random set of 10000 voters are generated each having a unique voter id and a randomly generated preferential score. This randomly generated preferential score is compared with each candidate fame score to generate preference value for each candidate. (Created as class objects of class Voters) 

3. Expected Winner – This is computed purely based on summation of the preferential scores of all the voters.

4. Generation of votes – 
   * Honest Voters: Votes are generated based on the preferential score provided by the candidate
   * Strategic Manipulation in voting: The concept of strategic manipulation is introduced by changing votes of  random voters to a famous candidate instead of their preferred candidate. (25%)

5. A method exist for all voting systems to generate the winning candidate

6. The next step involves simulating the whole process 100 times to 
   * Compute probability of each voting system generating the expected winner
   * Identify effect of strategic manipulation on each voting system

7. Parallel Processing was used to simulate the results using a multiprocessing module of python library to make an async call to the run_simulation() method.

8. Based on the number of times a voting system produced an accurate result, the probability of generating the expected results was computed and is tabulated as shown in the results section.


# References
https://dss.berkeley.edu/blog/voting-systems.html
