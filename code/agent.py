import json

from openai import ChatCompletion
import openai
import secret_variables as sv

openai.api_key = sv.API_KEY


class GPTAgent:
    def __init__(self, role: str, description: str | None = None):
        self.role = role
        if description:
            self.message_history = [{"role": "system", "content": description}]
        else:
            self.message_history = []
        self.functions = [
            {
                "name": "open_file",
                "description": "Open a file and write the content to it.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file to open."
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file."
                        }
                    },
                    "required": ["file_name", "content"]
                }
            }
        ]

    def _handle_response_chunks(self, response) -> str:
        # Remember to set stream=True to use this function.
        collected_messages = []
        print(f"\nResponse from {self.role}:\n")
        for chunk in response:
            try:
                chunk_message = chunk["choices"][0]["delta"]["content"]
                print(chunk_message, end="")
                collected_messages.append(chunk_message)
            except KeyError:
                pass
        print("\n")
        return "".join(collected_messages).strip()

    def _handle_response(self, response) -> str:
        response_message = response["choices"][0]["message"]
        print(f"\nResponse from {self.role}:\n")
        print(response_message["content"].strip())
        print("\n")
        return response_message["content"].strip()

    def _handle_function_calls(self, response) -> None | dict:
        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            available_functions = {
                "open_file": self.open_file
            }
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(
                file_name=function_args["file_name"],
                content=function_args["content"]
            )
            return {"role": "function", "name": function_name, "content": function_response}
        else:
            return None

    def _handle_response_and_function_calls(self, response) -> dict:
        response_message = response["choices"][0]["message"]

        # TODO Check what the response looks like when the agent calls a function and then sends a
        #  message.
        print(response["choices"])

        if response_message.get("function_call"):
            available_functions = {
                "open_file": self.open_file
            }
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(
                file_name=function_args["file_name"],
                content=function_args["content"]
            )
            return {"role": "function", "name": function_name, "content": f"function_response"}
        else:
            print(f"\nResponse from {self.role}:\n")
            print(response_message["content"].strip() + "\n")
            return {"role": "assistant", "content": response_message["content"].strip()}

    def communicate(self, message: str) -> str:
        self.message_history.append({"role": "user", "content": message})
        response = ChatCompletion.create(model="gpt-4", messages=self.message_history,
                                         functions=self.functions, function_call="auto")
        full_reply_content = self._handle_response_and_function_calls(response)
        self.message_history.append(full_reply_content)
        if full_reply_content["role"] == "function":
            return "Function called"
        else:
            return full_reply_content["content"]

    @staticmethod
    def open_file(file_name: str, content: str) -> bool:
        """Open a file and write the content to it."""
        try:
            with open(f"agent_files/{file_name}", "w+") as f:
                f.write(content)
                return True
        except Exception as e:
            print(e)
            return False
