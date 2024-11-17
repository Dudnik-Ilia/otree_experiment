from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets
from settings import NUMBER_OF_QUIZES
import random

c = cu
doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'IQ_Test'
    PLAYERS_PER_GROUP=None
    NUM_ROUNDS = 1
    ADMIN_REPORT_TEMPLATE = 'IQ_Test/admin_report.html'


class Subsession(BaseSubsession):
    total_answers = models.FloatField()
    odd_players = models.IntegerField(initial=0)
    a = models.IntegerField(initial=0)
    b = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    correct_answers = models.FloatField(initial=0)
    attempts = models.IntegerField(initial=1)
    current_question = models.IntegerField(initial=1)
    odd = models.IntegerField(initial=0)

    # INPUT FIELDS
    example_question = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz1 = models.StringField(choices=[['A', 'A'], ['True', 'B'], ['C', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz2 = models.StringField(choices=[['A', 'A'], ['True', 'B'], ['C', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz3 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['True', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz4 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['True', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz5 = models.StringField(choices=[['True', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz6 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['True', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz7 = models.StringField(choices=[['A', 'A'], ['True', 'B'], ['C', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz8 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['True', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz9 = models.StringField(choices=[['True', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']],
                                label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                  widget=widgets.RadioSelect)
    Quiz10 = models.StringField(choices=[['A', 'A'], ['True', 'B'], ['C', 'C'], ['D', 'D']],
                                 label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                   widget=widgets.RadioSelect)
    Quiz11 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['True', 'D']],
                                 label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                   widget=widgets.RadioSelect)
    Quiz12 = models.StringField(choices=[['True', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']],
                                 label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                   widget=widgets.RadioSelect)
    Quiz13 = models.StringField(choices=[['True', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']],
                                 label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                   widget=widgets.RadioSelect)
    Quiz14 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['True', 'C'], ['D', 'D']],
                                 label='Welcher Ausschnitt ist die richtige Ergänzung?',
                                   widget=widgets.RadioSelect)
    Quiz15 = models.StringField(choices=[['A', 'A'], ['B', 'B'], ['C', 'C'], ['True', 'D']],
                                 label='Welcher Ausschnitt ist die richtige Ergänzung?',
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
        player.example_question="A"


class ExampleExplanation(Page):
    form_model = 'player'
    form_fields = ['example_question']


class QuizStart(Page):
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
class QuizPage(Page):
    form_model = 'player'
    timeout_seconds = 30
    
    @property
    def form_fields(self):
        # Use player's current question to set form_fields dynamically
        return [f"Quiz{self.player.current_question}"]

    @staticmethod
    def vars_for_template(player):
        # Get the current quiz field from the generator
        quiz_num = player.current_question
        return {
            'title': f"Question {quiz_num}/{NUMBER_OF_QUIZES}",
            'image': f"IQ_Test/Quiz_4_4_{quiz_num}.PNG"
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
    

quiz_pages = [QuizPage for _ in range(NUMBER_OF_QUIZES)]

page_sequence = [
    Intro, 
    ExampleQuestion, 
    ExampleExplanation,
    QuizStart,
    *quiz_pages,
    ConfirmActive,
]