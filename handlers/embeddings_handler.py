import abc
import json
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from botocore.response import StreamingBody

from llama_index.embeddings.sagemaker_endpoint.utils import BaseIOHandler


class BGEHandler(BaseIOHandler):
    content_type: str = "application/json"
    accept: str = "application/json"

    def serialize_input(self, request: List[str], model_kwargs: dict) -> bytes:
        request_str = json.dumps(
            {"text_inputs": request, "mode": "embedding", **model_kwargs})
        return request_str.encode("utf-8")

    def deserialize_output(self, response: "StreamingBody") -> List[List[float]]:
        response_json = json.loads(response.read().decode("utf-8"))
        return response_json["embedding"]