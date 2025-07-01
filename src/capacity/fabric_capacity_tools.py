from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.fabric.aio import FabricMgmtClient
from .fabric_capacity import FabricCapacity
from common import logger

async def list_fabric_capacities(subscription_id: str) -> dict:
    """
    Asynchronously lists all Fabric capacities within a specified Azure subscription.

    Args:
        subscription_id (str): The Azure subscription ID for which to list Fabric capacities.

    Returns:
        dict: A dictionary containing a list of Fabric capacities under the key 'capacities'.

    Raises:
        Exception: Propagates any exception encountered during the listing process.
    """
    logger.info(f"Listing Fabric capacities for subscription: {subscription_id}")
    credential = DefaultAzureCredential()
    client = FabricMgmtClient(credential, subscription_id)
    try:
        result = client.fabric_capacities.list_by_subscription()
        capacities = [FabricCapacity(item).to_dict() async for item in result]
        logger.info(f"Found {len(capacities)} capacities.")
        return {"capacities": capacities}
    except Exception as e:
        logger.error(f"Error listing capacities: {e}")
        raise
    finally:
        await credential.close()
        await client.close()

async def get_fabric_capacity(subscription_id: str, resource_group: str, capacity_name: str) -> dict:
    """
    Retrieves details of a specific Fabric capacity resource.

    Args:
        subscription_id (str): The Azure subscription ID.
        resource_group (str): The name of the resource group containing the Fabric capacity.
        capacity_name (str): The name of the Fabric capacity resource.

    Returns:
        dict: A dictionary containing the details of the specified Fabric capacity.

    Raises:
        Exception: If there is an error retrieving the Fabric capacity details.
    """
    logger.info(f"Getting Fabric capacity: {capacity_name} in resource group: {resource_group}, subscription: {subscription_id}")
    credential = DefaultAzureCredential()
    client = FabricMgmtClient(credential, subscription_id)
    try:
        capacity = await client.fabric_capacities.get(resource_group, capacity_name)
        logger.info(f"Retrieved capacity: {capacity_name}")
        return FabricCapacity(capacity).to_dict()
    except Exception as e:
        logger.error(f"Error getting capacity: {e}")
        raise
    finally:
        await credential.close()
        await client.close()

async def resume_fabric_capacity(subscription_id: str, resource_group: str, capacity_name: str) -> dict:
    """Resume a Fabric capacity.

    Args:
        subscription_id (str): Azure subscription ID.
        resource_group (str): Name of the resource group.
        capacity_name (str): Name of the Fabric capacity.

    Returns:
        dict: Status and message about the resume operation.

    Raises:
        Exception: If an error occurs during the resume operation.
    """
    logger.info(f"Resuming Fabric capacity: {capacity_name} in resource group: {resource_group}, subscription: {subscription_id}")
    credential = DefaultAzureCredential()
    client = FabricMgmtClient(credential, subscription_id)
    try:
        poller = await client.fabric_capacities.begin_resume(resource_group, capacity_name)
        logger.info(f"Resume operation started for: {capacity_name}")
        return {
            "status": "accepted",
            "message": "Resume operation started. Check Azure portal for progress.",
            "poller_status": poller.status()
        }
    except Exception as e:
        logger.error(f"Error resuming capacity: {e}")
        raise
    finally:
        await credential.close()
        await client.close()

async def pause_fabric_capacity(subscription_id: str, resource_group: str, capacity_name: str) -> dict:
    """
    Pause a Fabric capacity.

    Args:
        subscription_id (str): Azure subscription ID.
        resource_group (str): Name of the resource group.
        capacity_name (str): Name of the Fabric capacity.

    Returns:
        dict: Status and message about the pause operation.

    Raises:
        Exception: If an error occurs during the pause operation.
    """
    logger.info(f"Pausing Fabric capacity: {capacity_name} in resource group: {resource_group}, subscription: {subscription_id}")
    credential = DefaultAzureCredential()
    client = FabricMgmtClient(credential, subscription_id)
    try:
        poller = await client.fabric_capacities.begin_suspend(resource_group, capacity_name)
        logger.info(f"Pause operation started for: {capacity_name}")
        return {
            "status": "accepted",
            "message": "Pause operation started. Check Azure portal for progress.",
            "poller_status": poller.status()
        }
    except Exception as e:
        logger.error(f"Error pausing capacity: {e}")
        raise
    finally:
        await credential.close()
        await client.close()

fabric_capacity_tools = [
    list_fabric_capacities,
    get_fabric_capacity,
    resume_fabric_capacity,
    pause_fabric_capacity,
]

def register_tools(mcp):
    for tool in fabric_capacity_tools:
        mcp.tool(tool)
