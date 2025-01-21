import itertools
import pandas as pd

# Cycle to iterate over the treatment
TREATMENT_CYCLE = itertools.cycle([1, 0])

# ================================
# MTurk Settings

qualifications = [
    # At least 60% of HITs approved
    {
        'QualificationTypeId': "000000000000000000L0",
        'Comparator': "GreaterThanOrEqualTo",
        'IntegerValues': [60]
    },
]

mturk_hit_settings=dict(
    keywords='bonus, study',
    title='Credit Assessment Study',
    description='Financial company conducting a study to assess decision-making in credit approval.',
    frame_height=500,
    template='global/mturk_template.html',
    minutes_allotted_per_assignment=60,
    expiration_hours=1 * 24,
    qualification_requirements=qualifications
    # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes
),


SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 0.1,
    'mturk_hit_settings': mturk_hit_settings
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
            'Payout',
            'Dropout', 
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
        'name': 'MainTest',
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
NUM_OF_QUESTIONS_INITIAL_TEST = 10
SAMPLES_INITIAL_TEST = pd.read_csv('_static/samples/picked_samples.csv')
# ControlQuestions
NUM_OF_CONTROL_QUESTIONS = 3
NUM_ROUNDS_CONTROL_QUESTIONS = 3
# MainTest
NUM_OF_BELIEFS = 3
NUM_OF_SIGNALS=2
NUM_OF_QUESTIONS_MAIN_TEST_PER_ROUND = 10
SAMPLES_MAIN_TEST = pd.read_csv('_static/samples/picked_samples_main.csv')
