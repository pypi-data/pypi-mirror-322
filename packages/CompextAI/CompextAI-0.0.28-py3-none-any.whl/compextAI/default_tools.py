from pydantic import BaseModel, Field
from typing import Type

class HumanInTheLoopInputSchema(BaseModel):
    message: str = Field(description="The message to ask the human for input")

class HumanInTheLoop:
    name = "human_in_the_loop"
    description = "Use this tool to ask the human for input"
    input_schema: Type[BaseModel] = HumanInTheLoopInputSchema

    def _run(self, input:dict):
        pass
