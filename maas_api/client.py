from requests import request
import re
from requests_oauthlib import OAuth1Session

re_camelcase = re.compile(r"([A-Z]*[a-z0-9]+|[A-Z]+)(?:(?=[^a-z0-9])|\Z)")


def handler_command_name(string):
    """Create a handler command name from an arbitrary string.
    Camel-case parts of string will be extracted, converted to lowercase,
    joined with hyphens, and the rest discarded. The term "handler" will also
    be removed if discovered amongst the aforementioned parts.
    """
    parts = re_camelcase.findall(string)
    parts = (part.lower() for part in parts)
    parts = (part for part in parts if part != "handler")
    return "-".join(parts)


class Action:
    def __init__(self, handler, name, method, op, doc, restful):
        self.handler = handler
        self.name = name
        self.method = method
        self.op = op
        self.doc = doc
        self.restful = restful

    def __call__(self, **kwargs):
        url = self.handler.uri.format(**kwargs)
        for p in self.handler.params:
            del kwargs[p]
        params = None
        if self.op is not None:
            params = {"op": self.op}
        response = self.handler.session.request(
            self.method, url, params=params, **kwargs
        )
        if response.ok:
            return response.json()
        raise Exception(response.text)


class Handler:
    def __init__(self, name, session, definition):
        self.name = name
        self.session = session
        self.uri = definition["uri"]
        self.params = definition["params"]
        # self.actions = [Action(**action) for action in actions]
        for action in definition["actions"]:
            setattr(self, action["name"], Action(handler=self, **action))


class Client(object):
    """The MAAS client."""

    def __init__(self, url: str, api_key: str):
        """
        The constructor for the MAAS client.

        Parameters:
        url (string): base url for the MAAS server
        api_key (string): api key for the MAAS server
        """
        super(Client, self).__init__()
        consumer_key, key, secret = api_key.split(":")
        self.base_url = url
        self.session = OAuth1Session(
            consumer_key, resource_owner_key=key, resource_owner_secret=secret
        )
        self.load_resources()

    def load_resources(self):
        response = self.session.get(f"{self.base_url}api/2.0/describe/")
        self.description = response.json()
        for resource in self.description["resources"]:
            if resource["auth"]:
                name = handler_command_name(resource["name"])
                handler = Handler(name, self.session, resource["auth"])
                setattr(self, name, handler)
