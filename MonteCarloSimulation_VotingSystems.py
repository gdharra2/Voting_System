import random
import pandas as pd
import operator
import multiprocessing as mp
import Candidate
import Voter

results = []

def create_candidates(number_of_candidates:int)->list:
    """
    Description: This method is used to create candidates using the candidates object.
    It takes the number of candidates as an input and generate a random fame score for the
    candidate
    :param number_of_candidates: Number of candidates to be created
    :return: candidates: List of candidates object

    >>> list_of_candidates = create_candidates(3)
    >>> len(list_of_candidates)
    3
    """
    candidates=[]
    for each_candidate in range(0,number_of_candidates):
        c = Candidate.Candidate(candidate_number=each_candidate, fame_score=random.random())
        candidates.append(c)

    return candidates


def create_voters(number_of_voters: int, number_of_strategic_voters: int, candidates: list)->list:
    """
    Description: This method is used to create voters using the Voters object.
    It takes the number of voters, number of strategic voters and candidates as input.
    It generates a random preferential score for every voter and the candidate with the nearest
    fame score gets the most preference.
    It returns a list of voters object.
    :param number_of_voters: Number of voters to be created
    :param number_of_strategic_voters: Number of strategic voters to be added
    :param candidates: List of candidate objects
    :return:
    >>> list_of_candidates = create_candidates(3)
    >>> list_of_voters = create_voters(10, 4, list_of_candidates)
    >>> len(list_of_voters)
    10
    """
    voters=[]
    list_of_strategic_voters = random.sample(range(0, number_of_voters), number_of_strategic_voters)

    candidate_dict = {k.candidate_number:k.fame_score for k in candidates}
    get_famous_candidate = dict(sorted(candidate_dict.items(), key=operator.itemgetter(1), reverse=True))
    fame_candidate = list(get_famous_candidate.keys())[0]

    for each_voter in range(0,number_of_voters):
        v = Voter.Voter(voter_id=each_voter, preferential_score=random.random())
        v.generate_preferences_for_candidates(list_candidates=candidates)
        v.generate_votes(list_candidates=candidates)
        v.generate_ranks()
        v.strategic_voters(v.voter_id in list_of_strategic_voters, fame_candidate)
        voters.append(v)
    return voters


def determine_winner(voters: list)-> int:
    """
    Description: Determines the winer based on the preferential score
    It takes list of voters as input and adds up score of each voter for every candidate.
    The candidate with the maximum score is determined as the winner and returned.
    :param voters: list of voters as input
    :return: Returns the candidate number of winning candidate

    >>> list_of_candidates = create_candidates(3)
    >>> list_of_voters = create_voters(10, 4, list_of_candidates)
    >>> type(determine_winner(list_of_voters))
    <class 'int'>
    """
    sum_of_scores_for_each_candidate = {}
    for each_voter in voters:
        for each_candidate in each_voter.candidate_preferential_score.keys():
            if each_candidate in sum_of_scores_for_each_candidate.keys():
                sum_of_scores_for_each_candidate[each_candidate] += \
                    each_voter.candidate_preferential_score[each_candidate]
            else:
                sum_of_scores_for_each_candidate[each_candidate] = \
                    each_voter.candidate_preferential_score[each_candidate]

    sorted_scores = dict(sorted(sum_of_scores_for_each_candidate.items(),
                                key=operator.itemgetter(1), reverse=True))

    return list(sorted_scores.keys())[0]


def runoff_election_method(voters: list, number_of_voters: int, number_of_strategic_voters: int,
                           candidates: list, winner: int, is_strategy: bool) -> bool:
    """
    Description: This method is used to determine the winner based on the run off method
    :param voters: List of voters
    :param number_of_voters: Number of voters
    :param number_of_strategic_voters: Number of strategic voters
    :param candidates: List of candidates
    :param winner: Expected Winner
    :param is_strategy: Boolean value indicating if strategy is to be used or not
    :return: Returns a boolean if the winner from this type was the same as expected winner
    >>> list_of_candidates = create_candidates(3)
    >>> list_of_voters = create_voters(10, 4, list_of_candidates)
    >>> type(determine_winner(list_of_voters))
    <class 'int'>
    """
    sum_of_scores_for_each_candidate = {}

    for each_voter in voters:
        vote_given = each_voter.vote

        if not is_strategy:
            if vote_given in sum_of_scores_for_each_candidate.keys():
                sum_of_scores_for_each_candidate[vote_given] += each_voter.vote
            else:
                sum_of_scores_for_each_candidate[vote_given] = each_voter.vote
        else:
            if vote_given in sum_of_scores_for_each_candidate:
                sum_of_scores_for_each_candidate[vote_given] += each_voter.strategic_vote
            else:
                sum_of_scores_for_each_candidate[vote_given] = each_voter.strategic_vote

    sorted_scores = dict(sorted(sum_of_scores_for_each_candidate.items(),
                                key=operator.itemgetter(1), reverse=True))

    last_element = list(sorted_scores.keys())[-1]
    sorted_scores.pop(last_element)

    updated_candidate_list = []

    for each_candidate in candidates:
        if each_candidate.candidate_number in sorted_scores.keys():
            updated_candidate_list.append(each_candidate)

    if len(sorted_scores)==1:
        return list(sorted_scores.keys())[0] == winner
    else:
        new_list_of_voters = create_voters(number_of_voters, number_of_strategic_voters, updated_candidate_list)
        return runoff_election_method(new_list_of_voters, number_of_voters,
                                      number_of_strategic_voters, updated_candidate_list,
                                      winner, is_strategy)


def determine_election_results_for_different_methods(voters: list, winner: int, result_map: dict,
                                                     n_strategy: int, candidates: list) -> dict:
    """
    Description: This method is used to determine the election result for different types of elections.
    :param voters: List of voters
    :param winner: Expected Winner
    :param result_map: A dictionary of result for different types of voting system
    :param n_strategy: Number of strategic voters
    :param candidates: List of candidates
    :return: Returns the result_map dictionary
    >>> list_of_candidates = create_candidates(3)
    >>> list_of_voters = create_voters(10, 4, list_of_candidates)
    >>> type(determine_winner(list_of_voters))
    <class 'int'>
    """
    sum_of_scores_for_each_candidate = {}
    sum_of_scores_for_each_candidate_with_strategy = {}
    sum_of_ranks_for_each_candidate = {}
    sum_of_ranks_for_each_candidate_strategy = {}
    condocert_votes_for_each_candidate = {}
    condocert_votes_for_each_candidate_strategy = {}
    score_votes_for_each_candidate = {}
    score_votes_for_each_candidate_strategy = {}

    result_map['Run_off'].append(runoff_election_method(voters, len(voters), n_strategy, candidates, winner, False))
    result_map['Run_off_Strategy'].append(runoff_election_method(voters, len(voters), n_strategy, candidates, winner, True))

    for each_voter in voters:
        vote_given = each_voter.vote
        ranks = each_voter.ranked_votes
        candidate_pref_score_dict = each_voter.candidate_preferential_score

        # Plurality
        if vote_given in sum_of_scores_for_each_candidate.keys():
            sum_of_scores_for_each_candidate[vote_given] += each_voter.vote
        else:
            sum_of_scores_for_each_candidate[vote_given] = each_voter.vote

        # Plurality with strategy
        if vote_given in sum_of_scores_for_each_candidate_with_strategy:
            sum_of_scores_for_each_candidate_with_strategy[vote_given] += each_voter.strategic_vote
        else:
            sum_of_scores_for_each_candidate_with_strategy[vote_given] = each_voter.strategic_vote

        # Borda
        for each_candidate in ranks.keys():
            if each_candidate in sum_of_ranks_for_each_candidate:
                sum_of_ranks_for_each_candidate[each_candidate] += ranks[each_candidate]
            else:
                sum_of_ranks_for_each_candidate[each_candidate] = ranks[each_candidate]

        # Condocert
        sorted_candidate_pref_Score_dict = dict(sorted(candidate_pref_score_dict.items(),
                                                  key = operator.itemgetter(1),
                                                  reverse = True))

        winner_based_on_pref_score = list(sorted_candidate_pref_Score_dict.keys())[0]

        if winner_based_on_pref_score in condocert_votes_for_each_candidate.keys():
            condocert_votes_for_each_candidate[winner_based_on_pref_score] +=1
        else:
            condocert_votes_for_each_candidate[winner_based_on_pref_score] = 1

        # Condocert with strategy

        winner_based_on_strategy_pref_Score = each_voter.strategic_vote\

        if winner_based_on_strategy_pref_Score in condocert_votes_for_each_candidate_strategy.keys():
            condocert_votes_for_each_candidate_strategy[winner_based_on_strategy_pref_Score] +=1
        else:
            condocert_votes_for_each_candidate_strategy[winner_based_on_strategy_pref_Score] = 1

        # Borda with strategy

        if ranks[winner_based_on_strategy_pref_Score] != 1:
            temp = ranks[winner_based_on_pref_score]
            ranks[winner_based_on_pref_score] = ranks[winner_based_on_strategy_pref_Score]
            ranks[winner_based_on_strategy_pref_Score] = 1

        for each_candidate in ranks.keys():

            if each_candidate in sum_of_ranks_for_each_candidate_strategy:
                sum_of_ranks_for_each_candidate_strategy[each_candidate] += ranks[each_candidate]
            else:
                sum_of_ranks_for_each_candidate_strategy[each_candidate] = ranks[each_candidate]

        # Score Voting with and without strategy

        for each_candidate in candidate_pref_score_dict.keys():
            if each_candidate in score_votes_for_each_candidate.keys():
                score_votes_for_each_candidate[each_candidate] += candidate_pref_score_dict[each_candidate] * 10
            else:
                score_votes_for_each_candidate[each_candidate] = candidate_pref_score_dict[each_candidate] * 10

        # Score Voting with strategy

        if each_voter.is_a_strategic_voter:
            temp = candidate_pref_score_dict[winner_based_on_pref_score]
            candidate_pref_score_dict[winner_based_on_pref_score] = candidate_pref_score_dict[each_voter.strategic_vote]
            candidate_pref_score_dict[each_voter.strategic_vote] = temp

        for each_candidate in candidate_pref_score_dict.keys():
            if each_candidate in score_votes_for_each_candidate_strategy:
                score_votes_for_each_candidate_strategy[each_candidate] += candidate_pref_score_dict[each_candidate] * 10
            else:
                score_votes_for_each_candidate_strategy[each_candidate] = candidate_pref_score_dict[each_candidate] * 10

    # Plurality:
    sorted_scores = dict(sorted(sum_of_scores_for_each_candidate.items(),
                                key=operator.itemgetter(1), reverse=True))
    result_map['Plurality'].append(list(sorted_scores.keys())[0] == winner)

    # Plurality with strategy
    sorted_scores_strategy = dict(sorted(sum_of_scores_for_each_candidate_with_strategy.items(),
                                key=operator.itemgetter(1), reverse=True))
    result_map['Plurality_Strategy'].append(list(sorted_scores_strategy.keys())[0] == winner)

    # Borda
    sorted_ranks = dict(sorted(sum_of_ranks_for_each_candidate.items(),
                                key=operator.itemgetter(1)))
    result_map['Borda'].append(list(sorted_ranks.keys())[0] == winner)

    # Borda with strategy
    sorted_ranks_strategy = dict(sorted(sum_of_ranks_for_each_candidate_strategy.items(),
                               key=operator.itemgetter(1)))
    result_map['Borda_Strategy'].append(list(sorted_ranks_strategy.keys())[0] == winner)

    # Condocert
    sorted_condocert_score = dict(sorted(condocert_votes_for_each_candidate.items(),
                                         key=operator.itemgetter(1),
                                         reverse=True))
    result_map['Condocert'].append(list(sorted_condocert_score.keys())[0]==winner)

    # Condocert with strategy
    sorted_condocert_strategy_score = dict(sorted(condocert_votes_for_each_candidate_strategy.items(),
                                         key=operator.itemgetter(1),
                                         reverse=True))
    result_map['Condocert_Strategy'].append(list(sorted_condocert_strategy_score.keys())[0] == winner)

    # Score Voting
    sorted_score_voting = dict(sorted(score_votes_for_each_candidate.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True))
    result_map['Score_Voting'].append(list(sorted_score_voting.keys())[0] == winner)

    # Score Voting with strategy
    sorted_score_voting_strategy = dict(sorted(score_votes_for_each_candidate_strategy.items(),
                                      key=operator.itemgetter(1),
                                      reverse=True))
    result_map['Score_Voting_Strategy'].append(list(sorted_score_voting_strategy.keys())[0] == winner)

    return result_map


def run_simulation(result_map):
    """

    :param result_map:
    :return:
    """
    # Number of Monte Carlo Simulations
    n_voters = 10000
    n_strategy = 2500
    n_candidates = 4

    # Generate Candidates with fame score
    candidates = create_candidates(n_candidates)

    # Generate Voters with preferential score for each candidate
    voters = create_voters(n_voters, n_strategy, candidates)

    # Predict winner based on the preferential score
    winner = determine_winner(voters)

    # Run election results
    return determine_election_results_for_different_methods(voters, winner, result_map, n_strategy, candidates)


def collect_result(result):
    """
    Description: Appends the result map returned from each simulaiton
    to the global result list variable.
    :param result: result_map returned from a simulation
    :return:
    """
    global results
    results.append(result)


def main():
    global results
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_columns', None)

    pool = mp.Pool(mp.cpu_count())

    result_map = [{'Plurality': [], 'Plurality_Strategy': [],
                   'Run_off': [], 'Run_off_Strategy': [],
                   'Borda': [], 'Borda_Strategy': [],
                   'Condocert': [], 'Condocert_Strategy': [],
                   'Score_Voting': [], 'Score_Voting_Strategy': []}]

    n_simulations = 100

    # run_simulation(result_map)
    for i in range(0,n_simulations):
        pool.apply_async(run_simulation, args=(result_map), callback=collect_result)

    pool.close()
    pool.join()
    print(results)

    total_pluraity = 0
    total_run_off = 0
    total_borda = 0
    total_condocert = 0
    total_score_voting = 0

    total_pluraity_strategy = 0
    total_condocert_strategy = 0
    total_score_voting_strategy = 0
    total_borda_strategy = 0
    total_run_off_strategy = 0

    for each_result in results:
        if each_result['Plurality'][0]:
            total_pluraity += 1

        if each_result['Run_off'][0]:
            total_run_off += 1

        if each_result['Borda'][0]:
            total_borda += 1

        if each_result['Condocert'][0]:
            total_condocert += 1

        if each_result['Score_Voting'][0]:
            total_score_voting += 1

        if each_result['Plurality_Strategy'][0]:
            total_pluraity_strategy += 1

        if each_result['Run_off_Strategy'][0]:
            total_run_off_strategy += 1

        if each_result['Borda_Strategy'][0]:
            total_borda_strategy += 1

        if each_result['Condocert_Strategy'][0]:
            total_condocert_strategy += 1

        if each_result['Score_Voting_Strategy'][0]:
            total_score_voting_strategy += 1

    print('Probability of Plurality = ', total_pluraity / n_simulations)
    print('Probability of Run off = ', total_run_off / n_simulations)
    print('Probability of Borda = ', total_borda / n_simulations)
    print('Probability of Condocert = ', total_condocert / n_simulations)
    print('Probability of Score Voting = ', total_score_voting / n_simulations)

    print('Probability of Plurality Strategy = ', total_pluraity_strategy / n_simulations)
    print('Probability of Run-off Strategy = ', total_run_off_strategy / n_simulations)
    print('Probability of Borda Strategy = ', total_borda_strategy / n_simulations)
    print('Probability of Condocert Strategy = ', total_condocert_strategy / n_simulations)
    print('Probability of Score Voting Strategy = ', total_score_voting_strategy / n_simulations)


if __name__ == '__main__':
    main()
