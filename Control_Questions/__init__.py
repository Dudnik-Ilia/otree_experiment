from otree.api import BaseConstants, BasePlayer, BaseSubsession,\
    BaseGroup, models, Page, widgets
from settings import NUMBER_OF_CONTROL_QUESTIONS, NUM_ROUNDS_CONTROL_QUESTIONS

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
    CORRECT_ANSWERS = ('30%', '50%', 'No')


class Player(BasePlayer):
    attempts = models.IntegerField(initial=1)
    # Input fields
    interactive = models.IntegerField(label='Answer in %:', max=100, min=0)
    cntr_quest_1 = models.StringField(choices=[['60%', '60%'], ['True', '30%'], ['20%', '20%']],
                                        label='1. Which probability should you specify to have the highest chance \
                                        of receiving a payout of 2 Euros?',
                                        widget=widgets.RadioSelect)
    cntr_quest_2 = models.StringField(choices=[['True', '50%'], ['40%', '40%'], ['30%', '30%']],
                                         initial='0',
                                         label='2. What is your probability of winning 2 Euros?',
                                         widget=widgets.RadioSelect)
    cntr_quest_3 = models.StringField(choices=[['Yes', 'Yes'], ['True', 'No']],
                                        label='3. Would you have had a higher probability of winning 2 Euros \
                                              if you had indicated a probability of 60% instead of 30%?',
                                        widget=widgets.RadioSelect)
    
    def _calculate_points(self) -> int:
        correct_questions = []
        wrong_questions = []
        for question in range(1, NUMBER_OF_CONTROL_QUESTIONS+1):
            if getattr(self, 'cntr_quest_'+str(question)) == 'True':
                correct_questions.append(question)
            else:
                wrong_questions.append(question)
        self.participant.vars['wrong_questions'] = wrong_questions
        return len(correct_questions)

    def check_answers(self) -> bool:
        control_points = self._calculate_points()
        # Register attempt
        if control_points < NUMBER_OF_CONTROL_QUESTIONS:
            self.attempts += 1
        if control_points == NUMBER_OF_CONTROL_QUESTIONS:
            return True
        return False


class ControlQuestions(Page):
    form_model = 'player'
    form_fields = ['interactive', 'cntr_quest_1', 'cntr_quest_2', 'cntr_quest_3']


class Result(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if_correct = player.check_answers()
        return {
            'wrong_questions': str(player.participant.vars['wrong_questions']),
            'quiz_correct': if_correct,
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.check_answers():
            return upcoming_apps[0] # Proceed
        elif player.attempts > NUM_ROUNDS_CONTROL_QUESTIONS:
            # Drop user if attempts > allowed
            player.participant.vars['dropout'] = True
            return 'Dropout'
        else:
            # Do again (stay here)
            return None

page_sequence = [ControlQuestions, Result]
