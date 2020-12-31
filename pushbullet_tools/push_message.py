import keyring
import requests
import json
import platform
from contextlib import contextmanager
import argparse
import getpass

PUSHBULLET_ENDPOINT = 'https://api.pushbullet.com/v2/pushes'
HOSTNAME = platform.node()
USERNAME = getpass.getuser()

def push_note(title, body, token=None):
    """Send notification to pushbullet

    :param title: notification title
    :param body: body of notification
    :param token: (optional), API token to use, otherwise uses API token from keyring
    :type title: str
    :type body: str
    :type token: str
    """
    if token is None:
        token = keyring.get_password('pushbullet', USERNAME)

    assert token is not None, 'No API token is stored and none was given'

    msg = {'type': 'note', 'title': title, 'body': body}
    resp = requests.post(PUSHBULLET_ENDPOINT, data=json.dumps(msg),
                         headers={'Access-Token': token,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Notifcation Error ', resp.status_code)
    else:
        print('Notification Sent')


def push_link(title, body, url, token=None):
    """Send notification to pushbullet

    :param title: notification title
    :param body: body of notification
    :param url: link url to send
    :param token: (optional), API token to use, otherwise uses API token from keyring
    :type title: str
    :type body: str
    :type url: str
    :type token: str
    """
    if token is None:
        token = keyring.get_password('pushbullet', USERNAME)

    assert token is not None, 'No API token is stored and none was given'

    msg = {'type': 'link', 'title': title, 'body': body, 'url': url}
    resp = requests.post(PUSHBULLET_ENDPOINT, data=json.dumps(msg),
                         headers={'Access-Token': token,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Notifcation Error ', resp.status_code)
    else:
        print('Notification Sent')


def push_file(file_name, file_type, file_url, body='', token=None):
    """Send notification to pushbullet

    :param file_name: name of the file
    :param file_type: file MIME type of the file
    :param file_url: file download url
    :param body: (optional) message to go with file
    :param token: (optional), API token to use, otherwise uses API token from keyring
    :type file_name: str
    :type file_type: str
    :type file_url: str
    :type body: str
    :type token: str
    """
    if token is None:
        token = keyring.get_password('pushbullet', USERNAME)

    assert token is not None, 'No API token is stored and none was given'

    msg = {'type': 'file', 'file_name': file_name,
           'file_type': file_type, 'file_url': file_url}
    resp = requests.post(PUSHBULLET_ENDPOINT, data=json.dumps(msg),
                         headers={'Access-Token': token,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Notifcation Error ', resp.status_code)
    else:
        print('Notification Sent')

@contextmanager
def push_alert(title='{hostname}', success_msg='Process complete!',
               fail_msg='{error}', closing_func=None):
    """contextmanager that will send a push message to all pushbullet linked
    devices when the contained processes are complete or when they error. Can
    also assign functions to be executed after everything else regardless of
    error.

    :param title: title of the push messages sent. {hostname} will insert the
        active computer's hostname. {username} will insert the current username.
    :param success_msg: notification text on success
    :param fail_msg: notification text on error, {error} will insert a short
        version of the error thrown
    :param closing_func: function to be executed on exit, regardless of error
    :type title: str
    :type success_msg: str
    :type fail_msg: str
    :type closing_func: function
    """
    fmt = {}
    if '{hostname}' in title:
        fmt['hostname'] = HOSTNAME

    if '{username}' in title:
        fmt['username'] = USERNAME

    title = title.format(**fmt)

    try:
        yield
        push_note(title, success_msg)
    except Exception as ex:
        if '{error}' in fail_msg:
            fail_msg = fail_msg.format(error=str(ex))

        push_note(title + ' Error!', fail_msg)
        raise ex
    finally:
        if closing_func is not None:
            closing_func()

def setup(token : str):
    """Adds pushbullet API token to the keyring and sends test message

    :param token: API token for pushbullet
    :type token: str
    """
    assert type(token) == str, 'token must be a str.'
    existsing = keyring.get_password('pushbullet', USERNAME)
    if existing is not None:
        q = input('Stored token already exists for pushbullet. '
                  'Would you like to replace it? (y/n) ')
    else:
        q = 'y'

    if q == y:
        keyring.set_password('pushbullet', USERNAME, token)
        print('New API token stored for pushbullet')
    else:
        print('Using existing token')

    push_note(HOSTNAME, 'Hello, World!')


def main():
    """
    usage:
        pbmsg config -t PUSHBULLET_API_TOKEN
        pbmsg push -m "Message to send"
        pbmsg push -t TOKEN -n MESSAGE_TITLE -m MESSAGE_BODY
        TODO:
        pgmsg push -l https://INSERT_WEBSITE.HERE
        pbmsg push -f /path/to/file
    """
    parser = argparse.ArgumentParser(prog='pbmsg',
                                     description='tool for sending push '
                                     'notifications via pushbullet')
    parser.add_argument('mode', help='Mode to run in. Can be "config" to '
                        'store credentials or "push" to send a message')
    parser.add_argument('-t', '--token', help='API token for pushbullet')
    parser.add_argument('-n', '--title', help='title of message to push', default=HOSTNAME)
    parser.add_argument('-m', '--body', help='message to send', default='')
    parser.add_argument('-l', '--link', help='link to send')
    parser.add_argument('-f', '--file', help='file to send')
    args = parser.parse_args()

    if args.mode == 'config':
        assert args.token is not None, ('Must provide [-t | --token] '
                                        'argument in order to configure')
        setup(args.token)
    elif args.mode == 'push':
        if args.body:
            push_note(args.title, args.body, token=args.token)

        if args.link:
            push_link(args.title, args.body, args.link, token=args.token)

        if args.file:
            file_name = os.path.basename(args.file).replace('%20', ' ')
            file_type = mimetypes.guess_type(file_name)
            push_file(file_name, file_type, args.file, body=args.body)
    else:
        parser.error('Must provide a valid usage mode. config | push')

if __name__ == '__main__':
    main()
