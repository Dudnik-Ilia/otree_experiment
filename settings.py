import itertools
import pandas as pd

TREATMENT_CYCLE = itertools.cycle([1, 0])

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 4
    }

SESSION_CONFIGS =   [
    {
        'name': 'Main',
        'num_demo_participants': 1,
        'app_sequence': [
            'Welcome', 
            'ControlQuestions',
            'InitialTest', 
            'MainTest', 
            'Questionnaire',
            'Dropout', 
            'Payout',
        ]
    },
    {
        'name': 'InitialTest',
        'num_demo_participants': 1,
        'app_sequence': [
            'InitialTest', 'Dropout'
        ]
    },
    {
        'name': 'Belief',
        'num_demo_participants': 1,
        'app_sequence': [
            'MainTest', 'Questionnaire', 'Dropout'
        ]
    }
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

SECRET_KEY = 'secret_key'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
# ================================
# Model accuracy
AI_ACCURACY = 0.5
# Accuracy of the messenger
PROBA_CORRECT_MESSENGER = 0.66
# InitialTest
NUMBER_OF_QUESTIONS_INITIAL_TEST = 10
SAMPLES_INITIAL_TEST = pd.read_csv('_static/samples/picked_samples.csv')
# ControlQuestions
NUMBER_OF_CONTROL_QUESTIONS = 3
NUM_ROUNDS_CONTROL_QUESTIONS = 3
# BeliefsSignals
NUMBER_OF_BELIEFS = 3
NUMBER_OF_SIGNALS=2
