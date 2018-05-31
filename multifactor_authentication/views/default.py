import json
import pyotp
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import UserSecret


@view_config(route_name='home', renderer='../templates/twofactor.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(UserSecret)
        one = query.filter(UserSecret.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'multifactor_authentication'}


@view_config(route_name='create_view', renderer='../templates/create_secret.jinja2')
def create_view(request):
    return {}

@view_config(route_name='authenticate', renderer='json')
def authenticate(request):
    try:
        payload = request.json_body
        username = payload.get(u'username')
        code = payload.get(u'code')
        query = request.dbsession.query(UserSecret)
        user_secret = query.filter(UserSecret.name == username).one_or_none()
        if not user_secret:
            return {u'success': False}
        totp = pyotp.TOTP(user_secret.value)
        success = totp.verify(code)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {u'success': success}


@view_config(route_name='create_secret', renderer='../templates/qrcode.jinja2')
def createSecret(request):
    """
    Create and share a secret for Multi Factor Authentication with an AccountUser
    :return: The url of the QR code that contains the secret
    :throws: InvalidValue if the account_user_uuid is not valid
    """
    username = request.matchdict['username']
    secret = pyotp.random_base32()
    user_secret = request.dbsession.query(UserSecret).filter(UserSecret.name == username).one_or_none()
    if user_secret:
        user_secret.value = secret
    else:
        user_secret = UserSecret(name=username, value=secret)
        request.dbsession.add(user_secret)

    request.dbsession.flush()
    totp = pyotp.TOTP(secret)
    qr_data = totp.provisioning_uri('My TwoFactor Authentication') # this will be the entry name in the Google Authenticator App
    qr_src = 'http://chart.apis.google.com/chart?cht=qr&chs=250x250&chl={0}'.format(qr_data)
    return {'qrcode': qr_src, 'secret': secret}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_multifactor_authentication_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
