from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets
from settings import NUMBER_OF_QUESTIONS
import random

c = cu
doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'Initial Test'
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
    example_question = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']],
                                label='Should we approve this loan request?',
                                  widget=widgets.RadioSelect)
    Question1 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']],
                                label='Should we approve this loan request?',
                                  widget=widgets.RadioSelect)
    Question2 = models.StringField(choices=[['Approve', 'Approve'], ['Decline', 'Decline']],
                                label='Should we approve this loan request?',
                                  widget=widgets.RadioSelect)
    still_active = models.BooleanField(blank=True, choices=[[True, 'Yes'], [False, 'No']], initial=False,
                                       label='Please click "Yes" and "Continue" within 60 seconds if you continue to actively participate in the experiment', widget=widgets.RadioSelect)

    @staticmethod
    def random_number():
        return random.randrange(10,50,10)


class Intro(Page):
    form_model = 'player'


class ExampleQuestion(Page):
    form_model = 'player'
    form_fields = ['example_question']
    timeout_seconds = 30
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Make correct choice for future explanation
        player.example_question="Approve"


class ExampleExplanation(Page):
    form_model = 'player'
    form_fields = ['example_question']


class TestStart(Page):
    form_model = 'player'


class ConfirmActive(Page):
    form_model = 'player'
    form_fields = ['still_active']
    timeout_seconds = 60
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Drop user if inactive
        if player.still_active!=True: 
            player.participant.vars["dropout"]=True
            return 'Dropout'


# Quiz Page for all quizes
class Question(Page):
    form_model = 'player'
    timeout_seconds = 30
    
    @property
    def form_fields(self):
        # Use player's current question to set form_fields dynamically
        return [f"Question{self.player.current_question}"]

    @staticmethod
    def vars_for_template(player):
        # Get the current quiz field from the generator
        question_num = player.current_question
        return {
            'question_num': question_num,
            'title': f"Question {question_num}/{NUMBER_OF_QUESTIONS}",
            'image': f"IQ_Test/Quiz_4_4_{question_num}.PNG"
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Access the current quiz field dynamically
        quiz_num = player.current_question
        if getattr(player, 'Quiz'+str(quiz_num)) == 'True':
            player.participant.payoff += player.random_number()
            player.correct_answers += 1
        # Increase question number
        player.current_question += 1
    

quiz_pages = [Question for _ in range(NUMBER_OF_QUESTIONS)]

page_sequence = [
    Intro, 
    ExampleQuestion, 
    ExampleExplanation,
    TestStart,
    *quiz_pages,
    ConfirmActive,
]