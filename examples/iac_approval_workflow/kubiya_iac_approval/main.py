import asyncio
import logging
import argparse

from kubiya_iac_approval.workflows.resource_request import handle_resource_request

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def async_main(user_input: str, purpose: str, ttl: str):
    try:
        final_state = await handle_resource_request(user_input, purpose, ttl)
        logger.info(f"Final state: {final_state}")
    except Exception as e:
        logger.error(f"Error in workflow execution: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Handle infrastructure resource requests")
    parser.add_argument("user_input", help="User's resource request")
    parser.add_argument("--purpose", required=True, help="Purpose of the resource request")
    parser.add_argument("--ttl", required=True, help="Time-to-live for the requested resources")

    args = parser.parse_args()

    asyncio.run(async_main(args.user_input, args.purpose, args.ttl))


if __name__ == "__main__":
    main()
