from otree.api import Bot


class PlayerBot(Bot):
    def play_round(self):
        self.participant.vars['dropout'] = True
        pass
