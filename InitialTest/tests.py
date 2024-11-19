from otree.api import Bot

import InitialTest
from helpers import save_html
from settings import NUMBER_OF_QUESTIONS_INITIAL_TEST, SAMPLES_INITIAL_TEST


class PlayerBot(Bot):
    def play_round(self):
        yield InitialTest.Intro
        save_html(self.html)

        yield InitialTest.ExampleQuestion, dict(example_question="A")
        save_html(self.html)

        yield InitialTest.ExampleExplanation, dict(example_question="A")
        save_html(self.html)

        yield InitialTest.TestStart
        save_html(self.html)

        # Loop through each dynamically generated QuizPage
        for i in range(1, NUMBER_OF_QUESTIONS_INITIAL_TEST + 1):
            answer = "Approve" if SAMPLES_INITIAL_TEST['class'].iloc[i-1] == 1 else "Decline"
            yield InitialTest.Question, {f"Question{i}": answer}
            save_html(self.html)

        yield InitialTest.ConfirmActive
        save_html(self.html)
