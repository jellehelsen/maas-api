from .fixtures import client


def test_listing(client):
    machines = client.machines.read()
    assert type(machines) == list
    assert len(machines) > 0
    assert "system_id" in machines[0]
    assert machines[0]["system_id"] is not None
    assert len(machines[0]["system_id"]) > 0


def test_allocation_and_release(client):
    machines = client.machines.read()
    machine = client.machines.allocate()
    assert machine is not None
    assert len(machine["system_id"]) > 0
    assert machine["status_name"] == "Allocated"
    new_machines = client.machines.read()
    assert len(new_machines) == len(machines) + 1
    allocated_machines = client.machines.list_allocated()
    assert len(allocated_machines) > 0
    client.machine.release(system_id=machine["system_id"])
    new_machines = client.machines.read()
    assert len(new_machines) == len(machines)


def test_deploying(client):
    machine = client.machines.allocate()
    new_machine = client.machine.deploy(system_id=machine["system_id"])
    assert new_machine["status_name"] == "Deploying"
    client.machine.release(system_id=machine["system_id"])
