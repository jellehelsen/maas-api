from maas_api import __version__
from maas_api.client import Client, handler_command_name
from pytest import fixture, mark, raises
import json

description = None
with open("maas-api.json", "rb") as f:
    description = json.load(f)

actions = []
for resource in description["resources"]:
    if resource["auth"]:
        for action in resource["auth"]["actions"]:
            actions.append(
                dict(
                    handler_name=handler_command_name(resource["name"]),
                    params=resource["auth"]["params"],
                    uri=resource["auth"]["uri"],
                    method=action["method"],
                    name=action["name"],
                )
            )


@fixture
def api_description():
    with open("maas-api.json", "rb") as f:
        return json.load(f)


@fixture
def client(requests_mock, api_description):
    requests_mock.get(
        "http://192.0.2.1:5240/MAAS/api/2.0/describe/", json=api_description
    )
    return Client(
        url="http://192.0.2.1:5240/MAAS/",
        api_key="some:api:key",
    )


def test_version():
    assert __version__ == "0.1.0"


def test_client(client, requests_mock, api_description):
    assert client is not None
    assert client.description is not None
    assert client.machines is not None
    assert client.machines.read is not None
    assert client.machines.uri is not None
    assert client.machines.params is not None
    assert client.machines.name is not None


def test_allocate(client, requests_mock, api_description):
    requests_mock.post(
        "http://192.0.2.1:5240/MAAS/api/2.0/machines/?op=allocate",
        json={"system_id": "abcd"},
    )
    machine = client.machines.allocate()
    assert machine is not None
    assert machine["system_id"] == "abcd"


def test_deploy(client, requests_mock):
    requests_mock.post(
        "http://192.0.2.1:5240/MAAS/api/2.0/machines/abcd/?op=deploy",
        json={"system_id": "abcd"},
    )
    machine = client.machine.deploy(system_id="abcd")
    assert machine is not None
    assert machine["system_id"] == "abcd"
    assert requests_mock.called, "deploy url not called"


def test_error(client, requests_mock):
    requests_mock.post(
        "http://192.0.2.1:5240/MAAS/api/2.0/machines/abcd/?op=deploy",
        status_code=400,
        text="Some error",
    )
    with raises(Exception, match="Some error"):
        client.machine.deploy(system_id="abcd")


@mark.parametrize("action", actions)
def test_action(action, client, requests_mock):
    params = dict()
    if len(action["params"]) > 0:
        for param in action["params"]:
            params[param] = "testvalue"
    requests_mock.register_uri(
        action["method"], action["uri"].format(**params), json={}
    )

    handler = getattr(client, action["handler_name"])
    method = getattr(handler, action["name"])
    method(**params)

    assert (
        requests_mock.called
    ), f"{action['handler_name']}: {action['name']} not called"
