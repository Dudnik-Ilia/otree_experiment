import itertools

TREATMENT_CYCLE = itertools.cycle([1, 0])

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 4
    }

SESSION_CONFIGS =   [
    {
        'name': 'Motivated_Belief_Updating',
        'num_demo_participants': 1,
        'app_sequence': [
            # 'Confirmation', 
            # 'Welcome', 
            'Control_Questions',
            # 'IQ_Test', 
            # 'Beliefs_Signals', 
            # 'Questionnaire'
            'Dropout', 
            # 'getID'
        ]
    },
    {
        'name': 'IQ_Test',
        'num_demo_participants': 1,
        'app_sequence': [
            'IQ_Test', 'Dropout'
        ]
    },
    {
        'name': 'Belief',
        'num_demo_participants': 1,
        'app_sequence': [
            'Beliefs_Signals', 'Questionnaire', 'Dropout'
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

# IQ_Test
NUMBER_OF_QUIZES = 15
NUMBER_OF_CONTROL_QUESTIONS = 3
NUM_ROUNDS_CONTROL_QUESTIONS = 3

NUMBER_OF_BELIEFS = 3
NUMBER_OF_SIGNALS=2