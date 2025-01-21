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
    sex = models.StringField(choices=[['female', 'female'], ['male', 'male']], label='Sex:')
    profession = models.StringField(
        choices=[
            ['technical', 'Technical/Engineering'],
            ['medical', 'Medical/Healthcare'],
            ['business', 'Business/Finance'],
            ['arts', 'Arts/Humanities'],
            ['science', 'Science/Research'],
            ['education', 'Education/Teaching'],
            ['other', 'Other']
        ],
        label='Professional Field:',
        widget=widgets.RadioSelect
    )
    age = models.StringField(
        choices=[
            ['14-18', '14-18 years'],
            ['19-25', '19-25 years'],
            ['26-35', '26-35 years'],
            ['36-45', '36-45 years'],
            ['46-60', '46-60 years'],
            ['60+', '60 years +']
        ],
        label='Age:',
        widget=widgets.RadioSelect
    )
    math_note = models.IntegerField(
        choices=[
            [3, 'Excellent'],
            [2, 'Good'],
            [1, 'Medium'],
            [0, 'Bad']
        ],
        label='Math grade in school:'
    )
    if_all_clear = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Were the instructions clear?')

    relevance_replacement = models.IntegerField(choices=[[i, f'{i}'] for i in range(1, 8)],
                                                 label="On a scale from 1 (very low) to 7 (very high), how relevant/probable do you consider a situation where \
                                                    AI models are integrated to replace around 1,000 branch-level managers in making critical decisions for loan approvals?",
                                                      widget=widgets.RadioSelectHorizontal)
    relevance_involvement = models.IntegerField(choices=[[i, f'{i}'] for i in range(1, 8)],
                                                 label="Rate on a scale from 1 (not at all) to 7 (very much) how strongly you\
                                                   tried to achieve the best performance result in the test.",
                                                     widget=widgets.RadioSelectHorizontal)
    relevance_ai_role = models.IntegerField(choices=[[i, f'{i}'] for i in range(1, 8)],
                                           label="On a scale from 1 (not at all) to 7 (very much), how likely do you think it \
                                            is that AI systems will play a central role in jobs traditionally held by humans?",
                                             widget=widgets.RadioSelectHorizontal)

    treatment_active1 = models.StringField(blank=True, choices=[['Hiring more managers to support AI', 'Hiring more managers to support AI'],
                                                                ['Replacing managers in branches', 'Replacing managers in branches'],
                                                                  ["Using AI only for minor tasks", "Using AI only for minor tasks"],
                                                                   ["Expanding the number of branches", "Expanding the number of branches"]],
                                             label='What was the potential impact of adopting the AI system mentioned in the study?',
                                             initial=False, widget=widgets.RadioSelect)
    treatment_active2 = models.StringField(blank=True, choices=[['Poor user interface design', 'Poor user interface design'],
                                                                ['Insufficient computing power', 'Insufficient computing power'],
                                                                  ["High financial cost", "High financial cost"],
                                                                   ["Loss of human knowledge", "Loss of human knowledge"]],
                                             label='What concern was mentioned about relying entirely on AI for decisions?',
                                             initial=False, widget=widgets.RadioSelect)


    treatment_passive1 = models.StringField(blank=True, choices=[['To reduce operational costs', 'To reduce operational costs'],
                                                                ['To completely replace managers', 'To completely replace managers'],
                                                                  ["To assist in decision-making processes", "To assist in decision-making processes"],
                                                                   ["To conduct psychological studies", "To conduct psychological studies"]],
                                             label='What was the stated purpose of integrating the AI support system?',
                                             initial=False, widget=widgets.RadioSelect)
    treatment_passive2 = models.StringField(blank=True, choices=[['Assess the AIs helpfulness', 'Assess the AIs helpfulness'],
                                                                ['Compare different management strategies', 'Compare different management strategies'],
                                                                  ["Identify poor-performing participants", "Identify poor-performing participants"],
                                                                   ["Evaluate the ethical implications of AI", "Evaluate the ethical implications of AI"]],
                                             label='What was the main goal of the study according to the description?',
                                             initial=False, widget=widgets.RadioSelect)

    how_truthful_question = models.IntegerField(
        choices=[
            [0, 'I tried to give my best possible estimate.'],
            [1, 'I did not think much and gave a random estimate.'],
            [2, 'I gave a (little/much) higher probability than my actual estimate.'],
            [3, 'I gave a (little/much) lower probability than my actual estimate.']
        ],
        label='Which of the following statements best describes your approach?',
        widget=widgets.RadioSelect
    )
    justification = models.LongStringField(label='Please describe your answer (optional)', blank=True)

    # Add payout if the questions were correct about Treatment
    def question_payoff(self):
        if self.treatment_active1=="Replacing managers in branches" and self.treatment_active2=="Loss of human knowledge":
                self.participant.payoff+=20
        if self.treatment_passive1=="To assist in decision-making processes" and self.treatment_passive2=="Assess the AIs helpfulness":
                self.participant.payoff+=20

class QuestionnaireStart(Page):
    form_model = 'player'

# Double check if the treatment was successfull
class TreatmentCheck(Page):
    form_model = 'player'
    form_fields = ['relevance_replacement', 'relevance_involvement', 'relevance_ai_role']

# Ask how truthful were the answers
class HowTruthfulQuestion(Page):
    form_model = 'player'
    form_fields = ['how_truthful_question', 'justification']

# To check whether participant read the treatment carefully + add payout
class TreatmentQuestion(Page):
    form_model = 'player'
    form_fields = ['treatment_active1', 'treatment_active2', 'treatment_passive1', 'treatment_passive2']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.question_payoff()
    def vars_for_template(player: Player):
        return dict(
            treatment = player.participant.vars['treatment'],
        )

class Demographics(Page):
    form_model = 'player'
    form_fields = ['sex', 'age', 'profession', 'math_note', 'if_all_clear']


page_sequence = [QuestionnaireStart, TreatmentCheck, HowTruthfulQuestion, TreatmentQuestion, Demographics]
