from otree.api import Bot

import Dropout as pages
from helpers import save_html


class PlayerBot(Bot):
    def play_round(self):
        self.participant.vars['dropout'] = True
        yield pages.Dropout
        save_html(self.html)
