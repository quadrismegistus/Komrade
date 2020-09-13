import os,sys; sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')),'..')))
from komrade import *
from komrade.backend.crypt import *
from abc import ABC, abstractmethod

# common external imports
from pythemis.skeygen import KEY_PAIR_TYPE, GenerateKeyPair
from pythemis.smessage import SMessage, ssign, sverify
from pythemis.skeygen import GenerateSymmetricKey
from pythemis.scell import SCellSeal
from pythemis.exception import ThemisError


 
class KomradeKey(ABC,Logger):
    @abstractmethod
    def encrypt(self,msg,**kwargs): pass
    @abstractmethod
    def decrypt(self,msg,**kwargs): pass
    @abstractmethod
    def data(self): pass
    @property
    def data_b64(self):return b64encode(self.data) if type(self.data)==bytes else self.data.data_b64
    @property
    def data_b64_s(self):
        return self.data_b64.decode()
    @property
    def discreet(self): return make_key_discreet(self.data)
    def __str__(self):
        return repr(self)


class KomradeSymmetricKey(KomradeKey):
    @property
    def cell(self):
        if not hasattr(self,'_cell'):
            # if hasattr(self,'passphrase') and self.passphrase:
            #     self._cell = SCellSeal(passphrase=hasher(self.passphrase))
            # elif hasattr(self,'key') and self.key:
            #     self._cell = SCellSeal(key=self.key)
            self._cell = SCellSeal(key=self.key)
        return self._cell
    def encrypt(self,msg,**kwargs):
        if hasattr(msg,'data'): msg=msg.data
        # print('??? dec',msg,kwargs)
        
        return self.cell.encrypt(msg,**kwargs)
    def decrypt(self,msg,**kwargs):
        if hasattr(msg,'data'): msg=msg.data
        # print('??? dec',msg,kwargs)
        
        try:
            return self.cell.decrypt(msg,**kwargs)
        except TypeError:
            return self.cell.decrypt(msg.data,**kwargs)


def getpass_status(passphrase=None):
    while not passphrase:
        passphrase1 = getpass(f'@Keymaker: What is a *memorable* pass word or phrase? Do not write it down.\n@{name}: ')
        passphrase2 = getpass(f'@Keymaker: Could you repeat that?')
        if passphrase1!=passphrase2:
            self.status('@Keymaker: Those passwords didn\'t match. Please try again.',clear=False,pause=False)
        else:
            return passphrase1

# get_pass_func = getpass_status if SHOW_STATUS else getpass
from getpass import getpass
        
class KomradeSymmetricKeyWithPassphrase(KomradeSymmetricKey):
    def hash(self,x): return self.crypt_keys.hash(x)

    def __init__(self,passphrase=DEBUG_DEFAULT_PASSPHRASE, why=WHY_MSG):
        # if not passphrase:
        #     # raise KomradeException
        #     passphrase=getpass(why)
        # else:
        #     self.passphrase=passphrase
        # # if passphrase: self.passphrase=passphrase
        pass

    @property
    def data(self): return KEY_TYPE_SYMMETRIC_WITH_PASSPHRASE.encode('utf-8')
    def __repr__(self): return f'[Symmetric Key] (generated by password)'
    @property
    def cell(self):
        if not hasattr(self,'_cell'):
            from getpass import getpass
            self._cell = SCellSeal(passphrase=hasher(getpass(WHY_MSG)))
        return self._cell


class KomradeSymmetricKeyWithoutPassphrase(KomradeSymmetricKey):
    def __init__(self,key=None):
        self.key = GenerateSymmetricKey() if not key else key
    @property
    def data(self): return self.key
    def __repr__(self): return f'[Symmetric Key]\n    ({self.discreet})'



class KomradeAsymmetricKey(KomradeKey):
    def __init__(self,pubkey=None,privkey=None):
        if not pubkey or not privkey:
            keypair = GenerateKeyPair(KEY_PAIR_TYPE.EC)
            privkey = keypair.export_private_key()
            pubkey = keypair.export_public_key()
        self.pubkey=pubkey
        self.privkey=privkey    
        self.privkey_obj = KomradeAsymmetricPrivateKey(privkey,pubkey)
        self.pubkey_obj = KomradeAsymmetricPublicKey(pubkey,privkey)

    def encrypt(self,msg,pubkey=None,privkey=None):
        if issubclass(type(msg), KomradeKey) or issubclass(type(msg), KomradeEncryptedKey): msg=msg.data
        pubkey=pubkey if pubkey else self.pubkey
        privkey=privkey if privkey else self.privkey
        return SMessage(privkey,pubkey).wrap(msg)
    def decrypt(self,msg,pubkey=None,privkey=None):
        if issubclass(type(msg), KomradeKey) or issubclass(type(msg), KomradeEncryptedKey): msg=msg.data
        pubkey=pubkey if pubkey else self.pubkey
        privkey=privkey if privkey else self.privkey
        return SMessage(privkey.data,pubkey.data).unwrap(msg)
    @property
    def data(self): return self.key
    
class KomradeAsymmetricPublicKey(KomradeAsymmetricKey):
    def __init__(self,pubkey,privkey=None):
        self.pubkey=pubkey
        self.privkey=privkey
    @property
    def key(self): return self.pubkey
    @property
    def data(self): return self.pubkey 
    
    def __repr__(self): return f'''[Asymmetric Public Key]\n    ({self.data_b64.decode()})'''
class KomradeAsymmetricPrivateKey(KomradeAsymmetricKey):
    def __init__(self,privkey,pubkey=None):
        self.pubkey=pubkey
        self.privkey=privkey
    @property
    def data(self): return self.privkey 
    @property
    def key(self): return self.privkey
    def __repr__(self): return f'''[Asymmetric Private Key]\n    ({self.discreet})'''

def make_key_discreet(data,chance_unredacted=0.25):
    import random

    if not data: return '?'
    if not isBase64(data): data=b64encode(data)
    key=data.decode()

    return ''.join((k if random.random()<chance_unredacted else '-') for k in key)
    # return ''.join((k if not i%6 or not i%3 else '-') for i,k in enumerate(key))


def make_key_discreet_str(string,chance_unredacted=0.25):
    import random
    if not string: return '?'
    return ''.join((k if random.random()<chance_unredacted else '-') for k in string)


def make_key_discreet1(data,len_start=10,len_end=10,ellipsis='.',show_len=True):
    if not data: return '?'
    if not isBase64(data): data=b64encode(data)
    data=data.decode()
    amt_missing = len(data) - len_start - len_end
    dstr = data[:len_start] + (ellipsis*amt_missing)
    if len_end: dstr+=data[-len_end:]
    return f'{dstr}' #' (+{len(data)-len_start-len_end})'

class KomradeEncryptedKey(Logger):
    def __init__(self,data): self.data=data
    @property
    def data_b64(self): return b64encode(self.data).decode()
    def __repr__(self): return f'[Encrypted Key]\n    ({self.discreet})'
    @property
    def discreet(self): return make_key_discreet(self.data)
    def __str__(self):
        return repr(self)

class KomradeEncryptedAsymmetricPrivateKey(KomradeEncryptedKey):
    def __repr__(self): return f'[Encrypted Asymmetric Private Key]\n    ({self.discreet})'
class KomradeEncryptedAsymmetricPublicKey(KomradeEncryptedKey):
    def __repr__(self): return f'[Encrypted Asymmetric Public Key]\n    ({self.discreet})'
class KomradeEncryptedSymmetricKey(KomradeEncryptedKey):
    def __repr__(self): return f'[Encrypted Symmetric Key]\n    ({self.discreet})'



KEYMAKER_DEFAULT_KEY_TYPES = {
    'pubkey':KomradeAsymmetricPublicKey,
    'privkey':KomradeAsymmetricPrivateKey,
    'adminkey':KomradeSymmetricKeyWithoutPassphrase,
    
    'pubkey_decr':KomradeSymmetricKeyWithoutPassphrase,
    'privkey_decr':KomradeSymmetricKeyWithPassphrase,
    'adminkey_decr':KomradeSymmetricKeyWithPassphrase,

    'pubkey_decr_decr':KomradeSymmetricKeyWithoutPassphrase,
    'privkey_decr_decr':KomradeSymmetricKeyWithPassphrase,
    'adminkey_decr_decr':KomradeSymmetricKeyWithPassphrase,

    'pubkey_encr_decr':KomradeSymmetricKeyWithoutPassphrase,
    'privkey_encr_decr':KomradeSymmetricKeyWithPassphrase,
    'adminkey_encr_decr':KomradeSymmetricKeyWithPassphrase,


    # encrypted keys
    'pubkey_encr':KomradeEncryptedAsymmetricPublicKey,
    'privkey_encr':KomradeEncryptedAsymmetricPrivateKey,
    'adminkey_encr':KomradeEncryptedSymmetricKey,
    'pubkey_encr_encr':KomradeEncryptedSymmetricKey,
    'privkey_encr_encr':KomradeEncryptedSymmetricKey,
    'adminkey_encr_encr':KomradeEncryptedSymmetricKey,
    'pubkey_decr_encr':KomradeEncryptedSymmetricKey,
    'privkey_decr_encr':KomradeEncryptedSymmetricKey,
    'adminkey_decr_encr':KomradeEncryptedSymmetricKey
}





def get_key_obj(keyname,data,passphrase=None,key_types=KEYMAKER_DEFAULT_KEY_TYPES):
    return key_types[keyname](data)









class Keymaker(Logger):
    def __init__(self,
                name=None,
                passphrase=DEBUG_DEFAULT_PASSPHRASE,
                uri_id=None,
                keychain={},
                path_crypt_keys=PATH_CRYPT_CA_KEYS,
                path_crypt_data=PATH_CRYPT_CA_DATA):
        
        # set defaults
        self.name=name
        self._uri_id=uri_id
        self._pubkey=None
        self._keychain=keychain
        self.path_crypt_keys=path_crypt_keys
        self.path_crypt_data=path_crypt_data

        # boot keychain
        # self._keychain = self.keychain(passphrase=passphrase)


    def find_pubkey(self,name=None):
        if not name: name=self.name
        if 'pubkey' in self._keychain and self._keychain['pubkey']:
            return self._keychain['pubkey']
        res = self.crypt_keys.get(name, prefix='/pubkey/')
        res = self.load_qr(self.name)
        if not res: return
        return b64dec(res)
        
        # self.log('I don\'t know my public key! Do I need to register?')
        # raise KomradeException(f'I don\'t know my public key!\n{self}\n{self._keychain}')
        # return res

    def find_name(self,pubkey_b64):
        res = self.crypt_keys.get(b64enc(q), prefix='/name/')
        return res

    @property
    def keys(self):
        return sorted(list(self.keychain().keys()))
    
    @property
    def top_keys(self):
        return [k for k in self.keys if k.count('_')==0]

    def load_keychain_from_bytes(self,keychain):
        for keyname,keyval in keychain.items():
            keychain[keyname] = get_key_obj(keyname,keyval)
        return keychain

    def find_pubkey_and_name(self,name=None,pubkey=None):
        if not pubkey: pubkey = self._keychain.get('pubkey')
        if not name: name = self.name

        if pubkey:
            # print('??',pubkey)
            if hasattr(pubkey,'data'):
                pubkey=pubkey.data_b64
            else:
                pubkey=b64enc(pubkey)

        # if name and pubkey:
            # make sure they match
            #assert self.find_pubkey(name) == self.find_name(pubkey)
            # if self.find_pubkey(name) != self.find_name:
                # pass
                # self.log(f'! {name} and {pubkey} do not match?')
        if name and not pubkey:
            pubkey = self.find_pubkey(name)
        elif pubkey and not name:
            self.name = self.find_name(pubkey)
        # else:
            # self.log('error! Neither name nor pubkey! Who am I?')
            # return (None,None)
        
        if pubkey:
            # self.log('!?!?!?!?',type(pubkey),pubkey)
            pubkey = b64dec(pubkey)
            pubkey=KomradeAsymmetricPublicKey(pubkey)
        
        self._keychain['pubkey'] = pubkey
        self.name = name

        self.log('found for name and pubkey',name,pubkey)
        
        return (name,pubkey)

    def keychain(self,look_for=KEYMAKER_DEFAULT_ALL_KEY_NAMES,passphrase=None):
        # load existing keychain
        keys = self._keychain
        
        # make sure we have the pubkey
        name,pubkey = self.find_pubkey_and_name()

        # get uri
        if pubkey:
            uri = pubkey.data_b64
            #uri = b64encode(pubkey) if type(pubkey)==bytes else b64encode(pubkey.encode())
            # get from cache
            for keyname in look_for:
                # print(self.name,'looking for key:',keyname)
                # if keyname in keys and keys[keyname]: continue
                key = self.crypt_keys.get(uri,prefix=f'/{keyname}/')
                # print('found in crypt:',key,'for',keyname)
                if key: keys[keyname]=get_key_obj(keyname,key)
        
        # try to assemble
        keys = self.assemble(self.assemble(keys,passphrase=passphrase),passphrase=passphrase)
        
        #store to existing set
        self._keychain = keys
        
        #return
        return keys


    @property
    def pubkey(self): return self.keychain().get('pubkey')
    @property
    def pubkey_b64(self): return b64encode(self.pubkey) #self.keychain().get('pubkey')
    @property
    def privkey(self): return self.keychain().get('privkey')
    @property
    def adminkey(self): return self.keychain().get('adminkey')
    @property
    def pubkey_encr(self): return self.keychain().get('pubkey_encr')
    @property
    def privkey_encr(self): return self.keychain().get('privkey_encr')
    @property
    def adminkey_encr(self): return self.keychain().get('adminkey_encr')
    @property
    def pubkey_decr(self): return self.keychain().get('pubkey_decr')
    @property
    def privkey_decr(self): return self.keychain().get('privkey_decr')
    @property
    def adminkey_decr(self): return self.keychain().get('adminkey_decr')


    def load_qr(self,name):
        # try to load?
        contact_fnfn = os.path.join(PATH_QRCODES,name+'.png')
        if not os.path.exists(contact_fnfn): return ''
        # with open(contact_fnfn,'rb') as f: dat=f.read()
        from pyzbar.pyzbar import decode
        from PIL import Image
        res= decode(Image.open(contact_fnfn))[0].data

        # self.log('QR??',res,b64decode(res))
        return b64decode(res)

    @property
    def uri_id(self):
        if not self._uri_id:
            pubkey = self.pubkey #find_pubkey()
            self._uri_id = pubkey.data_b64
        return self._uri_id


    ### BASE STORAGE
    @property
    def crypt_keys(self):
        if not hasattr(self,'_crypt_keys'):
            self._crypt_keys = Crypt(fn=self.path_crypt_keys)
        return self._crypt_keys

    @property
    def crypt_keys_mem(self):
        if not hasattr(self,'_crypt_keys_mem'):
            self._crypt_keys_mem = CryptMemory()
        return self._crypt_keys_mem
        
    @property
    def crypt_data(self):
        if not hasattr(self,'_crypt_data'):
            self._crypt_data = Crypt(fn=self.path_crypt_data)
        return self._crypt_data

    def can_log_in(self):
        if not self.pubkey: return False
        if not (self.privkey or self.privkey_encr): return False
        return True
    

    ### CREATING KEYS
    
    def get_new_keys(self):
        raise KomradeException('Every keymaker must make their own get_new_keys() !')



    def gen_keys_from_types(self,key_types=KEYMAKER_DEFAULT_KEY_TYPES,passphrase=DEBUG_DEFAULT_PASSPHRASE):
        """
        Get new asymmetric/symmetric keys, given a dictionary of constants describing their type
        """
        # print('bbbbb')

        asymmetric_pubkey=None
        asymmetric_privkey=None
        keychain = {}

        self.log('got key types:',dict_format(key_types))
        
        # gen keys requested
        for key_name,key_class in key_types.items():
            ## asymmetric?
            if issubclass(key_class,KomradeAsymmetricKey):
                if not asymmetric_privkey or asymmetric_pubkey:
                    asymmetric_keys = KomradeAsymmetricKey()
                    asymmetric_pubkey = asymmetric_keys.pubkey_obj
                    asymmetric_privkey = asymmetric_keys.privkey_obj
            
            if key_class == KomradeAsymmetricPublicKey:
                keychain[key_name]=asymmetric_pubkey
            elif key_class == KomradeAsymmetricPrivateKey:
                keychain[key_name]=asymmetric_privkey

            elif key_class == KomradeSymmetricKeyWithPassphrase:
                keychain[key_name] = KomradeSymmetricKeyWithPassphrase(passphrase)
            else:
                # print('??',key_name,key_class)
                keychain[key_name] = key_class(None)
            
        self.log('keytypes -> keychain',dict_format(keychain))
        return keychain



    


    def forge_new_keys(self,
                        name=None,
                        passphrase=DEBUG_DEFAULT_PASSPHRASE,
                        keys_to_save = KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_SERVER,
                        keys_to_return = KEYMAKER_DEFAULT_KEYS_TO_SAVE_ON_CLIENT,
                        keys_to_gen = KEYMAKER_DEFAULT_KEYS_TO_GEN,
                        key_types = KEYMAKER_DEFAULT_KEY_TYPES,
                        save_keychain=True,
                        return_keychain=True,
                        return_all_keys=False):
        # setup
        keys_to_gen = set(keys_to_gen) | set(keys_to_save) | set(keys_to_return)
        keys_to_gen = sorted(list(keys_to_gen),key=lambda x: x.count('_'))
        key_types = dict([(k,key_types[k]) for k in keys_to_gen if k])
        if not name: name=self.name



        # show user what's happening
        self.log(f'''
Keymaker ({self}) is forging new keys for {name}
''' + (f'''
* I will save these keys in this crypt: {', '.join(keys_to_save)}
''' if save_keychain else '') #+ #'''
# * I will also save this user's pubkey (as b64 URI) to:
        # {self.get_path_qrcode(name=name)}
# ''' + (f'''
+ (f'''
* I will return these keys to you: {', '.join(keys_to_return)}
''' if return_keychain else '')
+ f'''
* I will forge these keys for you: {', '.join(keys_to_gen)}

* I will be using these key types to do so:
    {dict_format(key_types,tab=4)}
''')

        

        # gen decryptor keys!
        keychain = self.gen_keys_from_types(key_types,passphrase=passphrase)
        # gen encrypted keys!
        self.log('I built this keychain v1!',dict_format(keychain,tab=2))
        
        keychain = self.disassemble(keychain,passphrase=passphrase)
        self.log('I built this keychain!',dict_format(keychain,tab=2))
        self.status('@Keymaker: I ended up building these keys:',keychain)
        

        # save keys!
        if save_keychain:
            # get URI id to save under (except for pubkeys, accessible by name)
            uri_id,keys_saved_d,keychain = self.save_keychain(name,keychain,keys_to_save)
            self.log(f'Trying to save these keys ({keys_to_save}), I saved this keychain:',dict_format(keys_saved_d,tab=2),'using the generated-from-pubkey URI ID',uri_id)

        # return keys!
        if return_all_keys:
            return keychain

        if return_keychain:
            keys_returned = self.return_keychain(keychain,keys_to_return)
            self.log('I am returning this keychain:',dict_format(keys_returned,tab=2))
            # return (uri_id,keys_returned)
            return keys_returned

        raise KomradeException('What did you want me to do here?')
        
                
    def return_keychain(self,keychain,keys_to_return=None):
        keychain_toreturn = {}
        if not keys_to_return: keys_to_return = list(keychain.keys())
        for key in keys_to_return:
            if key in keychain:
                keychain_toreturn[key]=keychain[key]
        return keychain_toreturn

    def get_path_qrcode(self,name=None,dir=None,ext='.png'):
        if not name: name=self.name
        if not dir: dir = PATH_QRCODES
        fnfn = os.path.join(dir,name+ext)
        return fnfn

    @property
    def qr(self): return self.qr_str(data=self.uri_id)

    def qr_str(self,data=None):
        data = self.uri_id if not data else data
        return get_qr_str(data)
        

    def save_uri_as_qrcode(self,uri_id=None,name=None):
        if not uri_id: uri_id = self.uri_id
        if not uri_id and not self.uri_id: raise KomradeException('Need URI id to save!')
        if not name: name=self.name

        # gen
        import pyqrcode
        qr = pyqrcode.create(uri_id)
        ofnfn = self.get_path_qrcode(name=name)
        qr.png(ofnfn,scale=5)
        
        self._uri_id = uri_id
        self.log(f'''Saved public key as QR code to:\n{ofnfn}\n\n{self.qr}''')
        return ofnfn

    def save_keychain(self,name,keychain,keys_to_save=None,uri_id=None):
        if not keys_to_save: keys_to_save = list(keychain.keys())
        if not uri_id and 'pubkey' in keychain:
            uri_id = b64encode(keychain['pubkey'].data).decode() #uri_id = get_random_id() + get_random_id()
        # self.log(f'SAVING KEYCHAIN FOR {name} under URI {uri_id}')
        self._uri_id = uri_id
        # filter for transfer
        for k,v in keychain.items():
            if issubclass(type(v),KomradeKey):
                v=v.data
            keychain[k]=v
        
        # save keychain
        keys_saved_d={}
        for keyname in keys_to_save:
            if not '_' in keyname and keyname!='pubkey':
                self.log('there is no private property in a socialist network! all keys must be split between komrades',keyname)
            if keyname in keychain:
                # uri = uri_id
                uri = uri_id if keyname!='pubkey' else name
                if not uri: raise KomradeException('invalid URI! {uri}')
                val = keychain[keyname]
                if issubclass(type(keychain[keyname]), KomradeKey) or issubclass(type(keychain[keyname]), KomradeEncryptedKey):
                    val = val.data
                self.crypt_keys.set(uri,val,prefix=f'/{keyname}/')
                keys_saved_d[keyname] = keychain[keyname]

        # save pubkey as QR
        if not 'pubkey' in keys_saved_d:
            # self.log('did not save pubkey in crypt, storing as QR...')
            self.save_uri_as_qrcode(name=name, uri_id=uri_id)

        # set to my keychain right away
        self._keychain = keychain

        return (uri_id,keys_saved_d,keychain)

    def assemble(self,keychain,passphrase=None,key_types=KEYMAKER_DEFAULT_KEY_TYPES,decrypt=True):
        encr_keys = [k for k in keychain.keys() if k.endswith('_encr')]
        for encr_key_name in encr_keys:
            decr_key_name = encr_key_name[:-5] + '_decr'
            unencr_key_name = encr_key_name[:-5]
            # self.log(encr_key_name,decr_key_name,unencr_key_name)
            if decrypt and unencr_key_name in keychain: continue
            if not decr_key_name in keychain:
                # self.log('looking for decr key name:',decr_key_name,keychain)
                keychain[decr_key_name] = KomradeSymmetricKeyWithPassphrase(passphrase=passphrase)
            else:
                continue
            decr_key = keychain.get(decr_key_name)
            # self.log('?',decr_key,decr_key_name,encr_key_name,keychain[encr_key_name])

            try:
                if decrypt:
                    encr_key = keychain.get(encr_key_name)
                    # self.log(f'about to decrypt {encr_key} with {decr_key}')
                    unencr_key = decr_key.decrypt(encr_key.data)
                    keychain[unencr_key_name] = get_key_obj(unencr_key_name,unencr_key)
                else:
                    # unencr_key = keychain.get(unencr_key_name)
                    self.log(f'about to encrypt {unencr_key} with {decr_key}')
                    encr_key = decr_key.encrypt(unencr_key.data)
                    keychain[encr_key_name] = get_key_obj(encr_key_name,encr_key)
            except ThemisError as e:
                self.log('error!!',decrypt,decr_key,encr_key,decr_key_name,encr_key_name)
                pass

        return keychain

    def disassemble(self,keychain,**kwargs):
        return self.assemble(keychain,decrypt=False,**kwargs)



if __name__ == '__main__':
    keymaker = Keymaker('marx69')
    keychain = keymaker.forge_new_keys()

    print(keychain)