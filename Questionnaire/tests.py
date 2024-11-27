from otree.api import Bot

import Questionnaire as pages
from helpers import save_html


class PlayerBot(Bot):
    def play_round(self):
        yield pages.QuestionnaireStart
        save_html(self.html)
        yield pages.TreatmentCheck, dict(relevance_replacement=7, relevance_involvement=7)
        save_html(self.html)
        yield pages.BeliefsQuestion, dict(how_truthful_answer="I tried to give my best possible estimate.", justification='')
        save_html(self.html)
        yield pages.TreatmentQuestion, dict(treatment_active1="Replacing managers in branches",
                                            treatment_active2="Loss of human knowledge")
        save_html(self.html)
        yield pages.TreatmentQuestion, dict(treatment_passive1="To assist in decision-making processes",
                                            treatment_passive2="Assess the AIs helpfulness")
        save_html(self.html)
        yield pages.Demographics, {'sex':'male', 'age':20, 'education':"my_education", 'math_note':4, 'if_all_clear':'Yes'}
        save_html(self.html)
