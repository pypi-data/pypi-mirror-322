import pytest
import asyncio 
import victronvenusclient

@pytest.mark.asyncio
async def test_connect(config_host,config_port,config_username,config_password,config_use_ssl):
    hub = victronvenusclient.Hub(config_host,config_port,config_username,config_password,config_use_ssl)
    await hub.connect()
    assert hub.connected == True
    await hub.disconnect()


    


@pytest.mark.asyncio
async def test_verify_connection(config_host,config_port,config_username,config_password,config_use_ssl):
        hub = victronvenusclient.Hub(config_host,config_port,config_username,config_password,config_use_ssl)
        serial = await hub.verify_connection_details()
        assert len(serial) > 0
