import MainTest as pages
from otree.api import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Explanation
        yield pages.Einschaetzung1, dict(Einschaetzung1=100)
        yield pages.ResultBelief
        yield pages.TreatmentIntro
        yield pages.TreatmentPassive
        yield pages.Questions, dict(ArticleQuestion1="Pro")
        yield pages.Result
        yield pages.Relevance, dict(relevance1=7, relevance2=7)
        yield pages.FeedbackExplanation
        yield pages.Signal1
        yield pages.Einschaetzung2, dict(Einschaetzung2=100)
        yield pages.Signal2
        yield pages.Einschaetzung3, dict(Einschaetzung3=100)
        yield pages.Payoff