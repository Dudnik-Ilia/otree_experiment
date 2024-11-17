from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, cu, models, widgets

c = cu
doc = """
    GetID page where participants acknowledge they need a code to receive a payout and view their ID and total payoff.
"""


class C(BaseConstants):
    NAME_IN_URL = 'getID'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    acknowledgment = models.StringField(
        choices=[
            [
                'I am aware that I will not receive a payout without the code',
                'I am aware that I will not receive a payout without the code.'
            ]
        ],
        label='',
        widget=widgets.RadioSelect
    )


class GetID(Page):
    form_model = 'player'
    form_fields = ['acknowledgment']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.vars.get("all_completed") == True and participant.vars.get("dropout") == False

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
            ID=participant.vars.get("ID"),
            payoff=participant.payoff_plus_participation_fee(),
        )


class End(Page):
    form_model = 'player'


page_sequence = [GetID, End]