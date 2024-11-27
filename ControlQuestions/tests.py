import ControlQuestions as pages
from otree.api import Bot

from helpers import save_html

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield pages.ControlQuestions, dict(
                cntr_quest_1="True",
                cntr_quest_2="True",
                cntr_quest_3="True",
            )
            save_html(self.html)
            yield pages.Result
            save_html(self.html)
