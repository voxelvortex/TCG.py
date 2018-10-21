import requests
import json


class Handler(object):

    bearer = ""
    login_data = dict()

    def __init__(self, **kwargs):
        if "bearer" in kwargs:
            self.bearer = kwargs["bearer"]
        elif "public" in kwargs and "private" in kwargs:
            self._get_login_data(kwargs["public"], kwargs["private"])

            if "error" in self.login_data:
                # replace with custom exception later? :thinking:
                raise ValueError(self.login_data["error"]
                                 + ", description: "
                                 + self.login_data["error_description"])
            else:
                self.bearer = self.login_data["access_token"]
        else:
            raise ValueError("Test requirers a bearer or both public"
                             " and private arguments. You provided: "
                             + ", ".join(kwargs.keys()))

    def __get_login_data(self, public, private):
        token_url = "https://api.tcgplayer.com/token"
        data = "grant_type=client_credentials&client_id={0}&client_secret={1}"
        data = data.format(public, private)
        response = requests.request("POST", token_url, data=data)
        self.login_data = json.loads(response.text)
