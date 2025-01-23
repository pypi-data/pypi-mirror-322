from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema

from typing import Optional

@dataclass
class PromptResponse:
    """ author semantha, this is a generated class do not change manually! """
    response: Optional[str] = None

PromptResponseSchema = class_schema(PromptResponse, base_schema=RestSchema)
