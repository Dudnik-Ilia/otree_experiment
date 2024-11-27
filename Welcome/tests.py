from otree.api import Bot

import Welcome as pages
from helpers import save_html

class PlayerBot(Bot):
    def play_round(self):
        save_html(self.html)
        yield pages.Confirmation, dict(confirm="Yes, I would like to participate in the experiment")
        save_html(self.html)

        yield pages.Welcome
        save_html(self.html)

        yield pages.Introduction
        save_html(self.html)
