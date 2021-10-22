
# Table of Contents

1.  [Quickstart](#orgc1e985f)
    1.  [Installing](#org8a0e592)
    2.  [Using](#org155b2b6)
2.  [Why?](#org5d3a245)
3.  [How?](#orgfb84d69)



<a id="orgc1e985f"></a>

# Quickstart


<a id="org8a0e592"></a>

## Installing

You can install using pip.

    pip install maas-api


<a id="org155b2b6"></a>

## Using

You can use the api client the same way you would use the CLI.

    from maas_api import Client
    
    client = Client("http://192.0.2.10:/MAAS", api_key="your:api:key")
    
    # allocate a machine
    machine = client.machines.allocate()
    # start deploy
    client.machine.deploy(system_id=machine["system_id"])
    # release the machine
    client.machine.release(system_id=machine["system_id"])


<a id="org5d3a245"></a>

# Why?

The official MAAS api client library [python-libmaas](https://pypi.org/project/python-libmaas/) did not receive any new
functionality that is available with MAAS.
There is however a [CLI](https://github.com/maas/maas/tree/master/src) written in python. This allows all the functionality to
be used.


<a id="orgfb84d69"></a>

# How?

By using the same technique as the official CLI. By using the API description
available at [/MAAS/api/2.0/describe](file:///MAAS/api/2.0/describe). This allows us to expose the full API
exposed by the MAAS server and to keep functional parity with the CLI.

