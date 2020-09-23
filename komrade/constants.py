# addresses
KOMRADE_ONION = 'u7spnj3dmwumzoa4.onion'
KOMRADE_ONION2 = 'rwg4zcnpwshv4laq.onion'
KOMRADE_URL = '68.66.241.111'  #KOMRADE_ONION


OPERATOR_API_URL_TOR = f'http://{KOMRADE_ONION}/op/'
OPERATOR_API_URL_CLEARNET = f'http://{KOMRADE_URL}/op/'

OPERATOR_API_URL = OPERATOR_API_URL_TOR

# paths
import os
PATH_USER_HOME = os.path.join(os.path.expanduser('~'))
PATH_KOMRADE = os.path.abspath(os.path.join(os.path.expanduser('~'),'komrade','data'))
PATH_KOMRADE_KEYS = os.path.join(PATH_KOMRADE,'.keys')
PATH_KOMRADE_DATA = os.path.join(PATH_KOMRADE,'.data')
PATH_KOMRADE_LIB = os.path.abspath(os.path.join(os.path.expanduser('~'),'komrade','lib'))

PATH_CRYPT_OP_KEYS = os.path.join(PATH_KOMRADE_KEYS,'.op.db.keys.crypt')
PATH_CRYPT_OP_DATA = os.path.join(PATH_KOMRADE_DATA,'.op.db.data.crypt')

# PATH_CRYPT_CA_KEYS = os.path.join(PATH_KOMRADE_KEYS,'.ca.db.keys.crypt')
# PATH_CRYPT_CA_DATA = os.path.join(PATH_KOMRADE_DATA,'.ca.db.data.encr')
PATH_CRYPT_CA_KEYS = PATH_CRYPT_OP_KEYS
PATH_CRYPT_CA_DATA = PATH_CRYPT_OP_DATA
PATH_QRCODES = os.path.join(PATH_KOMRADE,'contacts')
# PATH_SECRETS = os.path.join(PATH_KOMRADE,'.secrets')
PATH_SECRETS = PATH_SUPER_SECRETS = os.path.join(PATH_USER_HOME,'.secrets')
PATH_SUPER_SECRET_OP_KEY = os.path.join(PATH_SUPER_SECRETS,'.komrade.op.key')



PATH_LOG_OUTPUT = os.path.join(PATH_KOMRADE,'logs')


for x in [PATH_KOMRADE,PATH_KOMRADE_DATA,PATH_KOMRADE_KEYS,PATH_QRCODES,PATH_SECRETS,PATH_SUPER_SECRETS,PATH_LOG_OUTPUT]:
    if not os.path.exists(x):
        os.makedirs(x)

CRYPT_USE_SECRET = True
PATH_CRYPT_SECRET = os.path.join(PATH_SECRETS,'.salt')
PATH_CRYPT_SECRET_KEY = os.path.join(PATH_SECRETS,'.key')

# etc
BSEP=b'||||||||||'
BSEP2=b'@@@@@@@@@@'
BSEP3=b'##########'

OPERATOR_NAME = 'Operator'
TELEPHONE_NAME = 'Telephone'
WORLD_NAME = 'komrades'
PATH_REPO = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)
PATH_GUI = os.path.join(PATH_REPO,'komrade','app')
PATH_GUI_ASSETS = os.path.join(PATH_GUI,'assets')
PATH_DEFAULT_AVATAR = os.path.join(PATH_GUI_ASSETS,'avatars','marxbot.png')


PATH_REPO = PATH_APP = os.path.abspath(os.path.dirname(__file__))
# PATH_APP = os.path.join(PATH_REPO,'komrade')
# PATH_BUILTIN_KEYCHAINS_ENCR = os.path.join(PATH_APP,'.builtin.keychains.encr')
PATH_BUILTIN_KEYCHAIN = os.path.join(PATH_APP,'.builtin.keys')
PATH_OMEGA_KEY = os.path.join(PATH_APP,'.omega.key')
# PATH_BUILTIN_KEYCHAINS_DECR = os.path.join(PATH_APP,'.builtin.keychains.decr')
PATH_GUI = os.path.join(PATH_APP, )

# key names

KEYNAMES = [
    'pubkey','privkey','adminkey',
    'pubkey_encr','privkey_encr','adminkey_encr',
    'pubkey_decr','privkey_decr','adminkey_decr',
    'pubkey_encr_encr','privkey_encr_encr','adminkey_encr_encr',
    'pubkey_encr_decr','privkey_encr_decr','adminkey_encr_decr',
    'pubkey_decr_encr','privkey_decr_encr','adminkey_decr_encr',
    'pubkey_decr_decr','privkey_decr_decr','adminkey_decr_decr'
]

OPERATOR_INTERCEPT_MESSAGE = "If you'd like to make a call, please hang up and try again. If you need help, hang up, and then dial your operator."



# KEYMAKER_DEFAULT_KEYS_TO_SAVE = ['pubkey_encr', 'privkey_encr', 'adminkey_encr']
# KEYMAKER_DEFAULT_KEYS_TO_RETURN =  ['pubkey_decr_encr', 'privkey_decr_encr', 'adminkey_decr_encr']


# defaults oriented to Callers

# kept on server
KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_SERVER = ['pubkey']   # stored under QR URI

# kept on client
KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_CLIENT = ['privkey_encr','privkey_decr']
                                   #'pubkey'  # as QR
                                #    'privkey_encr',  
                                #    'adminkey_encr',
                                #    'privkey_decr'],
                                   #'privkey_decr_encr',
                                   #'privkey_decr_decr',
                                #    'adminkey_decr_encr',
                                #    'adminkey_decr_decr']

# KEYMAKER_DEFAULT_KEYS_TO_GEN =  ['pubkey','privkey','adminkey',
                                #  'pubkey_decr','privkey_decr', 'adminkey_decr']
KEYMAKER_DEFAULT_KEYS_TO_GEN = ['pubkey','privkey']
KEYMAKER_DEFAULT_KEYS_TO_GEN += KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_SERVER
KEYMAKER_DEFAULT_KEYS_TO_GEN += KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_CLIENT
KEYMAKER_DEFAULT_KEYS_TO_GEN = list(set(KEYMAKER_DEFAULT_KEYS_TO_GEN))
KEYMAKER_DEFAULT_KEYS_TO_GEN.sort(key=lambda x: x.count('_'))

# print('KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_SERVER',KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_SERVER)
# print('KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_CLIENT',KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_CLIENT)
# print('KEYMAKER_DEFAULT_KEYS_TO_GEN',KEYMAKER_DEFAULT_KEYS_TO_GEN)


KEY_TYPE_ASYMMETRIC_PUBKEY = 'asymmetric_pubkey'
KEY_TYPE_ASYMMETRIC_PRIVKEY = 'asymmetric_privkey'
KEY_TYPE_SYMMETRIC_WITHOUT_PASSPHRASE = 'symmetric_key_without_passphrase'
KEY_TYPE_SYMMETRIC_WITH_PASSPHRASE = 'symmetric_key_with_passphrase'
ENCRYPTED_KEY = 'encrypted_key'




KEYMAKER_DEFAULT_ALL_KEY_NAMES = KEYNAMES

WHY_MSG = 'password: '#What is the password of memory for this account? '



TELEPHONE_KEYCHAIN = None
OPERATOR_KEYCHAIN = None
WORLD_KEYCHAIN = None
OMEGA_KEY = None
OPERATOR = None
TELEPHONE = None




PATH_OPERATOR_WEB_KEYS_FILE = f'/home/ryan/www/website-komrade/pub'
PATH_OPERATOR_WEB_KEYS_URL = f'http://{KOMRADE_URL}/pub'
# PATH_OPERATOR_WEB_CONTACTS_DIR = '/home/ryan/www/website-komrade/.contacts'
# PATH_OPERATOR_WEB_CONTACT_OP_URL = f'http://{KOMRADE_URL}/.contacts/TheOperator.png'
# PATH_OPERATOR_WEB_CONTACT_PH_URL = f'http://{KOMRADE_URL}/.contacts/TheTelephone.png'


# dangerous! leave on only if absolutely necessary for initial dev
ALLOW_CLEARNET = True


DEBUG_DEFAULT_PASSPHRASE = None # 'all your base are belong to us'


ROUTE_KEYNAME = 'request'


OPERATOR_INTRO = 'Hello, this is the Operator speaking. '




VISIBILITY_TYPE_PUBLIC = 'VISIBILITY_TYPE_PUBLIC'  # visible to the world
VISIBILITY_TYPE_SEMIPUBLIC = 'VISIBILITY_TYPE_SEMIPUBLIC'  # visible to the world
VISIBILITY_TYPE_PRIVATE = 'VISIBILITY_TYPE_PRIVATE'  # visible to the world

DEFAULT_USER_SETTINGS = {
    'visibility':VISIBILITY_TYPE_SEMIPUBLIC
}

import os
SHOW_LOG = 1
SHOW_STATUS = 0
PAUSE_LOGGER = 0
CLEAR_LOGGER = 0

SAVE_LOGS = 1

CLI_TITLE = 'KOMRADE'
CLI_FONT = 'clr5x6'#'colossal'
CLI_WIDTH = STATUS_LINE_WIDTH = 60
CLI_HEIGHT = 30


MAX_POST_LEN = 1000
MAX_MSG_LEN = 1000


import os,logging
if not 'KOMRADE_SHOW_LOG' in os.environ or not os.environ['KOMRADE_SHOW_LOG'] or os.environ['KOMRADE_SHOW_LOG']=='0':
    logger = logging.getLogger()
    logger.propagate = False

if not 'KOMRADE_USE_TOR' in os.environ or not os.environ['KOMRADE_USE_TOR']:
    KOMRADE_USE_TOR = os.environ['KOMRADE_USE_TOR'] = '1'
if not 'KOMRADE_USE_CLEARNET' in os.environ or not os.environ['KOMRADE_USE_CLEARNET']:
    KOMRADE_USE_CLEARNET = os.environ['KOMRADE_USE_CLEARNET'] = '0'



FONT_PATH = os.path.join(PATH_GUI_ASSETS,'font.otf')