from otree.api import Bot

import Payout as pages
from helpers import save_html


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Payout, {'acknowledgment': 'I am aware that I will not receive a payout without the code'}
        save_html(self.html)
        yield pages.End
        save_html(self.html)
