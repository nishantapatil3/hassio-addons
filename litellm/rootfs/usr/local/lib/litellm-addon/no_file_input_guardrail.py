from typing import Literal, Optional, Union

from litellm.caching.caching import DualCache
from litellm.integrations.custom_guardrail import CustomGuardrail
from litellm.proxy._types import UserAPIKeyAuth

BLOCKED_CONTENT_TYPES = ("file", "document")
IMAGE_CONTENT_TYPES = ("image_url", "image")
HAIKU_MODEL = "claude-haiku-4-5-20251001"


class NoFileInputGuardrail(CustomGuardrail):
    """Block document uploads and send image requests to the low-cost tier."""

    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: Literal[
            "completion",
            "text_completion",
            "embeddings",
            "image_generation",
            "moderation",
            "audio_transcription",
            "pass_through_endpoint",
            "rerank",
        ],
    ) -> Optional[Union[Exception, str, dict]]:
        has_image = False
        for message in data.get("messages", []):
            content = message.get("content", "")
            if not isinstance(content, list):
                continue

            for part in content:
                content_type = part.get("type", "")
                if content_type in BLOCKED_CONTENT_TYPES:
                    raise Exception(
                        "File and document inputs are not allowed. "
                        "Extract their text and send it as text instead."
                    )
                if content_type in IMAGE_CONTENT_TYPES:
                    has_image = True

        if has_image:
            data["model"] = HAIKU_MODEL

        return data
