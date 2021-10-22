from pytest import fixture
from maas_api import Client


@fixture
def client():
    return Client(
        url="http://10.66.51.128:5240/MAAS/",
        api_key="nEnncD3wfvYpEeAwr7:rzQnvtLX359uawNtB6:VY7GhF2Ncth5dvuBLK3rS9davVVcAK5t",
    )
