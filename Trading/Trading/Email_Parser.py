from __future__ import print_function
import httplib2
import os
import pprint
import base64

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret_858943483448-lebr404rqt5uabkqlnb8jn5ijvgde607.apps.googleusercontent.com.json'  #'client_secret.json'
APPLICATION_NAME = 'Python_Email_Scraper'  #'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'python_email_scraper.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])

    try:
        query = 'in:trash to:w.arr7020@gmail.com label:Stock_Newsletter '
        response = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        for message in messages:
            email = service.users().messages().get(userId='me', id=message['id']).execute()
            parts = email['payload']['parts']
            for part in parts:
                body = part['body']
                #pprint.pprint(body['data'], width=1) 
                print(base64.b64decode(body['data']))

    except errors.HttpError, error:
        print("An error occurred: %s" % error)


if __name__ == '__main__':
    main()