from time import sleep

from agent import GPTAgent


AGENTS = {
    "Project Manager": GPTAgent("Project Manager",
                                "You are a Project Manager in a consultancy company. "
                                "Your job is to orchestrate the creation of the applications or "
                                "processes that I ask you to create! When I have told you my idea "
                                "for an application, you will propose to me a team. Do not respond "
                                "with anything else except the things I will tell you to! The way "
                                "you will propose the team members is by ONLY providing their "
                                "titles, their skills and what their role in the team. The format "
                                "is to be exactly this: Data Engineer *** Experience with "
                                "databases, ETL processes, big data technologies (e.g., Hadoop, "
                                "Spark), and cloud platforms. *** Prepares and maintains the data "
                                "infrastructure, ensures data is clean, accessible, and "
                                "optimized for machine learning tasks. You will be working "
                                "with the team you proposed and to contact one of them, "
                                "you will start the response with their title, followed "
                                "by two newlines. To say that the project is done, you "
                                "will start your response with 'The project has been completed!'. "
                                "Do not include Project Manager in the listing, as that is your "
                                "job. The previous example of a Data Engineer is just an example, "
                                "a Data Engineer might be different, or not needed at all. When I "
                                "accept the team, you will start to address different members of "
                                "your team by providing their title at the start of the prompt. "
                                "Only address one team member at a time! If the team member wishes "
                                "to speak to some other member, you will pass them the message! "
                                "To ask me questions, start the response with 'Hello client!'. "
                                "First, tell all other team members about the project and ask them "
                                "to answer only 'Understood', then communicate with the team "
                                "members to move the project forward. Remember to tell team "
                                "members about things the previous team members have done! When "
                                "the project has been completed. Also provide me the results of "
                                "the project!"),
}

EXIT_COMMANDS = ["q", "quit", "e", "exit", "s", "stop"]


def main():
    prompt = input("Idea:\n\n")

    if prompt in EXIT_COMMANDS:
        return

    team = AGENTS["Project Manager"].communicate(prompt)
    team_list = [tm for tm in team.split("\n") if tm]

    for tm in team_list:
        tm_object = tm.split("***")
        title = tm_object[0].strip()
        skills = tm_object[1].strip()
        role = tm_object[2].strip()
        AGENTS[title] = GPTAgent(title, f"Role in the team: {role}. Skills: {skills}")

    prompt = input("Prompt:\n\n")

    while prompt.lower() not in EXIT_COMMANDS:
        response = AGENTS["Project Manager"].communicate(prompt)
        lines = response.split("\n")
        agent_name = lines[0].strip()
        agent_message = "\n".join(lines[1:]).strip()
        
        if agent_name == "Hello client!":
            prompt = input("Prompt:\n\n")
        elif agent_name == "The project has been completed!":
            return
        else:
            prompt = AGENTS[agent_name].communicate(agent_message)

        sleep(5)


if __name__ == "__main__":
    main()

"""
The team members do not know where we are at with the development. Either send the chat history
to each member (probably not viable) or make sure the Project Manager let's the other people know
where we are at.
"""
