from compextAI.api.api import APIClient
from compextAI.messages import Message
from compextAI.threads import ThreadExecutionResponse
from compextAI.tools import get_tool
import time
import queue
import json

class ThreadExecutionStatus:
    status: str

    def __init__(self, status:str):
        self.status = status

def get_thread_execution_status(client:APIClient, thread_execution_id:str) -> str:
    response = client.get(f"/threadexec/{thread_execution_id}/status")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to get thread execution status, status code: {status_code}, response: {data}")
    
    return ThreadExecutionStatus(data["status"])

def get_thread_execution_response(client:APIClient, thread_execution_id:str) -> dict:
    response = client.get(f"/threadexec/{thread_execution_id}/response")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to get thread execution response, status code: {status_code}, response: {data}")
    
    return data


class ExecuteMessagesResponse:
    thread_execution_id: str

    def __init__(self, thread_execution_id:str, thread_execution_param_id:str, messages:list[Message], system_prompt:str, append_assistant_response:bool, metadata:dict):
        self.thread_execution_id = thread_execution_id
        self.thread_execution_param_id = thread_execution_param_id
        self.messages = messages
        self.system_prompt = system_prompt
        self.append_assistant_response = append_assistant_response
        self.metadata = metadata

    def poll_thread_execution(self, client:APIClient) -> any:
        while True:
            try:
                thread_run_status = get_thread_execution_status(
                    client=client,
                    thread_execution_id=self.thread_execution_id
                ).status
            except Exception as e:
                print(e)
                raise Exception("failed to get thread execution status")
            if thread_run_status == "completed":
                break
            elif thread_run_status == "failed":
                raise Exception("Thread run failed")
            elif thread_run_status == "in_progress":
                print("thread run in progress")
                time.sleep(3)
            else:
                raise Exception(f"Unknown thread run status: {thread_run_status}")
        
        return get_thread_execution_response(
            client=client,
            thread_execution_id=self.thread_execution_id
        )
    
    def get_stop_reason(self, client:APIClient) -> str:
        response = self.poll_thread_execution(client)
        return response['response']['choices'][0]['finish_reason']

class Tool:
    name: str
    description: str
    input_schema: dict

    def __init__(self, name:str, description:str, input_schema:dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }

def execute_messages(client:APIClient, thread_execution_param_id:str, messages:list[Message],system_prompt:str="", append_assistant_response:bool=True, metadata:dict={}) -> ThreadExecutionResponse:
    thread_id = "compext_thread_null"
    response = client.post(f"/thread/{thread_id}/execute", data={
            "thread_execution_param_id": thread_execution_param_id,
            "append_assistant_response": append_assistant_response,
            "thread_execution_system_prompt": system_prompt,
            "messages": [message.to_dict() for message in messages],
            "metadata": metadata,
        })

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to execute thread, status code: {status_code}, response: {data}")
        
    return ExecuteMessagesResponse(data["identifier"], thread_execution_param_id, messages, system_prompt, append_assistant_response, metadata)

class ExecuteMessagesWithToolsResponse(ExecuteMessagesResponse):
    tools: list[Tool]
    messages: list[Message]
    human_in_the_loop: bool
    human_intervention_handler: callable
    def __init__(self, thread_execution_id:str, thread_execution_param_id:str, messages:list[Message], system_prompt:str, append_assistant_response:bool, metadata:dict, tools:list[str], human_in_the_loop:bool=False, human_intervention_handler:callable=None):
        super().__init__(thread_execution_id, thread_execution_param_id, messages, system_prompt, append_assistant_response, metadata)
        if human_in_the_loop:
            if human_intervention_handler is None:
                raise Exception("Human intervention handler is required when human_in_the_loop is True")
        self.tools = tools
        self.human_in_the_loop = human_in_the_loop
        self.human_intervention_handler = human_intervention_handler

    def poll_until_completion(self, client:APIClient, execution_queue:queue.Queue=None) -> any:
        while True:
            response = self.poll_thread_execution(client)
            if self.get_stop_reason(client) == "tool_calls":
                content_msg = response['response']['choices'][0]['message']['content']
                tool_calls = response['response']['choices'][0]['message']['tool_calls']
                self.messages.append(Message(
                    **response['response']['choices'][0]['message'],
                ))
                for tool_call in tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_input = tool_call['function']['arguments']
                    tool_use_id = tool_call['id']

                    if tool_name == "json_tool_call":
                        self.messages.append(Message(
                            role="tool" ,
                            content=tool_call['function']['arguments'],
                            tool_call_id=tool_use_id
                        ))  
                        continue
                        
                    if execution_queue:
                        execution_queue.put({
                            "type": "tool_use",
                            "content": {
                                "tool_name": tool_name,
                                "tool_input": tool_input,
                                "tool_use_id": tool_use_id
                            }
                        })
                    tool_input_dict = json.loads(tool_input)
                    print("tool return", tool_call)
                    print("tool input", tool_input_dict)
                    print("tool input type", type(tool_input_dict))
                    try:
                        if tool_name == "human_in_the_loop":
                            tool_result = self.human_intervention_handler(**tool_input_dict)
                        else:
                            tool_result = get_tool(tool_name)(**tool_input_dict)
                    except Exception as e:
                        print(f"Error executing tool {tool_name}: {e}")
                        raise Exception(f"Error executing tool {tool_name}: {e}")
        
                    # handle tool result
                    print(f"Tool {tool_name} returned: {tool_result.get_content()}")
                    if execution_queue:
                        execution_queue.put({
                            "type": "tool_result",
                            "content": {
                                "tool_use_id": tool_use_id,
                                "result": tool_result.get_content()
                            }
                        })
                    print("response assistant appending", response['response']['choices'][0]['message'])
                    self.messages.append(Message(
                        role="tool" ,
                        content=tool_result.get_result(),
                        tool_call_id=tool_use_id
                    ))
                # start a new execution with the new messages
                new_execution = execute_messages_with_tools(
                    client=client,
                    thread_execution_param_id=self.thread_execution_param_id,
                    messages=self.messages,
                    system_prompt=self.system_prompt,
                    append_assistant_response=self.append_assistant_response,
                    metadata=self.metadata,
                    tool_list=self.tools
                )
                self.thread_execution_id = new_execution.thread_execution_id
            else:
                break

        return response


def execute_messages_with_tools(client:APIClient, thread_execution_param_id:str, messages:list[Message],system_prompt:str="", append_assistant_response:bool=True, metadata:dict={}, tool_list:list[str]=[], human_in_the_loop:bool=False, human_intervention_handler:callable=None) -> ExecuteMessagesWithToolsResponse:
    if human_in_the_loop:
        tool_list.append("human_in_the_loop")
    thread_id = "compext_thread_null"
    response = client.post(f"/thread/{thread_id}/execute", data={
            "thread_execution_param_id": thread_execution_param_id,
            "append_assistant_response": append_assistant_response,
            "thread_execution_system_prompt": system_prompt,
            "messages": [message.to_dict() for message in messages],
            "metadata": metadata,
            "tools": [get_tool(tool).to_dict() for tool in tool_list]
        })
    
    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to execute thread, status code: {status_code}, response: {data}")
    
    return ExecuteMessagesWithToolsResponse(data["identifier"], thread_execution_param_id, messages, system_prompt, append_assistant_response, metadata, tool_list, human_in_the_loop, human_intervention_handler)
