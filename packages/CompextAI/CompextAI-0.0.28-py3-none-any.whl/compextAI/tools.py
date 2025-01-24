from typing import Callable
from typing import Any, Dict, get_origin, get_args
from pydantic import BaseModel
from typing import Type

ToolRegistry = {}

def get_input_schema_dict(input_schema:Type[BaseModel]) -> dict:
    input_schema_dict = input_schema.model_json_schema()
    return input_schema_dict

class ToolResult:
    result: str
    content: str

    def __init__(self, result:str, content:str):
        self.result = result
        self.content = content

    def get_result(self):
        return self.result

    def get_content(self):
        return self.content

class Tool:
    name:str
    description:str
    input_schema:dict
    func:Callable
    def __init__(self, name:str, description:str, input_schema:dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def __call__(self, *args, **kwargs) -> ToolResult:
        return self.func(self.tool_class(), *args, **kwargs)
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }
    def __str__(self):
        return f"Tool(name={self.name}, description={self.description}, input_schema={self.input_schema})"

def register_tool(cls):
    if not hasattr(cls, "name"):
        raise Exception(f"Tool {cls.__name__} does not have a name")
    if not hasattr(cls, "description"):
        raise Exception(f"Tool {cls.__name__} does not have a description")
    if not hasattr(cls, "input_schema"):
        raise Exception(f"Tool {cls.__name__} does not have an input schema")
    if not hasattr(cls, "_run"):
        raise Exception(f"Tool {cls.__name__} does not have a _run method")
    
    input_schema = get_input_schema_dict(cls.input_schema)
    tool_instance = Tool(name=cls.name, description=cls.description, input_schema=input_schema)
    tool_instance.func = cls._run
    tool_instance.tool_class = cls
    ToolRegistry[cls.name] = tool_instance

    return cls

def get_tool(name:str) -> Tool:
    if name not in ToolRegistry:
        raise Exception(f"Tool {name} not found, please register the tool first")
    return ToolRegistry[name]

def get_tool_names() -> list[str]:
    return ToolRegistry.keys()
