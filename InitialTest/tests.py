from otree.api import Bot

import InitialTest as pages
from helpers import save_html
from settings import NUM_OF_QUESTIONS_INITIAL_TEST, SAMPLES_INITIAL_TEST


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Intro
        save_html(self.html)

        yield pages.ExampleQuestion, dict(example_question="Approve")
        save_html(self.html)

        yield pages.ExampleExplanation
        save_html(self.html)

        yield pages.TestStart
        save_html(self.html)

        # Loop through each dynamically generated QuizPage
        for i in range(1, NUM_OF_QUESTIONS_INITIAL_TEST + 1):
            answer = "Approve" if SAMPLES_INITIAL_TEST['class'].iloc[i-1] == 1 else "Decline"
            yield pages.Question, {f"question{i}": answer}
            save_html(self.html)

        yield pages.ConfirmActive, dict(still_active='Yes')
        save_html(self.html)
