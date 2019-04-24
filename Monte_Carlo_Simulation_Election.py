import random
import numpy as np
import pandas as pd
import operator


def create_candidates(list_of_candidates):
    # code to create candidates
    """

    :param list_of_candidates:
    :return:
    """
    data = {}
    for each_candidate in list_of_candidates:
        data[each_candidate] = random.random()

    return data


def create_voters(number_of_voters, candidates):
    # code to create voters
    """

    :param number_of_voters:
    :param candidates:
    :return:
    """
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
    """

    :param n_trials:
    :param voters:
    :return:
    """
    total_score_a = voters.preferential_score_candidate_A.sum()/n_trials
    total_score_b = voters.preferential_score_candidate_B.sum()/n_trials
    total_score_c = voters.preferential_score_candidate_C.sum()/n_trials
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


def generate_votes_based_on_candidates(voters, candidates_list):
    """

    :param voters:
    :param candidates_list:
    :return:
    """
    voter_votes = []

    for index, row in voters.iterrows():

        list_of_preferential_scores = []

        if 'A' in candidates_list:
            list_of_preferential_scores.append(row.preferential_score_candidate_A)

        if 'B' in candidates_list:
            list_of_preferential_scores.append(row.preferential_score_candidate_B)

        if 'C' in candidates_list:
            list_of_preferential_scores.append(row.preferential_score_candidate_C)

        max_value = max(list_of_preferential_scores)
        voted_candidate = 'A' if 'A' in candidates_list \
                          and max_value == row.preferential_score_candidate_A \
                          else 'B' if 'B' in candidates_list and \
                          max_value == row.preferential_score_candidate_B \
                          else 'C'
        voter_votes.append(voted_candidate)

    voters['Vote'] = voter_votes

    return voters


def generate_votes_by_assigning_ranks(voters, candidates_list):
    """

    :param voters:
    :param candidates_list:
    :return:
    """
    voters_rank_a = []
    voters_rank_b = []
    voters_rank_c = []
    for index, row in voters.iterrows():

        dict_of_preferential_scores = {}

        if 'A' in candidates_list:
            dict_of_preferential_scores['A'] = row.preferential_score_candidate_A

        if 'B' in candidates_list:
            dict_of_preferential_scores['B'] = row.preferential_score_candidate_B

        if 'C' in candidates_list:
            dict_of_preferential_scores['C'] = row.preferential_score_candidate_C

        sorted_dict_preferential_scores = dict(sorted(dict_of_preferential_scores.items(),
                                                key=operator.itemgetter(1)))

        i = 1

        for each_score in sorted_dict_preferential_scores.keys():
            sorted_dict_preferential_scores[each_score] = 1 + len(candidates_list) - i
            i += 1

        if 'A' in sorted_dict_preferential_scores.keys():
            voters_rank_a.append(sorted_dict_preferential_scores['A'])
        else:
            voters_rank_a.append(np.nan)

        if 'B' in sorted_dict_preferential_scores.keys():
            voters_rank_b.append(sorted_dict_preferential_scores['B'])
        else:
            voters_rank_b.append(np.nan)

        if 'C' in sorted_dict_preferential_scores.keys():
            voters_rank_c.append(sorted_dict_preferential_scores['C'])
        else:
            voters_rank_c.append(np.nan)

    voters['rank_a'] = voters_rank_a
    voters['rank_b'] = voters_rank_b
    voters['rank_c'] = voters_rank_c

    return voters


def introduce_strategic_manipulation_on_votes(num_strategic_voters, voters, candidate, total_voters):
    """

    :param num_strategic_voters:
    :param voters:
    :param candidate:
    :param total_voters:
    :return:
    """
    get_famous_candidate = dict(sorted(candidate.items(), key=operator.itemgetter(1), reverse=True))
    print(list(get_famous_candidate.keys())[0])
    fame_candidate = list(get_famous_candidate.keys())[0]

    for i in random.sample(range(0, total_voters), num_strategic_voters):
        if voters.iat[i,4] != get_famous_candidate:
            new_value = pd.DataFrame({'Vote': [fame_candidate]}, index=[i])
            voters.update(new_value)

    return voters


def plurality_election_method(voters):
    """

    :param voters:
    :return:
    """
    return voters.groupby('Vote')['Vote'].count().idxmax()


def runoff_election_method(voters, number_of_candidates):
    """

    :param voters:
    :param number_of_candidates:
    :return:
    """
    voters_by_count = voters.groupby('Vote')['Vote'].count() \
                      .reset_index(name='count').sort_values('count', ascending=False)\
                      .head(number_of_candidates-1)
    if len(voters_by_count)==1:
        return voters.groupby('Vote')['Vote'].count().idxmax()
    else:
        new_list_of_voters = generate_votes_based_on_candidates(voters, list(voters_by_count['Vote']))
        return runoff_election_method(new_list_of_voters, len(list(voters_by_count['Vote'])))


def borda_election_method(voters):
    """

    :param voters:
    :return:
    """
    rank_a = voters['rank_a'].sum()
    rank_b = voters['rank_b'].sum()
    rank_c = voters['rank_c'].sum()

    net_score = {'A':rank_a, 'B':rank_b, 'C':rank_c}
    sorted_net_score = dict(sorted(net_score.items(),
                              key = operator.itemgetter(1), reverse=True))

    return list(sorted_net_score.keys())[0]


def condocert_election_method(voters, candidate, introduce_strategy, total_voters, num_strategic_voters):
    """

    :param voters:
    :return:
    """
    total_votes_a = 0
    total_votes_b = 0
    total_votes_c = 0

    if introduce_strategy:
        get_famous_candidate = dict(sorted(candidate.items(), key=operator.itemgetter(1), reverse=True))
        fame_candidate = list(get_famous_candidate.keys())[0]
        strategic_voter_ids = random.sample(range(0, total_voters), num_strategic_voters)

        for index, row in voters.iterrows():
            if index in strategic_voter_ids:
                dict_preferential_values = {'A': row.preferential_score_candidate_A,
                                            'B': row.preferential_score_candidate_B,
                                            'C': row.preferential_score_candidate_C}
                sorted_dict_preferential_values = dict(sorted(dict_preferential_values.items(),
                                                              key=operator.itemgetter(1),
                                                              reverse=True))
                preferred_candidate = list(sorted_dict_preferential_values.keys())[0]
                if preferred_candidate != fame_candidate:
                    temp = dict_preferential_values[preferred_candidate]
                    dict_preferential_values[preferred_candidate] = dict_preferential_values[fame_candidate]
                    dict_preferential_values[fame_candidate] = temp

                if dict_preferential_values['A'] > dict_preferential_values['B']:
                    if dict_preferential_values['A'] > dict_preferential_values['C']:
                        total_votes_a += 1
                    else:
                        total_votes_c += 1
                else:
                    if dict_preferential_values['B'] > dict_preferential_values['C']:
                        total_votes_b += 1
                    else:
                        total_votes_c += 1
            else:
                if row.preferential_score_candidate_A > row.preferential_score_candidate_B:
                    if row.preferential_score_candidate_A > row.preferential_score_candidate_C:
                        total_votes_a += 1
                    else:
                        total_votes_c += 1
                else:
                    if row.preferential_score_candidate_B > row.preferential_score_candidate_C:
                        total_votes_b += 1
                    else:
                        total_votes_c += 1
    else:
        for index, row in voters.iterrows():
            if row.preferential_score_candidate_A > row.preferential_score_candidate_B:
                if row.preferential_score_candidate_A > row.preferential_score_candidate_C:
                    total_votes_a += 1
                else:
                    total_votes_c += 1
            else:
                if row.preferential_score_candidate_B > row.preferential_score_candidate_C:
                    total_votes_b += 1
                else:
                    total_votes_c += 1

    dict_score_values = {'A':total_votes_a, 'B':total_votes_b, 'C':total_votes_c}
    sorted_dict_score_values = dict(sorted(dict_score_values.items(),
                                           key = operator.itemgetter(1), reverse=True))

    return list(sorted_dict_score_values.keys())[0]


def score_voting_election_method(voters, candidate, introduce_strategy, total_voters, num_strategic_voters):
    """

    :param voters:
    :param candidate:
    :param introduce_strategy:
    :param total_voters:
    :param num_strategic_voters:
    :return:
    """

    score_votes_a = []
    score_votes_b = []
    score_votes_c = []

    if introduce_strategy:
        get_famous_candidate = dict(sorted(candidate.items(), key=operator.itemgetter(1), reverse=True))
        fame_candidate = list(get_famous_candidate.keys())[0]
        strategic_voter_ids = random.sample(range(0, total_voters), num_strategic_voters)

        for index, row in voters.iterrows():

            if index in strategic_voter_ids:
                dict_preferential_values = {'A': row.preferential_score_candidate_A * 10,
                                            'B': row.preferential_score_candidate_B * 10,
                                            'C': row.preferential_score_candidate_C * 10}
                sorted_dict_preferential_values = dict(sorted(dict_preferential_values.items(),
                                                              key=operator.itemgetter(1),
                                                              reverse=True))
                preferred_candidate = list(sorted_dict_preferential_values.keys())[0]
                if preferred_candidate != fame_candidate:
                    temp = dict_preferential_values[preferred_candidate]
                    dict_preferential_values[preferred_candidate] = dict_preferential_values[fame_candidate]
                    dict_preferential_values[fame_candidate] = temp
                score_votes_a.append(dict_preferential_values['A'] * 10)
                score_votes_b.append(dict_preferential_values['B'] * 10)
                score_votes_c.append(dict_preferential_values['C'] * 10)
            else:
                score_votes_a.append(row.preferential_score_candidate_A * 10)
                score_votes_b.append(row.preferential_score_candidate_B * 10)
                score_votes_c.append(row.preferential_score_candidate_C * 10)

    else:
        # rating all voters on a scale of 10
        for index, row in voters.iterrows():
            score_votes_a.append(row.preferential_score_candidate_A * 10)
            score_votes_b.append(row.preferential_score_candidate_B * 10)
            score_votes_c.append(row.preferential_score_candidate_C * 10)

    voters['score_value_a'] = score_votes_a
    voters['score_value_b'] = score_votes_b
    voters['score_value_c'] = score_votes_c

    score_a = voters['score_value_a'].sum()
    score_b = voters['score_value_b'].sum()
    score_c = voters['score_value_c'].sum()

    dict_score_values = {'A': score_a, 'B': score_b, 'C': score_c}
    sorted_dict_score_values = dict(sorted(dict_score_values.items(),
                                           key=operator.itemgetter(1), reverse=True))

    return list(sorted_dict_score_values.keys())[0]


def main():
    # call all functions

    # Number of Monte Carlo Simulations
    n_run = 100000

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

    # Get voters based
    voters_with_votes = generate_votes_based_on_candidates(voters, ['A', 'B', 'C'])
    print('candidate based voters list')
    print(voters_with_votes)

    # Get votes based on ranking
    voters_with_ranking = generate_votes_by_assigning_ranks(voters, ['A','B','C'])
    print('ranked candidate based voters list')
    print(voters_with_ranking)

    # Applying Strategic Manipulaiton
    voters_strategy = introduce_strategic_manipulation_on_votes(1000, voters, candidates, n_run)
    print('Strategic Manipulation')
    print(voters_strategy)

    # Get winner using Plurality
    winner_plurality = plurality_election_method(voters_with_votes)
    print('Plurality Result = ', winner_plurality)

    # Get winner using Plurality with strategy
    winner_plurality_strategy = plurality_election_method(voters_strategy)
    print('Strategy Plurality Result = ', winner_plurality_strategy)

    # Get winner using runoff
    winner_runoff = runoff_election_method(voters_with_votes, len(candidates))
    print('Run off Result =', winner_runoff)

    # Get winner using runoff with strategy
    winner_runoff_strategy = runoff_election_method(voters_strategy, len(candidates))
    print('Run off Result with Strategy =', winner_runoff_strategy)

    # Get winner using borda
    winner_borda = borda_election_method(voters_with_ranking)
    print('Borda Result =',winner_borda)

    # Get winner using Condocert
    winner_condocert = condocert_election_method(voters, candidates, False, n_run, 1000)
    print('Condocert Result =', winner_condocert)

    # Get winner using Condocert with strategy
    winner_condocert = condocert_election_method(voters, candidates, True, n_run, 1000)
    print('Condocert Result with strategy=', winner_condocert)

    # Get winner using score voting
    winner_score_voting = score_voting_election_method(voters, candidates, False, n_run, 1000)
    print('Score Voting Result =', winner_score_voting)

    # Get winner using score voting with strategy
    winner_score_voting_strategy = score_voting_election_method(voters, candidates, True, n_run, 1000)
    print('Score Voting Result with Strategy =', winner_score_voting_strategy)


if __name__ == '__main__':
    main()
