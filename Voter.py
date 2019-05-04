# Rename it to Voter
import operator
class Voter:

    def __init__(self, voter_id:int, preferential_score: float):
        """
        Initialize the Voters object
        :param voter_id: A unique Id
        :param preferential_score: A randomly generated score
        """
        self.voter_id = voter_id
        self.preferential_score = preferential_score
        self.candidate_preferential_score = {}
        self.vote = ''
        self.ranked_votes = {}
        self.strategic_vote = ''
        self.is_a_strategic_voter = False

    def generate_preferences_for_candidates(self, list_candidates:list):
        """
        Computes distance of each candidate from the voter based on the preferential and fame score.
        :param list_candidates: List of all candidate objects
        :return:
        """
        for each_candidate in list_candidates:
            self.candidate_preferential_score[each_candidate.candidate_number] = \
                1 - abs(each_candidate.fame_score - self.preferential_score)

    def generate_votes(self, list_candidates:list):
        """
        Creates votes based on the preferential score
        :param list_candidates: List of candidates
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
        Generate Ranks (1,2,3...) based on the preferential score
        :return:
        """
        sorted_candidate_preferential_score = dict(sorted(self.candidate_preferential_score.items(),
                                                          key=operator.itemgetter(1), reverse=True))
        rank = 1
        for each_candidate in sorted_candidate_preferential_score.keys():
            self.ranked_votes[each_candidate] = rank
            rank += 1

    def strategic_voters(self, is_a_strategic_voter: bool, fame_candidate: int):
        """
        Manipulates votes for strategic voters to favor the famous candidate instead of the preferred candidate.
        :param is_a_strategic_voter: Boolean indicating if the voter is strategic or not
        :param fame_candidate: Integer indicating the candidate number that has the highest fame score
        :return:
        """
        self.is_a_strategic_voter = is_a_strategic_voter
        if is_a_strategic_voter:
            self.strategic_vote = fame_candidate
        else:
            self.strategic_vote = self.vote

    def to_dict(self)->dict:
        """
        Converts voters object to a dictionary
        :return:
        """
        return {'voter_id':self.voter_id,
                'preferential_score':self.preferential_score,
                'candidate_preferential_score':self.candidate_preferential_score,
                'vote':self.vote,
                'ranked_votes': self.ranked_votes,
                'strategic_vote':self.strategic_vote,
                'is_strategic_voter':self.is_a_strategic_voter}
