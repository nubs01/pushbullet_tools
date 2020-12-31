import eevee_ai.security as sec
import requests
import json
import platform
from contextlib import contextmanager
import argparse

PUSHBULLET_ENDPOINT = 'https://api.pushbullet.com/v2/pushes'
HOSTNAME = platform.node()

def pushbullet_message(title, body, token=None):
    """Send notification to pushbullet

    :param title: notification title
    :param body: body of notification
    :param token: (optional), API token to use, otherwise uses stored API token
    :type title: str
    :type body: str
    :type token: str
    """
    if token is None:
        token = sec.readToken('pushbullet')

    msg = {'type': 'note', 'title': title, 'body': body}
    resp = requests.post(PUSHBULLET_ENDPOINT, data=json.dumps(msg),
                         headers={'Access-Token': token,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Notifcation Error ', resp.status_code)
    else:
        print('Notification Sent')

@contextmanager
def push_alert(header='{hostname}', success_msg='Process complete!',
               fail_msg='{error}', closing_func=None):
    """contextmanager that will send a push message to all pushbullet linked
    devices when the contained processes are complete or when they error. Can
    also assign functions to be executed after everything else regardless of
    error.

    :param header: title of the push messages sent. {hostname} will insert the active computer's hostname
    :param success_msg: notification text on success
    :param fail_msg: notification text on error, {error} will insert a short version of the error thrown
    :param closing_func: function to be executed on exit, regardless of error
    :type header: str
    :type success_msg: str
    :type fail_msg: str
    :type closing_func: function
    """
    try:
        header = header.format(hostname=HOSTNAME)
    except KeyError:
        pass

    try:
        yield
        pushbullet_message(header, success_msg)
    except Exception as ex:
        try:
            fail_msg = fail_msg.format(error=str(ex))
        except KeyError:
            pass

        pushbullet_message(header + ' Error!', fail_msg)
        raise ex
    finally:
        if closing_func is not None:
            closing_func()

def setup(token):
    """Adds pushbullet API token to secrets directory and sends test message

    :param token: API token for pushbullet
    :type token: str
    """
    assert type(token) == str, 'token must be a str.'
    existing = sec.reatToken('pushbullet')
    if existing is not None:
        q = input('Stored token already exists for pushbullet. '
                  'Would you like to replace it? (y/n) ')
    else:
        q = 'y'

    if q == y:
        sec.writeToken('pushbullet', token, overwrite=True)
        print('New API token stored for pushbullet')
    else:
        print('Using existing token')

    pushbullet_message(HOSTNAME, 'Hello, World!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tool for sending push '
                                     'notifications via pushbullet')
    parser.add_argument('-t', '--token', type=str, help='API token for pushbullet')
    parser.add_argument('--config', action='store_true', help='store API '
                        'token and send test message. Allows future calls of '
                        'push_message to operate without a token input')
    parser.add_argument('--title', type=str, help='title of message to push', default=HOSTNAME)
    parser.add_argument('-m', dest='body', type=str, help='message to send')
    args = parser.parse_args()

    if args.config and args.token is not None:
        setup(args.token)
    elif args.config:
        parser.error('Must provide -t/--token argument in order to configure')
    else:
        pushbullet_message(args.title, args.body, token=args.token)
