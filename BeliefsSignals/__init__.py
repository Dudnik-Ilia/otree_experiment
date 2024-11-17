
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets
import random

from settings import NUMBER_OF_BELIEFS, NUMBER_OF_SIGNALS, TREATMENT_CYCLE

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

    # INPUT
    a = models.IntegerField()
    b1 = models.IntegerField()
    b2 = models.IntegerField()

    signal1 = models.StringField()
    signal2 = models.StringField()
    prob_signal1 = models.FloatField()
    prob_signal2 = models.FloatField()

    Einschaetzung1 = models.IntegerField(label='Ihre Einschätzung in X%:', max=100, min=0)
    Einschaetzung2 = models.IntegerField(label='Ihre Einschätzung in X%:', max=100, min=0)
    Einschaetzung3 = models.IntegerField(label='Ihre Einschätzung in X%:', max=100, min=0)

    randomX1 = models.IntegerField()
    randomX2 = models.IntegerField()
    randomX3 = models.IntegerField()

    def get_signal(self, singal_num: int):
        setattr(self, f'prob_signal{singal_num}', 200/3)
        setattr(self, f'b{singal_num}', random.randint(0,100))
        prob_signal = getattr(self, f'prob_signal{singal_num}')
        b = getattr(self, f'b{singal_num}')
        # TODO
        participant_result = 1.0
        if participant_result > 0.5:
            if b<=prob_signal: 
                msg = "Your performance was in the top 50%"
            else: 
                msg = "Your performance was not in the top 50%"
        else:
            if b<=prob_signal: 
                msg = "Your performance was not in the top 50%"
            else: 
                msg= "Your performance was in the top 50%"
        setattr(self, f'signal{singal_num}', msg)

    def define_payoff(self, pay_number: int):
        participant = self.participant
        setattr(self, f'randomX{pay_number}', random.randint(0,100))
        Einschaetzung = getattr(self, f"Einschaetzung{pay_number}")
        randomX = getattr(self, f"randomX{pay_number}")
        participant_result = 1.0
        if Einschaetzung>randomX:
            if participant_result > 0.5:
                participant.payoff+=200
        else:
            self.a=random.randint(0,100)
            if self.a<=randomX:
                participant.payoff+=200


class Explanation(Page):
    form_model = 'player'

class Feedback_Explanation(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.get_signal(singal_num=1)
        player.get_signal(singal_num=2)


class ArticleInstruction(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Assign Treatment
        player.participant.vars['treatment'] = next(TREATMENT_CYCLE)

class ArticleCon(Page):
    form_model = 'player'
    timeout_seconds = 5
    @staticmethod
    def is_displayed(player: Player):
        if player.participant.vars['treatment'] == 0:
            return True

class ArticlePro(Page):
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
        return [f"Einschaetzung{self.player.current_belief_page}"]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.define_payoff(pay_number=player.current_belief_page)
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
                  ArticleInstruction, ArticleCon, ArticlePro,
                    WaitForSignal1, signal_pages[0], belief_pages[1],
                      WaitForSignal2, signal_pages[1], belief_pages[2]]