
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page, cu, widgets

c = cu
doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'Demographics'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ADMIN_REPORT_TEMPLATE = 'Demographics/admin_report.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Sex = models.StringField(choices=[['female', 'female'], ['male', 'male']], label='Sex:')
    Education = models.StringField(label='Education:')
    Age = models.IntegerField(label='Age:', max=100, min=14)
    MathNote = models.IntegerField(choices=[
            [0, 'Excellent'],
            [1, 'Good'],
            [2, 'Medium'],
            [3, 'Bad']
        ],
        label='Math note in school:')
    IfAllClear = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Were the instructions clear?')

    relevanceStudy = models.IntegerField(choices=[[i, ' '] for i in range(1, 8)], widget=widgets.RadioSelectHorizontal)
    relevanceProfession = models.IntegerField(choices=[[i, ' '] for i in range(1, 8)], widget=widgets.RadioSelectHorizontal)
    relevanceInvolvement = models.IntegerField(choices=[[i, ' '] for i in range(1, 8)], widget=widgets.RadioSelectHorizontal)

    ArticleQuestionPro = models.StringField(blank=True, choices=[['Kovacs and Convay', 'Kovacs and Convay'], ['True', 'DeVader und Alliger']],
                                             label='Wie heißen die Wissenschaftler, die gezeigt haben, dass intelligente Menschen ein größeres Führungspotential besitzen?',
                                             initial=False, widget=widgets.RadioSelect)
    ArticleQuestionCon = models.StringField(blank=True, choices=[['Nassim Djabou', 'Nassim Djabou'], ['True', 'Nassim Taleb']],
                                                label='Wie heißt der Wissenschaftler aus dem Artikel zur Bedeutung von Intelligenztests?',
                                                  initial=False, widget=widgets.RadioSelect)

    QuestionRating = models.IntegerField(
        choices=[
            [0, 'I tried to give my best possible estimate.'],
            [1, 'I did not think much and gave a random estimate.'],
            [2, 'I gave a higher probability than my actual estimate.'],
            [3, 'I gave a lower probability than my actual estimate.']
        ],
        label='Which of the following statements best describes your approach?',
        widget=widgets.RadioSelect
    )
    Justification = models.LongStringField(label='Please describe your answer')

    def question_payoff(self):
        participant = self.participant
        if self.ArticleQuestionPro=="True" or self.ArticleQuestionCon=="True":
                participant.payoff+=200


class QuestionnaireStart(Page):
    form_model = 'player'

class Relevance(Page):
    form_model = 'player'
    form_fields = ['relevanceStudy', 'relevanceProfession', 'relevanceInvolvement']

class Beliefs_Rational(Page):
    form_model = 'player'
    form_fields = ['QuestionRating', 'Justification']

class Article_Question(Page):
    form_model = 'player'
    form_fields = ['ArticleQuestionPro', 'ArticleQuestionCon']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.question_payoff()
    def vars_for_template(player: Player):
        return dict(
            treatment = player.participant.vars['treatment'],
        )

class Demographics(Page):
    form_model = 'player'
    form_fields = ['Sex', 'Age', 'Education', 'MathNote', 'IfAllClear']


page_sequence = [QuestionnaireStart, Relevance, Beliefs_Rational, Article_Question, Demographics]
