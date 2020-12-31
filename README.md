# PushBullet Messaging and Alerting tools
To use this you should get the pushbullet app on your phone.
On your computer, first go to the [pushbullet](https://www.pushbullet.com/)
website, and create an account. Then go to *Settings*  and click *Create Access
Token*. Copy this token as you will need it for configuring pushbullet_tools.  

## Installation
```bash
pip install pushbullet_tools
pbmsg config YOUR_PUSHBULLET_API_TOKEN
```
This will store your API token using your user's local python keyring.

## Command-line Usage
```bash
pbmsg push -m 'push a simple message'
pbmsg push --title 'message title' -m 'message body'
pbmsg push --link <URL> --title 'Link Title' --body 'additional message to include'
pbmsg push --file <FILE_URL>
```

## Context Manager
The `pushbullet_tools.push_alert` context manager you can execute a process and
receive a push notification on process completion or on error.
```python
import pushbullet_tools as pbt

with pbt.push_alert():
    /** insert long running process here **/

with pbt.push_alert(title='With love from {username}',
                    success_msg='This Turkey is cooked!',
                    fail_msg='There was a problem see: {error}',
                    closing_func=cleanup_func):
    /** do lots of stuff **/
```

The messages can be customized and a `closing_func` can be assign to run after
process regardless of whether an error is thrown.


## Sending messages in python
```python
from pushbullet_tools import push_message as pm

pm.push_note(pm.HOSTNAME, pm.USERNAME + ' says hi')
pm.push_link('link title', 'some message context', 'link URL')
pm.push_file('some_file.py', 'text/python', 'https://file.download.url')
```

