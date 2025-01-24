from compextAI.api.api import APIClient
from datetime import datetime

class Message:
    message_id: str
    thread_id: str
    content: any
    role: str
    metadata: dict
    created_at: datetime
    updated_at: datetime
    tool_call_id: str
    tool_calls: any
    function_call: any

    def __init__(self,content:any, role:str, message_id:str='', thread_id:str='', metadata:dict={}, created_at:datetime=None, updated_at:datetime=None, **kwargs):
        self.tool_call_id = None
        self.tool_calls = None
        self.function_call = None
        self.message_id = message_id
        self.thread_id = thread_id
        self.content = content
        self.role = role
        self.metadata = metadata
        self.created_at = created_at
        self.updated_at = updated_at
        if "tool_call_id" in kwargs:
            self.tool_call_id = kwargs["tool_call_id"]
        if "tool_calls" in kwargs:
            self.tool_calls = kwargs["tool_calls"]
        if "function_call" in kwargs:
            self.function_call = kwargs["function_call"]

    def __str__(self):
        return f"Message(message_id={self.message_id}, thread_id={self.thread_id}, content={self.content}, role={self.role}, metadata={self.metadata}, tool_call_id={self.tool_call_id}, tool_calls={self.tool_calls}, function_call={self.function_call})"
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "role": self.role,
            "metadata": self.metadata,
            "message_id": self.message_id,
            "thread_id": self.thread_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tool_call_id": self.tool_call_id if self.tool_call_id else None,
            "tool_calls": self.tool_calls if self.tool_calls else None,
            "function_call": self.function_call if self.function_call else None
        }

def get_message_object_from_dict(data:dict) -> Message:
    return Message(
        content=data["content"],
        role=data["role"],
        message_id=data["identifier"],
        thread_id=data["thread_id"],
        metadata=data["metadata"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        tool_call_id=data["tool_call_id"] if "tool_call_id" in data else None,
        tool_calls=data["tool_calls"] if "tool_calls" in data else None,
        function_call=data["function_call"] if "function_call" in data else None
    )

def list_all(client:APIClient, thread_id:str) -> list[Message]:
    response = client.get(f"/message/thread/{thread_id}")

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to list messages, status code: {status_code}, response: {data}")
    
    return [get_message_object_from_dict(message) for message in data]

def retrieve(client:APIClient, message_id:str) -> Message:
    response = client.get(f"/message/{message_id}")

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to retrieve message, status code: {status_code}, response: {data}")
    
    return get_message_object_from_dict(data)

def create(client:APIClient, thread_id:str, messages:list[Message]) -> list[Message]:
    response = client.post(f"/message/thread/{thread_id}", data={"messages": [message.to_dict() for message in messages]})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to create message, status code: {status_code}, response: {data}")
    
    return [get_message_object_from_dict(message) for message in data]

def update(client:APIClient, message_id:str, content:any, role:str, metadata:dict={}) -> Message:
    response = client.put(f"/message/{message_id}", data={"content": content, "role": role, "metadata": metadata})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to update message, status code: {status_code}, response: {data}")
    
    return get_message_object_from_dict(data)

def delete(client:APIClient, message_id:str) -> bool:
    response = client.delete(f"/message/{message_id}")
    return response["status"] == 204
