import msal
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.graph_client import GraphClient


class ConnectionSettings:
    context = None
    sharepoint_url = None

    def __init__(self, settings: dict):
        """
Sets up an Office 365 connection context for use with Office365-REST-Python-Client.
Unless settings['ConnectionType'] == 'SharePoint', GraphClient is returned.
Future versions will store 'settings' using encryption
        :param settings: dict - 'ClientId', 'ClientSecret', 'ConnectionType', 'Domain', 'SharePointUrl'
        :return: Connection object (either office365.sharepoint.client_context.ClientContext,
         or office365.graph_client.GraphClient)
        """
        self.user = settings.get('User')
        self.password = settings.get('Password')
        self.client_id = settings.get('ClientId')
        self.client_secret = settings.get('ClientSecret')
        self.auth_type = settings.get('ConnectionType')
        if not self.auth_type:
            self.auth_type = 'Secret'
        if self.auth_type == 'SharePoint':
            self.sharepoint_url = settings.get('SharePointUrl')
            self._sp_sign_in()
        else:
            self.domain = settings.get('Domain')
            self._graph_sign_in()
        self.context.execute_query()

    def _sp_sign_in(self):
        ctx_auth = AuthenticationContext(self.sharepoint_url)
        if ctx_auth.acquire_token_for_app(self.client_id, self.client_secret):
            self.context = ClientContext(self.sharepoint_url, ctx_auth)
            # print('mso_base.sign_in', ctx.authentication_context.__dict__)
        else:
            print(ctx_auth.get_last_error())

    def _graph_sign_in(self):
        def acquire_token_by_client_credentials():
            app = msal.ConfidentialClientApplication(
                authority=f'https://login.microsoftonline.com/{self.domain}.onmicrosoft.com',
                client_id=self.client_id,
                client_credential=self.client_secret
            )
            token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
            return token

        self.context = GraphClient(acquire_token_by_client_credentials)

