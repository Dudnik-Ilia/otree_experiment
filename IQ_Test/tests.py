from otree.api import Bot

import IQ_Test
from helpers import save_html
from settings import NUMBER_OF_QUIZES


class PlayerBot(Bot):
    def play_round(self):
        yield IQ_Test.Intro
        save_html(self.html)

        yield IQ_Test.ExampleQuestion, dict(example_question="A")
        save_html(self.html)

        yield IQ_Test.ExampleExplanation, dict(example_question="A")
        save_html(self.html)

        yield IQ_Test.QuizStart
        save_html(self.html)

        # Loop through each dynamically generated QuizPage
        for i in range(1, NUMBER_OF_QUIZES + 1):
            answer = "True" if i in [5, 9, 12] else "A"
            yield IQ_Test.QuizPage, {f"Quiz{i}": answer}
            save_html(self.html)

        yield IQ_Test.ConfirmActive
        save_html(self.html)
