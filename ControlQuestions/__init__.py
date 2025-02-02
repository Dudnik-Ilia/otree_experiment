from otree.api import BaseConstants, BasePlayer, BaseSubsession,\
    BaseGroup, models, Page, widgets
from settings import NUM_OF_CONTROL_QUESTIONS, NUM_ROUNDS_CONTROL_QUESTIONS

doc = """
    Control Questions checking whether the player understands how to answer on questions regarding probabilities.
"""

# Empty placeholders, not used here
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass


class C(BaseConstants):
    NAME_IN_URL = 'Control_Questions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = NUM_ROUNDS_CONTROL_QUESTIONS
    # CORRECT_ANSWERS = ('30%', 'No')


class Player(BasePlayer):
    if_correct = models.BooleanField(initial=False)
    # Input fields
    cntr_quest_1 = models.StringField(choices=[['60%', '60%'], ['True', '30%'], ['20%', '20%']],
                                        label='1. Which probability should you specify to have the highest chance \
                                        of receiving an additional payout?',
                                        widget=widgets.RadioSelect)
    cntr_quest_2 = models.StringField(choices=[['Yes', 'Yes'], ['True', 'No']],
                                        label='2. Would you have had a higher probability of winning additional payout \
                                              if you had indicated a probability of 60% instead of 30%?',
                                        widget=widgets.RadioSelect)
    
    def _calculate_points(self) -> int:
        correct_questions = []
        wrong_questions = []
        for question in range(1, NUM_OF_CONTROL_QUESTIONS+1):
            if getattr(self, 'cntr_quest_'+str(question)) == 'True':
                correct_questions.append(question)
            else:
                wrong_questions.append(question)
        self.participant.vars['wrong_questions'] = wrong_questions
        return len(correct_questions)

    def check_answers(self) -> None:
        if 'control_attempts' not in self.participant.vars:
            self.participant.vars['control_attempts'] = 1
        control_points = self._calculate_points()
        # Register attempt
        if control_points < NUM_OF_CONTROL_QUESTIONS:
            self.participant.vars['control_attempts'] += 1
        if control_points == NUM_OF_CONTROL_QUESTIONS:
            self.if_correct = True
        else:
            self.if_correct = False


class ControlQuestions(Page):
    form_model = 'player'
    form_fields = ['cntr_quest_1', 'cntr_quest_2']


class Result(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        player.check_answers()
        return {
            'attempt': player.participant.vars['control_attempts'],
            'wrong_questions': str(player.participant.vars['wrong_questions']),
            'quiz_correct': player.if_correct,
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.if_correct:
            return upcoming_apps[0] # Proceed
        elif player.participant.vars['control_attempts'] == NUM_ROUNDS_CONTROL_QUESTIONS:
            # Drop user if attempts > allowed
            player.participant.vars['dropout'] = True
            return 'Dropout'
        else:
            # Do again (stay here for more round)
            return None

page_sequence = [ControlQuestions, Result]
