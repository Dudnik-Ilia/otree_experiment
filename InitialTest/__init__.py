from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets
from settings import NUM_OF_QUESTIONS_INITIAL_TEST, SAMPLES_INITIAL_TEST, AI_ACCURACY
import random

c = cu
doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'InitialTest'
    PLAYERS_PER_GROUP=None
    NUM_ROUNDS = 1
    ADMIN_REPORT_TEMPLATE = 'InitialTest/admin_report.html'


class Subsession(BaseSubsession):
	pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    correct_answers = models.IntegerField(initial=0)
    current_question = models.IntegerField(initial=1)

    # INPUT FIELDS
    example_question = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']], label='Should we approve this loan request?', widget=widgets.RadioSelect)
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

    still_active = models.BooleanField(blank=True, choices=[[True, 'Yes'], [False, 'No']], initial=False,
                                       label='Please click "Yes" and "Continue" within 60 seconds if you continue to actively participate in the experiment', widget=widgets.RadioSelect)


class Intro(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player):
        return {
            'num_questions': NUM_OF_QUESTIONS_INITIAL_TEST,
        }


EXAMPLE_SAMPLE = {
	"Personal status and sex": "Male: single",
	"Housing status": "Owned house",
	"Credit history": "Established but risky credit history",
	"Bank account status": "No account in bank",
	"Savings account status": "More than 5k $",
	"Other credits": "No other credits",
	"Age (in years)": 40,
	"Installment rate: % of income used for loan payments": 1,
	"Credit amount (applicant has requested)": 10000,
	"Loan duration (months)": 6
}

class ExampleQuestion(Page):
    form_model = 'player'
    form_fields = ['example_question']
    timeout_seconds = 120
    @staticmethod
    def vars_for_template(player):
        return {
            'title': "Example Question",
            'sample_dict': EXAMPLE_SAMPLE,
        }


class ExampleExplanation(Page):
    form_model = 'player'
    timeout_seconds = 120
    @staticmethod
    def vars_for_template(player):
        return {
            'title': "Example Explanation",
            'sample_dict': EXAMPLE_SAMPLE,
        }

class TestStart(Page):
    form_model = 'player'


# Quiz Page for all quizes
class Question(Page):
    form_model = 'player'
    timeout_seconds = 60
    @property
    def form_fields(self):
        # Use player's current question to set form_fields dynamically
        return [f"question{self.player.current_question}"]
    @staticmethod
    def vars_for_template(player):
        # Get the current quiz field from the generator
        question_num = player.current_question
        ai_decision = SAMPLES_INITIAL_TEST['class'].iloc[question_num-1]
        ai_decision = "Approve" if ai_decision == 1 else "Decline"
        if random.random() > AI_ACCURACY:
            # Make incorrect prediction
            ai_decision = "Decline" if ai_decision == "Approve" else "Approve"
        return {
            'title': f"Question {question_num}/{NUM_OF_QUESTIONS_INITIAL_TEST}",
            'sample_dict': SAMPLES_INITIAL_TEST.iloc[question_num-1].to_dict(),
            'ai_decision': ai_decision,
            'real_decision': SAMPLES_INITIAL_TEST['class'].iloc[question_num-1] # For debugging
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Access the current question
        question_num = player.current_question
        user_answer = getattr(player, 'question'+str(question_num))
        real_answer = SAMPLES_INITIAL_TEST['class'].iloc[question_num-1]
        if (user_answer == "Approve" and real_answer == 1) or (user_answer == "Decline" and real_answer == 0):
            player.participant.payoff += 1
            player.correct_answers += 1
        # Increase question number
        player.current_question += 1


class ConfirmActive(Page):
    form_model = 'player'
    form_fields = ['still_active']
    timeout_seconds = 60
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        # Drop user if inactive
        if player.still_active!=True:
            player.participant.vars["dropout"]=True
            return 'Dropout'
        else:
            return upcoming_apps[0]


quiz_pages = [Question for _ in range(NUM_OF_QUESTIONS_INITIAL_TEST)]

page_sequence = [
    Intro, 
    ExampleQuestion, 
    ExampleExplanation,
    TestStart,
    *quiz_pages,
    ConfirmActive,
]