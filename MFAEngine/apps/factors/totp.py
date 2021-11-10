
from passlib.totp import TOTP
from passlib.exc import UsedTokenError, InvalidTokenError, MalformedTokenError
import pyqrcode


"""
    MFAServer wrapper for passLib TOTP library.
    ---------------

    Todo:
    ------

    1/ ...
"""


class FactoryTOTP(TOTP):
    
    def __init__(self, totp_params):

        self.totp_params = totp_params

        self.digits = self.totp_params['DIGITS']
        self.period = self.totp_params['PERIOD']
        self.alg = self.totp_params['ALG']
        self.issuer = self.totp_params['ISSUER']


    def create_factory(self, secret=None):

        totpfactory = TOTP.using(
            digits = self.digits,
            period = self.period, 
            alg = self.alg,
            issuer = self.issuer, 
            secrets = secret
        )
        
        return totpfactory


    def get_factory(self, instance):
        
        return instance


    def get_totp_instance(self, factory):

        return factory.new()
        

    def store_totp_instance(self, instance):
        
        return instance.to_json()


    def get_key(self, factory, instance):

        key = factory.from_json(instance).pretty_key()

        return key


    def config_client(self, factory, label, key):

        client = factory(key)
        
        return client.to_uri(label, self.totp_params['ISSUER'])


    def get_qrcode(self, uri):

        qrcode = pyqrcode.create(uri)

        b64_qrcode = qrcode.png_as_base64_str(scale=5)

        b64_qrcode_url = "data:image/png;base64,{}".format(b64_qrcode)
        
        return b64_qrcode_url


    def get_token(self, factory, key):

        token = factory(key).generate(None).token

        return token


    def verify_token(self, token, factory, instance):

        instance = factory.from_json(instance)

        try:
            return factory.verify(token, instance)
        except MalformedTokenError as err:
            return err
        except InvalidTokenError as err:
            return err
        except UsedTokenError as err:
            return err


##SampleTest

totp_def = {
    'DIGITS' : 6, 
    'PERIOD' : 30,
    'PERIOD_SKEW' : 0, 
    'ALG' : 'sha1', 
    'ISSUER' : 'mfa.server.com',
}


init = FactoryTOTP(totp_def)
factory = init.create_factory()
instance = init.get_totp_instance(factory)
instance = instance.to_json()
key = init.get_key(factory, instance)
key_URI = init.config_client(factory, "andykawa3@gmail.com", key)
print(key_URI)
print(init.get_token(factory, key))
print(init.get_token(factory, key))
res = init.verify_token(init.get_token(factory, key), factory, instance)
print(res.__class__.__name__)
print(init.get_qrcode(key_URI))