import random
import numpy as np
import pandas as pd
import operator


def create_candidates(list_of_candidates):
    # code to create candidates
    data = {}
    for each_candidate in list_of_candidates:
        data[each_candidate] = random.random()

    return data


def create_voters(number_of_voters, candidates):
    # code to create voters
    print(number_of_voters)
    voters={'voter_id':[],'preferential_score_candidate_A':[],
            'preferential_score_candidate_B':[],
            'preferential_score_candidate_C': [],
            'Vote':''}

    fame_score_candidate_a = candidates['A']
    fame_score_candidate_b = candidates['B']
    fame_score_candidate_c = candidates['C']

    for trial in range(0, number_of_voters):
        voters['voter_id'].append(trial)
        random_int = random.random()

        voters['preferential_score_candidate_A'].append(1-abs(fame_score_candidate_a-random_int))
        voters['preferential_score_candidate_B'].append(1-abs(fame_score_candidate_b-random_int))
        voters['preferential_score_candidate_C'].append(1-abs(fame_score_candidate_c-random_int))

    voters_pd = pd.DataFrame(voters)

    return voters_pd


def determine_winner(n_trials, voters):
    # code to determine winner
    total_score_a = voters.preferential_score_candidate_A.sum()/n_trials
    total_score_b = voters.preferential_score_candidate_B.sum()/n_trials
    total_score_c = voters.preferential_score_candidate_C.sum()/n_trials
    print('total_score_A', total_score_a)
    print('total_score_B', total_score_b)
    print('total_score_C', total_score_c)

    if total_score_a > total_score_b:
        if total_score_a > total_score_c:
            return 'A'
        else:
            return 'C'
    else:
        if total_score_b > total_score_c:
            return 'B'
        else:
            return 'C'


def generate_votes(voters):
    voter_votes = []

    for index, row in voters.iterrows():
        print('Preferential Score Votes')
        print('A', row.preferential_score_candidate_A)
        print('B', row.preferential_score_candidate_B)
        print('C', row.preferential_score_candidate_C)

        max_value = max(row.preferential_score_candidate_A, row.preferential_score_candidate_B, row.preferential_score_candidate_C)
        print('max_value=',max_value)
        voted_candidate = 'A' if max_value == row.preferential_score_candidate_A else 'B' if max_value == row.preferential_score_candidate_B else 'C'
        print('voted_candidate=', voted_candidate)
        voter_votes.append(voted_candidate)

    voters['Vote'] = voter_votes

    return voters


def generate_votes_based_on_candidates(voters, candidates_list):
    voter_votes = []

    for index, row in voters.iterrows():
        print('Preferential Score Votes')
        print('A', row.preferential_score_candidate_A)
        print('B', row.preferential_score_candidate_B)
        print('C', row.preferential_score_candidate_C)

        list_of_preferential_scores = []

        if 'A' in candidates_list:
            list_of_preferential_scores.append(row.preferential_score_candidate_A)

        if 'B' in candidates_list:
            list_of_preferential_scores.append(row.preferential_score_candidate_B)

        if 'C' in candidates_list:
            list_of_preferential_scores.append(row.preferential_score_candidate_C)

        max_value = max(list_of_preferential_scores)
        print('max_value=',max_value)
        voted_candidate = 'A' if max_value == row.preferential_score_candidate_A else 'B' if max_value == row.preferential_score_candidate_B else 'C'
        print('voted_candidate=', voted_candidate)
        voter_votes.append(voted_candidate)

    voters['Vote'] = voter_votes

    return voters


def introduce_strategic_manipulation(num_strategic_voters, voters, candidate, total_voters):
    get_famous_candidate = dict(sorted(candidate.items(), key=operator.itemgetter(1), reverse=True))
    print(list(get_famous_candidate.keys())[0])
    fame_candidate = list(get_famous_candidate.keys())[0]

    for i in random.sample(range(0, total_voters), num_strategic_voters):
        if voters.iat[i,4] != get_famous_candidate:
            new_value = pd.DataFrame({'Vote': [fame_candidate]}, index=[i])
            voters.update(new_value)

    return voters


def plurality_election_method(voters):
    return voters.groupby('Vote')['Vote'].count().idxmax()


def runoff_election_method(voters, number_of_candidates):
    voters_by_count = voters.groupby('Vote')['Vote'].count() \
                      .reset_index(name='count').sort_values('count', ascending=False)\
                      .head(number_of_candidates-1)
    print(voters_by_count)
    if len(voters_by_count)==1:
        return voters.groupby('Vote')['Vote'].count().idxmax()
    else:
        return 'B'


def main():
    # call all functions

    # Number of Monte Carlo Simulations
    n_run = 5

    # Generate Candidates with fame score
    candidates = create_candidates(['A', 'B', 'C'])
    print('Candidates with fame score')
    print(candidates)

    # Generate Voters with preferential score for each candidate
    voters = create_voters(n_run, candidates)
    print('Voters with preferential score')
    print(voters)

    # Predict winner based on the preferential score
    winner = determine_winner(n_run,voters)
    print('Expected Winner = ',winner)

    # Generate votes
    voters = generate_votes(voters)
    print('Votes Generated')
    print(voters)

    # Applying Strategic Manipulaiton
    voters_strategy = introduce_strategic_manipulation(2, voters, candidates, n_run)
    print('Strategic Manipulation')
    print(voters_strategy)

    # Get winner using Plurality
    winner_plurality = plurality_election_method(voters)
    print('Plurality Result = ', winner_plurality)

    # Get winner using Plurality with strategy
    winner_plurality_strategy = plurality_election_method(voters_strategy)
    print('Strategy Plurality Result = ', winner_plurality_strategy)

    # Get winner using runoff
    winner_runoff = runoff_election_method(voters, len(candidates))
    print('Run off Result =', winner_runoff)

    voters_3 = generate_votes_based_on_candidates(voters, ['A','B','C'])
    print('candidate based voters list')
    print(voters_3)



if __name__ == '__main__':
    main()
