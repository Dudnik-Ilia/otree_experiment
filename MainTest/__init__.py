from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets
import random

from settings import NUM_OF_BELIEFS, NUM_OF_QUESTIONS_MAIN_TEST_PER_ROUND, NUM_OF_SIGNALS, SAMPLES_MAIN_TEST, TREATMENT_CYCLE, AI_ACCURACY, PROBA_CORRECT_MESSENGER

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
    current_round = models.IntegerField(initial=1)
    current_question = models.IntegerField(initial=1)

    # Results
    correct_answers_round1 = models.IntegerField(initial=0)
    correct_answers_round2 = models.IntegerField(initial=0)

    signal1 = models.StringField()
    signal2 = models.StringField()

    # INPUT
    belief_assessment1 = models.IntegerField(label='Your assessment in %:', max=100, min=0)
    belief_assessment2 = models.IntegerField(label='Your assessment in %:', max=100, min=0)
    belief_assessment3 = models.IntegerField(label='Your assessment in %:', max=100, min=0)

    question1 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question2 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question3 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question4 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question5 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question6 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question7 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question8 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question9 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question10 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question11 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question12 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question13 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question14 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question15 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question16 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question17 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question18 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question19 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
    question20 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)

    @staticmethod
    def add_payout_correct_quest():
        return random.randrange(1,5,1)

    def get_signal(self, singal_num: int):
        # Get result in the round
        praticipant_result = getattr(self, f'correct_answers_round{singal_num}')
        # Decide whether we are going to tell the truth
        to_tell_truth = True if random.random() < PROBA_CORRECT_MESSENGER else False
        signal = praticipant_result > AI_ACCURACY
        if not to_tell_truth:
            signal = not signal # Lie
        setattr(self, f'signal{singal_num}', int(signal))


class Explanation(Page):
    form_model = 'player'

class FeedbackExplanation(Page):
    form_model = 'player'


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


class Signal(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            signal = getattr(player, f"signal{player.current_round}"),
        )


class Belief(Page):
    form_model = 'player'
    timeout_seconds = 30
    @property
    def form_fields(self):
        return [f"belief_assessment{self.player.current_round}"]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_round += 1


class WaitForSignal1(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.get_signal(singal_num=1)

class WaitForSignal2(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.get_signal(singal_num=2)

# Quiz Page for all quizes
class Question(Page):
    form_model = 'player'
    timeout_seconds = 60
    @property
    def form_fields(self):
        # Use player's current question to set form_fields dynamically
        return [f"question{self.player.current_question}"]
    @staticmethod
    def vars_for_template(player: Player):
        # Get the current quiz field from the generator
        question_num = player.current_question
        ai_decision = SAMPLES_MAIN_TEST['class'].iloc[question_num-1]
        ai_decision = "Approve" if ai_decision == 1 else "Decline"
        if random.random() > AI_ACCURACY:
            # Make incorrect prediction
            ai_decision = "Decline" if ai_decision == "Approve" else "Approve"
        return {
            'title': f"Question {question_num%(NUM_OF_QUESTIONS_MAIN_TEST_PER_ROUND+1)}/{NUM_OF_QUESTIONS_MAIN_TEST_PER_ROUND}",
            'sample_dict': SAMPLES_MAIN_TEST.iloc[question_num-1].to_dict(),
            'ai_decision': ai_decision,
            'real_decision': SAMPLES_MAIN_TEST['class'].iloc[question_num-1] # For debugging
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Access the current question
        question_num = player.current_question
        user_answer = getattr(player, 'question'+str(question_num))
        real_answer = SAMPLES_MAIN_TEST['class'].iloc[question_num-1]
        # If correctly classified
        if (user_answer == "Approve" and real_answer == 1) or (user_answer == "Decline" and real_answer == 0):
            # Increase payout a bit
            player.participant.payoff += player.add_payout_correct_quest()
            # Increment correct answers
            correct_answers_round = getattr(player, 'correct_answers_round'+str(player.current_round))
            setattr(player, 'correct_answers_round'+str(player.current_round), correct_answers_round+1)
        # Increase question number
        player.current_question += 1


belief_pages = [Belief for _ in range(NUM_OF_BELIEFS)]
signal_pages = [Signal for _ in range(NUM_OF_SIGNALS)]
quiz_pages_1 = [Question for _ in range(NUM_OF_QUESTIONS_MAIN_TEST_PER_ROUND)]
quiz_pages_2 = [Question for _ in range(NUM_OF_QUESTIONS_MAIN_TEST_PER_ROUND)]

page_sequence = [Explanation, belief_pages[0], FeedbackExplanation, # Explanations
                  TreatmentIntro, TreatmentPassive, TreatmentActive, # Treatment
                    *quiz_pages_1, WaitForSignal1, signal_pages[0], belief_pages[1], # Round 1
                      *quiz_pages_2, WaitForSignal2, signal_pages[1], belief_pages[2], # Round 2
                      ]
