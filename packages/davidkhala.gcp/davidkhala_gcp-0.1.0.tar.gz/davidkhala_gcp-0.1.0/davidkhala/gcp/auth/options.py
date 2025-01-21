from typing import TypeVar, Generic

import google.auth
from google.auth.credentials import CredentialsWithQuotaProject
from google.oauth2 import service_account, credentials

from davidkhala.gcp.auth import OptionsInterface, ServiceAccountInfo

GenericCredentials = TypeVar('GenericCredentials', bound=CredentialsWithQuotaProject)


class AuthOptions(OptionsInterface, Generic[GenericCredentials]):
    credentials: GenericCredentials
    """
    :type credentials: service_account.Credentials | credentials.Credentials
    being as google.oauth2.credentials.Credentials when get from Application Default Credentials (ADC)
    raw secret not cached in credentials object. You need cache it by yourself.  
    """

    @staticmethod
    def default():
        c = AuthOptions[credentials.Credentials]()
        c.credentials, c.projectId = google.auth.default()
        return c

    @staticmethod
    def from_service_account(info: ServiceAccountInfo = None, *, client_email, private_key, project_id=None):
        if not info:
            info = {
                'client_email': client_email,
                'private_key': private_key,
            }
        if project_id:
            info['project_id'] = project_id

        if not info.get('project_id'):
            info['project_id'] = info.get('client_email').split('@')[1].split('.')[0]

        info['token_uri'] = "https://oauth2.googleapis.com/token"

        c = AuthOptions[service_account.Credentials]()

        c.credentials = service_account.Credentials.from_service_account_info(info)
        c.projectId = info['project_id']
        return c

    @staticmethod
    def from_api_key(api_key: str, client_options=None) -> dict:
        if client_options is None:
            client_options = {}
        client_options["api_key"] = api_key
        return client_options
