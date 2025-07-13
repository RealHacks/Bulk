import os
import google.auth.transport.requests
import google_auth_oauthlib.flow
import google.oauth2.credentials
from flask import session, redirect, url_for

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authorize_user(callback=False):
    if callback:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'credentials.json', scopes=SCOPES)
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        return redirect('/')
    else:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'credentials.json', scopes=SCOPES)
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return redirect(authorization_url)

def get_gmail_service(creds_dict):
    creds = google.oauth2.credentials.Credentials(**creds_dict)
    from googleapiclient.discovery import build
    return build('gmail', 'v1', credentials=creds)