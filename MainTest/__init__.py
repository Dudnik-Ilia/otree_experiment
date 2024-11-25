
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets
import random

from settings import NUMBER_OF_BELIEFS, NUMBER_OF_SIGNALS, TREATMENT_CYCLE, AI_ACCURACY, PROBA_CORRECT_MESSENGER

c = cu
doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'Beliefs_Signals'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ADMIN_REPORT_TEMPLATE = 'Beliefs_Signals/admin_report.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # For dynamic pages
    current_belief_page = models.IntegerField(initial=1)
    current_signal_page = models.IntegerField(initial=1)

    # Results
    result_round1 = models.FloatField()
    result_round2 = models.FloatField()

    signal1 = models.StringField()
    signal2 = models.StringField()

    # INPUT
    belief_assessment1 = models.IntegerField(label='Your assessment in %:', max=100, min=0)
    belief_assessment2 = models.IntegerField(label='Your assessment in %:', max=100, min=0)
    belief_assessment3 = models.IntegerField(label='Your assessment in %:', max=100, min=0)

    def get_signal(self, singal_num: int):
        # Get result in the round
        praticipant_result = getattr(self, f'result_round{singal_num}')
        # Decide whether we are going to tell the truth
        to_tell_truth = True if random.random() < PROBA_CORRECT_MESSENGER else False
        signal = praticipant_result > AI_ACCURACY
        if not to_tell_truth:
            signal = not signal # Lie
        setattr(self, f'signal{singal_num}', int(signal))


class Explanation(Page):
    form_model = 'player'

class Feedback_Explanation(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.get_signal(singal_num=1)
        player.get_signal(singal_num=2)


class TreatmentIntro(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Assign Treatment
        player.participant.vars['treatment'] = next(TREATMENT_CYCLE)

class TreatmentPassive(Page):
    form_model = 'player'
    timeout_seconds = 5
    @staticmethod
    def is_displayed(player: Player):
        if player.participant.vars['treatment'] == 0:
            return True

class TreatmentActive(Page):
    form_model = 'player'
    timeout_seconds = 5
    @staticmethod
    def is_displayed(player: Player):
        if player.participant.vars['treatment'] == 1:
            return True


class Belief(Page):
    form_model = 'player'
    timeout_seconds = 30
    @property
    def form_fields(self):
        return [f"belief_assessment{self.player.current_belief_page}"]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_belief_page += 1


class Signal(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            signal = getattr(player, f"signal{player.current_signal_page}"),
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_signal_page += 1


class WaitForSignal1(Page):
    form_model = 'player'

class WaitForSignal2(Page):
    form_model = 'player'



belief_pages = [Belief for _ in range(NUMBER_OF_BELIEFS)]
signal_pages = [Signal for _ in range(NUMBER_OF_SIGNALS)]

page_sequence = [Explanation, belief_pages[0], Feedback_Explanation,
                  TreatmentIntro, TreatmentPassive, TreatmentActive,
                    WaitForSignal1, signal_pages[0], belief_pages[1],
                      WaitForSignal2, signal_pages[1], belief_pages[2]]
