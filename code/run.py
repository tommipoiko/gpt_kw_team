from agent import GPTAgent


AGENTS = {
    "Normal GPT": GPTAgent("Normal GPT")
}

EXIT_COMMANDS = ["q", "quit", "e", "exit", "s", "stop"]


def main():
    prompt = input("Prompt:\n\n")
    while prompt.lower() not in EXIT_COMMANDS:
        response = AGENTS["Normal GPT"].communicate(prompt)
        prompt = input("Prompt:\n\n")


if __name__ == "__main__":
    main()
