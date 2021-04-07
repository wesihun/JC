from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app


class Token(object):
    def __init__(self):
        pass

    def generate_token(self, id='1', expiration=60 * 10):
        """生成token"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'id': id}).decode('ascii')
        return token

    def verify_auth_token(self, token):
        """token验证"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token,but expired
        except BadSignature:
            return None  # invalid token

        return data
