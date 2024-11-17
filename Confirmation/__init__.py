from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets, Page, cu

c = cu
doc = """
    Confirmation page where participants confirm their willingness to participate in the experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Confirmation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


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
    has_confirmed = models.BooleanField(initial=False)


class Confirmation(Page):
    form_model = 'player'
    form_fields = ['confirm']
    timeout_seconds = 10

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.vars["dropout"] = False
        participant.vars["id"] = 0

        if timeout_happened:
            player.has_confirmed = False
            participant.vars["dropout"] = True

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        participant = player.participant
        if participant.vars["dropout"]:
            return "Dropout"


page_sequence = [Confirmation]
