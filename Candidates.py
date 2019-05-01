class Candidates:

    def __init__(self, fame_score:float, candidate_number: int):
        """
        Initializes a Candidate object with a desired candidate number and fame score
        :param fame_score: A randomly generated value between 0 and 1
        :param candidate_number: A sequentially generated number unique for a candidate
        """
        self.fame_score = fame_score
        self.candidate_number = candidate_number


