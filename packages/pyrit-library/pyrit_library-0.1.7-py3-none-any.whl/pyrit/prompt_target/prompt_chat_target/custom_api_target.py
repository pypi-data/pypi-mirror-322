import logging
import json
import httpx  # or you can use `requests` if preferred
from pyrit.memory import MemoryInterface
from pyrit.models import PromptRequestResponse, PromptRequestPiece, construct_response_from_request
from pyrit.prompt_target import PromptChatTarget

logger = logging.getLogger(__name__)

class CustomAPITarget(PromptChatTarget):
    """This class facilitates interaction with a custom API"""

    # API_URL = ""

    def __init__(self, api_url: str, field_name: str, field_name2: str,field_value2: str, *, memory: MemoryInterface = None) -> None:
        """Class that initializes a custom API target"""
        PromptChatTarget.__init__(self, memory=memory)
        self.api_url = api_url
        self.field_name = field_name
        self.field_name2 = field_name2
        self.field_value2 = field_value2

    async def send_prompt_async(self, *, prompt_request: PromptRequestResponse) -> PromptRequestResponse:
        """Asynchronously sends a prompt request to the custom API and handles the response."""
        self._validate_request(prompt_request=prompt_request)
        request: PromptRequestPiece = prompt_request.request_pieces[0]

        logger.info(f"Sending the following prompt to the custom API: {request}")

        # Prepare the payload for the custom API
        payload = {
            self.field_name: prompt_request.request_pieces[0].original_value,
            self.field_name2: self.field_value2
        }
        
        try:
            # Send the request to the custom API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.api_url, json=payload)

            if response.status_code == 200:
                if "completion_result" in response.json():
                     prompt_request.request_pieces[0].converted_value = response.json()["completion_result"]

                # Construct the response entry
                response_entry = construct_response_from_request(request=request, response_text_pieces=[prompt_request.request_pieces[0].converted_value])
            else:
                logger.error(f"Failed to get a valid response from the custom API. Status code: {response.status_code}")
                response_entry = construct_response_from_request(
                    request=request, response_text_pieces=["Error: Failed to get a valid response"]
                )

        except httpx.ReadTimeout:
            logger.error("Request timed out while waiting for a response from the custom API.")
            response_entry = construct_response_from_request(
                request=request, response_text_pieces=["Error: Request timed out"]
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            response_entry = construct_response_from_request(
                request=request, response_text_pieces=[f"HTTP error occurred: {e.response.status_code} - {e.response.text}"]
            )
        except httpx.HTTPError as e:
            logger.error(f"An HTTP error occurred: {str(e)}")
            response_entry = construct_response_from_request(
                request=request, response_text_pieces=[f"An HTTP error occurred: {str(e)}"]
            )

        return response_entry

    def _validate_request(self, prompt_request: PromptRequestResponse) -> None:
        if len(prompt_request.request_pieces) != 1:
            raise ValueError("This target only supports a single prompt request piece.")
        if prompt_request.request_pieces[0].converted_value_data_type != "text":
            raise ValueError("This target only supports text prompt input.")