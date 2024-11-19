from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets

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

    confirm = models.StringField(
        choices=[['Yes', 'Yes, I would like to participate in the experiment']],
        label='',
        widget=widgets.RadioSelect
    )
    has_confirmed = models.BooleanField()

    # Method to save a unique ID for the player
    def save_id(self):
        self.participant.vars["id"] = self.id


class Confirmation(Page):
    form_model = 'player'
    form_fields = ['confirm']
    timeout_seconds = 10

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        
        if timeout_happened:
            player.has_confirmed = False
            participant.vars["dropout"] = True
        else:
            player.has_confirmed = True
            participant.vars["dropout"] = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        participant = player.participant
        if participant.vars["dropout"] == True:
            return "Dropout"


class Welcome(Page):
    form_model = 'player'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.save_id()


class Introduction(Page):
    form_model = 'player'


page_sequence = [Confirmation, Welcome, Introduction]
