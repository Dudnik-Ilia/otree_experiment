import ControlQuestions
from otree.api import Bot


class PlayerBot(Bot):
    cases = [1,2]
    def play_round(self):
        if self.case == 1:
            yield ControlQuestions.ControlQuestions, dict(
                interactive=1,
                cntr_quest_1="True",
                cntr_quest_2="True",
                cntr_quest_3="True",
            )
            yield ControlQuestions.Result
            assert self.participant._current_page_name == 'Dropout'
            return

        if self.case == 2:
            yield ControlQuestions.ControlQuestions, dict(
                interactive=1,
                cntr_quest_1="True",
                cntr_quest_2="40%",
                cntr_quest_3="True",
            )
            yield ControlQuestions.Result
            assert self.participant._current_page_name == 'ControlQuestions', f"{self.participant._current_page_name}"
            return None