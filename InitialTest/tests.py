from otree.api import Bot

import InitialTest
from helpers import save_html
from settings import NUMBER_OF_QUIZES


class PlayerBot(Bot):
    def play_round(self):
        yield InitialTest.Intro
        save_html(self.html)

        yield InitialTest.ExampleQuestion, dict(example_question="A")
        save_html(self.html)

        yield InitialTest.ExampleExplanation, dict(example_question="A")
        save_html(self.html)

        yield InitialTest.QuizStart
        save_html(self.html)

        # Loop through each dynamically generated QuizPage
        for i in range(1, NUMBER_OF_QUIZES + 1):
            answer = "True" if i in [5, 9, 12] else "A"
            yield InitialTest.QuizPage, {f"Quiz{i}": answer}
            save_html(self.html)

        yield InitialTest.ConfirmActive
        save_html(self.html)
