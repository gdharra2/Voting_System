import csv
import pickle
import us
import numpy as np
from scipy.stats import norm

try:
    from numpy import random_intel as random  # Use Intel random if available
except ImportError:
    from numpy import random

import pollster
from pollster.rest import ApiException

# Get state names from us.STATES
states = {state.abbr: state.name for state in us.STATES}
print('states',states)

# Read electoral college votes from csv file
# https://raw.githubusercontent.com/chris-taylor/USElection/master/data/electoral-college-votes.csv
with open('electoral-college-votes.csv') as csvfile:
    reader = csv.reader(csvfile)
    college = {row[0]: int(row[1]) for row in reader}

# Initialize Pollster API
pollster = pollster.Api()

cursor = None                # str | Special string to index into the Array (optional)
tags = '2016-president'                # str | Comma-separated list of tag slugs. Only Charts with one or more of these tags and Charts based on Questions with one or more of these tags will be returned. (optional)
election_date = '2016-11-01' # date | Date of an election

try:
    # Charts
    charts = pollster.charts_get(cursor=cursor, tags=tags, election_date=election_date)
    # print(charts)
except ApiException as e:
    print("Exception when calling DefaultApi->charts_get: %s\n" % e)
# Save polls by pickle
pickle.dump(charts, open('charts.p', 'wb'))

question_slug = next(c.question.slug for c in charts.items if c.question.n_polls > 30)

polls = pollster.polls_get(
  question=question_slug,
  sort='created_at'
)
#print(polls.items)

state_polls = [questions
               for poll in polls.items for questions in poll.poll_questions
               if questions.question.name.partition(' Presidential')[0].replace('2016 ','').title() in states.values()]
print(state_polls)

for each_poll in state_polls:
    each_poll.question.state = each_poll.question.name.partition(' Presidential')[0].replace('2016 ','').title()

polls_by_state_counts = {state: sum(each_poll.question.state == state for each_poll in state_polls)
                                    for state in states.values()}

print(polls_by_state_counts)


# Each state is a dictionary of arrays
# obs: poll size
# dem: Democrat popular vote percentage
# rep: Republican popular vote percentage
# other: Other popular vote percentage
polls_by_state = {state: {'obs':[], 'dem':[], 'rep':[], 'other':[]} for state in states.values()}
for question in state_polls:
    state = question.question.state
    obs = question.sample_subpopulations[0].observations
    dem = ''
    rep = ''
    other = 0.0
    for response in question.sample_subpopulations[0].responses:
        if response.text == 'Clinton':
            dem = response.value
        if response.text == 'Trump':
            rep = response.value
        if response.text == 'Other':
            other = response.value
    # Check for empty responses
    if state and obs and dem and rep:
        polls_by_state[state]['obs'].append(obs)
        polls_by_state[state]['dem'].append(dem)
        polls_by_state[state]['rep'].append(rep)
        polls_by_state[state]['other'].append(other)

print(polls_by_state)

state_mean_dem = {}
state_std_dem = {}
state_cdf_dem = {}

state_mean_rep = {}
state_std_rep = {}
state_cdf_rep = {}

for state, poll in polls_by_state.items():
    dem = np.array(poll['dem'])
    rep = np.array(poll['rep'])
    other = np.array(poll['other'])
    obs = np.array(poll['obs'])
    dem_mean = 0.0
    rep_mean = 0.0
    other_mean = 0.0
    if dem.size > 0:
        dem_mean = np.average(dem, weights=obs)
    if rep.size > 0:
        rep_mean = np.average(rep, weights=obs)
    if other.size > 0:
        other_mean = np.average(other, weights=obs)

    if dem_mean != 0.0 and rep_mean != 0.0:
        state_mean_dem[state] = dem_mean / (dem_mean + rep_mean + other_mean) * 100

        state_std_dem[state] = np.sqrt(np.average(np.square(dem - dem_mean) +
                                                  (100 - dem) * dem / 10000, weights=obs)) / (dem_mean + rep_mean + other_mean) * 100

        state_cdf_dem[state] = norm.cdf((state_mean_dem[state] - 50) / state_std_dem[state])

        state_mean_rep[state] = rep_mean / (dem_mean + rep_mean + other_mean) * 100

        state_std_rep[state] = np.sqrt(np.average(np.square(rep - rep_mean) +
                                                  (100 - dem) * dem / 10000, weights=obs)) / (dem_mean + rep_mean + other_mean) * 100

        state_cdf_rep[state] = norm.cdf((state_mean_rep[state] - 50) / state_std_rep[state])

print(state_cdf_dem)
print(state_cdf_rep)

# Number of Monte Carlo simulations
n_run = 100000
random_numbers = random.rand(n_run, len(states))

college_total = sum(college.values())  # Total electoral college votes
college_required = college_total / 2  # Electoral college votes required to win
college_dem = np.zeros(n_run)  # Democrats' total electoral college votes
college_rep = np.zeros(n_run)

# Magic
for i, r in enumerate(random_numbers):
    for state_index, state in enumerate(state_cdf_dem):
        if r[state_index] < state_cdf_dem[state]:
            college_dem[i] += college[state]
        elif r[state_index] < state_cdf_rep[state]:
            college_rep[i] += college[state]

print('college_dem=',college_dem)
print('college_rem=',college_rep)

print('college_required=',college_required)

chance_dem = sum(college_dem > college_required) / n_run * 100
print(chance_dem)

chance_rep = sum(college_rep > college_required) / n_run * 100
print(chance_rep)


print('Median of Hillary Clinton\'s electoral votes: {}'.format(int(np.median(college_dem))))
print('Median of Trump\'s electoral votes: {}'.format(int(np.median(college_rep))))
print('Median of Other\'s electoral votes: {}'.format(int(college_total - np.median(college_dem) - np.median(college_rep))))


