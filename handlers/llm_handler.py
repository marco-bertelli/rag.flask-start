from llama_index.llms.sagemaker_endpoint.utils import BaseIOHandler
from llama_index.core.llms import ChatMessage, MessageRole

from typing import Optional, Sequence, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from botocore.response import StreamingBody


class MistralIOHandler(BaseIOHandler):
    content_type: str = "application/json"
    accept: str = "application/json"

    def serialize_input(self, request: str, model_kwargs: dict) -> bytes:
        params = model_kwargs.copy()

        params["return_full_text"] = False

        if "max_new_tokens" not in params:
            params["max_new_tokens"] = 1024

        if "temperature" not in params:
            params["temperature"] = 0.3

        if "stop" not in params:
            params["stop"] = ["</s>"]

        request_body = {
            "inputs": request,
            "parameters": params,
        }

        return json.dumps(request_body).encode("utf-8")

    def deserialize_output(self, response: "StreamingBody") -> str:
        response_bytes = response.read()
        response_str = response_bytes.decode("utf-8")

        try:
            data = json.loads(response_str)
            generated_text = data.get("generated_text", "")

            return generated_text
        except json.JSONDecodeError:
            print(f"Error parsing JSON from response: {response_str}")
            return ""

    def deserialize_streaming_output(self, response: bytes) -> str:
        chunk_str = response.decode("utf-8")

        return chunk_str

    def remove_prefix(self, response: str, prompt: str) -> str:
        if response.startswith(prompt):
            return response[len(prompt):]
        return response


def messages_to_prompt_mistral(
    messages: Sequence[ChatMessage], system_prompt: Optional[str] = None
) -> str:
    """
    <s>[INST] System Instruction + User Message [/INST] Model Answer</s>[INST] User [/INST]
    """
    sys_content = ""

    if messages and messages[0].role == MessageRole.SYSTEM:
        sys_content = messages[0].content
        messages = messages[1:]

    if not sys_content and system_prompt:
        sys_content = system_prompt

    prompt = "<s>"

    for i, message in enumerate(messages):
        role = message.role
        content = message.content

        if role == MessageRole.USER:
            prompt += "[INST] "

            if i == 0 and sys_content is not None:
                prompt += f"{sys_content}\n\n"
                sys_content = None

            prompt += f"{content} [/INST]"

        elif role == MessageRole.ASSISTANT:
            prompt += f" {content}</s>"

    return prompt
