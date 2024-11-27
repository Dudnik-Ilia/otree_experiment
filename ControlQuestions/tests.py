import ControlQuestions as pages
from otree.api import Bot

from helpers import save_html

class PlayerBot(Bot):
    cases = [1,2]
    def play_round(self):
        
        # Base case
        if self.case == 1:
            yield pages.ControlQuestions, dict(
                cntr_quest_1="True",
                cntr_quest_2="True",
                cntr_quest_3="True",
            )
            save_html(self.html)
            yield pages.Result
            save_html(self.html)

        # Check that we do another try if we fail to correctly answer all questions
        if self.case == 2:
            yield pages.ControlQuestions, dict(
                cntr_quest_1="True",
                cntr_quest_2="40%",
                cntr_quest_3="True",
            )
            yield pages.Result
            assert self.participant._current_page_name == 'ControlQuestions', f"{self.participant._current_page_name}"
