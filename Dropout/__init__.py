from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, cu

c = cu
doc = """
    Dropout page informing participants that they have opted out of the experiment and should close the browser window.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Dropout'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Dropout(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if not getattr(participant.vars, "dropout", False):
            print("Dropout is False! Check that it is awaited")
        participant.payoff = 0  # Set participation fee to zero
        return True


page_sequence = [Dropout]
