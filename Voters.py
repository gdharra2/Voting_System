import operator
class Voters:

    def __init__(self, voter_id:int, preferential_score: float):
        """

        :param voter_id:
        :param preferential_score:
        """
        self.voter_id = voter_id
        self.preferential_score = preferential_score
        self.candidate_preferential_score = {}
        self.vote = ''
        self.ranked_votes = {}
        self.strategic_vote = ''
        self.is_a_strategic_voter = False

    def generate_preferences_for_candidates(self, list_candidates:[]):
        """

        :param preferential_score:
        :param list_candidates:
        :return:
        """
        for each_candidate in list_candidates:
            self.candidate_preferential_score[each_candidate.candidate_number] = \
                1 - abs(each_candidate.fame_score - self.preferential_score)

    def generate_votes(self, list_candidates:[]):
        """

        :param list_candidates:
        :return:
        """
        candidates_to_be_considered = {}
        for each_candidate in list_candidates:
            candidates_to_be_considered[each_candidate.candidate_number] = \
                self.candidate_preferential_score[each_candidate.candidate_number]

        sorted_candidate_preferential_score = dict(sorted(candidates_to_be_considered.items(),
                                                     key=operator.itemgetter(1), reverse=True))
        self.vote = list(sorted_candidate_preferential_score.keys())[0]

    def generate_ranks(self):
        """

        :return:
        """
        sorted_candidate_preferential_score = dict(sorted(self.candidate_preferential_score.items(),
                                                          key=operator.itemgetter(1), reverse=True))
        rank = 1
        for each_candidate in sorted_candidate_preferential_score.keys():
            self.ranked_votes[each_candidate] = rank
            rank += 1

    def strategic_voters(self, is_a_strategic_voter, fame_candidate):
        """

        :return:
        """
        self.is_a_strategic_voter = is_a_strategic_voter
        if is_a_strategic_voter:
            self.strategic_vote = fame_candidate
        else:
            self.strategic_vote = self.vote

    def to_dict(self):
        """

        :return:
        """
        return {'voter_id':self.voter_id,
                'preferential_score':self.preferential_score,
                'candidate_preferential_score':self.candidate_preferential_score,
                'vote':self.vote,
                'ranked_votes': self.ranked_votes,
                'strategic_vote':self.strategic_vote,
                'is_strategic_voter':self.is_a_strategic_voter}
