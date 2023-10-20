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

    @staticmethod
    def _handle_response(response) -> str:
        collected_messages = []
        print("\nResponse:\n")
        for chunk in response:
            try:
                chunk_message = chunk["choices"][0]["delta"]["content"]
                print(chunk_message, end="")
                collected_messages.append(chunk_message)
            except KeyError:
                pass
        print("\n")

        return "".join(collected_messages).strip()

    def communicate(self, message: str) -> str:
        self.message_history.append({"role": "user", "content": message})
        response = ChatCompletion.create(model="gpt-4", messages=self.message_history, stream=True)
        full_reply_content = self._handle_response(response)
        self.message_history.append({"role": "assistant", "content": full_reply_content})

        return full_reply_content
