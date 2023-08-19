import openai
import re
import csv

openai.api_key = "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"

user_name = None
user_adr = None
user_email = None
user_phone = None
user_edu = None
user_dob = None


conversation = [
    {"role": "system", "content": "You are in a chat with the user, Agent 1, Agent 2 and Agent 3 . Agent 1 is responsible for convincing the user to share their information, Agent 2 is reponsible for extraction information from the user messages and Agent 3 is responsible for only tagging the extracting input with appropriate labels."},
    {"role": "user", "content": "User: Hi, I need help with this issue."},
    {"role": "assistant", "content": "Hi there! I am Agent 1 and I'm responsible for convincing the user to share their name, email address, phone number, address, education and date of birth while being SUBLIME and SMOOTH"}
, {"role": "assistant", "content": "Hi there! I am Agent 2 and I'm responsible for extracting information about  Name, Email, Phone number, Address, DOB and Education from user messages."},
    {"role": "assistant", "content": "Hi there! I am Agent 3 and I'm responsible for ONLY printing out tags of Name, Email, Phone number, Address, DOB and Education in the format [Name:info1][Email:info2][Phone_Number:info3][Address:info4][DOB:info5][Education:info6]."}
]

while True:
    user_input = input("You: ")
    conversation.append({"role": "user", "content": f"User: {user_input}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    user_response = response.choices[0].message['content']
    conversation.append({"role": "assistant", "content": f"Agent 1: {user_response}"})
    print("Bot :", user_response)

    agent_2_input = f"User: {user_input}"
    conversation.append({"role": "user", "content": f"{agent_2_input}"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= conversation
    )

    agent_2_response = response.choices[0].message['content']

    conversation.append({"role": "assistant", "content": f"Agent 2: {agent_2_response}"})
    agent_3_input = f"Agent 2:{agent_2_response}"
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        messages= conversation
    )
    agent_3_response = response.choices[0].message['content']
    conversation.append({"role": "assistant", "content": f"Agent 3: {agent_3_response}"})

    print(agent_3_response)

    pattern = r'\[([^:\]]+):([^:\]]+)\]'

    matches = re.findall(pattern, agent_3_response)

    tag_data_dict = dict(matches)

    print(tag_data_dict)

    for key,query in tag_data_dict.items():
        if key == 'Name':
            user_name = query
        elif key == 'DOB':
            user_dob = query
        elif key == 'Email':
            user_email = query
        elif key == 'Education':
            user_edu = query
        elif key == 'Address':
            user_adr = query
        else:
            user_phone = query


    if user_name and user_phone and user_adr and user_edu and user_email and user_dob:
        csv_data = [{"Name": user_name, "DateOfBirth": user_dob,"Address":user_adr,"Email":user_email,"Phone":user_phone, "Education":user_edu}]
        csv_file = "user_information.csv"

        with open(csv_file, "w", newline="") as csvfile:
            field_names = ["Name", "DateOfBirth","Address","Email","Phone","Education"]
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(csv_data)

        print("User information saved to", csv_file)
        break