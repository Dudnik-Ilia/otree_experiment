from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu
from datetime import datetime

c = cu
doc = """
    Welcome page that generates a unique participant ID and initializes tracking variables for the experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Welcome'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SESSION_STRING = 'N'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payoff_id = models.StringField()

    # Method to generate a unique ID for the player
    def create_id(self):
        current_date = datetime.now().strftime("%Y%m%d")
        self.participant.vars["ID"] = current_date + C.SESSION_STRING + str(self.id_in_group)
        self.payoff_id = self.participant.vars["ID"]


class Welcome(Page):
    form_model = 'player'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.create_id()



page_sequence = [Welcome]
