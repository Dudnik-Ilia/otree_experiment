import MainTest as pages
from otree.api import Bot

from helpers import save_html
from settings import NUM_OF_QUESTIONS_INITIAL_TEST, SAMPLES_MAIN_TEST


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Explanation
        save_html(self.html)
        yield pages.Belief, dict(belief_assessment0=50)
        save_html(self.html)
        yield pages.FeedbackExplanation
        save_html(self.html)
        yield pages.TreatmentIntro
        save_html(self.html)
        if self.participant.vars['treatment'] == 0:
            yield pages.TreatmentPassive
        else:
            yield pages.TreatmentActive
        save_html(self.html)
        
        for i in range(1, self.player.round_number*NUM_OF_QUESTIONS_INITIAL_TEST + 1):
            answer = "Approve" if SAMPLES_MAIN_TEST['class'].iloc[i-1] == 1 else "Decline"
            yield pages.Question, {f"question{i}": answer}
            save_html(self.html)
        yield pages.WaitForSignal1
        save_html(self.html)
        yield pages.Signal
        save_html(self.html)
        yield pages.Belief, dict(belief_assessment1=50)
        save_html(self.html)

        for i in range(1+(self.player.round_number)*NUM_OF_QUESTIONS_INITIAL_TEST,
                        (self.player.round_number+1)*NUM_OF_QUESTIONS_INITIAL_TEST + 1):
            answer = "Approve" if SAMPLES_MAIN_TEST['class'].iloc[i-1] == 1 else "Decline"
            yield pages.Question, {f"question{i}": answer}
            save_html(self.html)
        yield pages.WaitForSignal2
        save_html(self.html)
        yield pages.Signal
        save_html(self.html)
        yield pages.Belief, dict(belief_assessment2=50)
        save_html(self.html)
        