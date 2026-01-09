import asyncio
import logging
from typing import Any
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import AgentCard, MessageSendParams, SendMessageRequest
from a2a.utils.constants import (
    AGENT_CARD_WELL_KNOWN_PATH,
    EXTENDED_AGENT_CARD_PATH,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ORCHESTRATOR_AGENT_URL = "http://localhost:10002"

async def main() -> None:

    base_url = ORCHESTRATOR_AGENT_URL
    
    # Increase the HTTP client timeout
    timeout = httpx.Timeout(60.0, connect=5.0)

    async with httpx.AsyncClient(timeout=timeout) as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        final_agent_card_to_use: AgentCard | None = None

        try:
            logger.info(f"Attempting to fetch public agent card from: {base_url}{AGENT_CARD_WELL_KNOWN_PATH}")
            _public_card = await resolver.get_agent_card()
            logger.info("Successfully fetched public agent card:")
            logger.info(_public_card.model_dump_json(indent=2, exclude_none=True))
            final_agent_card_to_use = _public_card
            logger.info("\nUsing PUBLIC agent card for client initialization (default).")

        except Exception as e:
            logger.error(f"Critical error fetching public agent card: {e}", exc_info=True)
            raise RuntimeError("Failed to fetch the public agent card. Cannot continue.") from e

        # --8<-- [start:send_message]
        client = A2AClient(httpx_client=httpx_client, agent_card=final_agent_card_to_use, url=base_url)
        logger.info("A2AClient initialized.")

        # Test routing to Jira
        send_message_payload: dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": 'Show me my jira tickets',
                    }
                ],
                "message_id": uuid4().hex,
            },
        }
        request = SendMessageRequest(id=str(uuid4()), params=MessageSendParams(**send_message_payload))

        try:
            print("\n--- Sending request to Orchestrator (Jira query) ---")
            response = await client.send_message(request)
            print(response.model_dump(mode="json", exclude_none=True))
        except httpx.ReadTimeout:
            logger.error("Request timed out. The agent took too long to respond.")


if __name__ == "__main__":
    asyncio.run(main())
