import json
import os
from dotenv import load_dotenv
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen



# Access variables in env file
load_dotenv()
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIANC = os.getenv('API_AUDIANC')


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def get_error_message(self):
        return self.error['code'], self.error['description']


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''

def get_token_auth_header():
    # Check Authorization sent with headers
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'Authorization_header is missing',
            'description': 'Except to receive Authorization'
        }, 401)

    # Store authorization
    auth = request.headers['Authorization']

    # unpack auth
    auth_parts = auth.split(' ')
    # Make it two because it should consist with bearer and token
    if len(auth_parts) != 2:
        raise AuthError({
            "code": "Invalid_header",
            "description": "Token Not found"
        }, 401)

    elif auth_parts[0].lower() != 'bearer':
        raise AuthError({
            "code": "Invalid_header",
            "description": "Authorization header must start with bearer"
        }, 401)

    token = auth_parts[1]
    return token


# DECODE TOKEN
def verify_decode_jwt(token):
    """ arg : token : a json web token (jwt), return payloads
     which contain token,ras_key and audience """
    jsonurl = urlopen(
        f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization malform'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIANC,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )

            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid claim',
                'description': "Incorrect claims please check" +
                        "audience and issuer"
            }, 400)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unabel to parse authentication token'
            }, 401)
    raise AuthError({
        'code': 'Invalid_header',
        'description': "Unable to find a property key"
    }, 401)


# CHECK PERMISSIONS
def check_permissions(permission, payload):
    """Take payload that came from verify_decode_jwt
        func and permission which pass as a string,
        If payload contains permission return True
        or False if payload not contain any permissions """
    if 'permissions' not in payload:
        raise AuthError({'code': 'Invalid_claims',
                         'description': 'Permissions not include with JWT'
                         }, 400)
    if permission not in payload['permissions']:
        raise AuthError({'code': 'unauthorized',
                         'description': 'Permissions not found'
                         }, 403)
    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    !!NOTE urlopen has a common certificate error
     described here:
      https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


# REQUIRE AUTH
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator