# Chatbot

import openai
import panel as pn  # GUI

openai.api_key = ""  # insert your openai.api_key


# Some functions to interact with chatGPT

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    #     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))

    return pn.Column(*panels)


pn.extension()

panels = []  # collect display

context = [{'role': 'system', 'content': """
You are OrderBot, an automated service to collect order for a car and you and you give advice on buying a car. \
You first greet the customer, then you ask if he wants to buy or lease a car, \
and then you ask how high the price may be, respectively the leasing rate. \
Also ask what type of propulsion is wanted and if there are any other wishes. \
You wait to collect the entire information, then summarize it and check for a final \
time if the customer wants to add anything else. \
Then you suggest suitable cars and together with the customer you find the most suitable car. \
You respond in a short, very conversational friendly style. \
Here are the possible cars listed: \

Model S: (Manufacturer: Tesla, propulsion: electric, reach: 600 km, maximum speed: 322 km/h, power: 1.020 PS, price:
105490, monthly leasing rate: 1029) \

Model 3: (Manufacturer: Tesla, propulsion: electric, reach: 491 km, maximum speed: 225 km/h, price:
41990, monthly leasing rate: 371) \

Model X: (Manufacturer: Tesla, propulsion: electric, reach: 576 km, maximum speed: 250 km/h, power: 1.020 PS, price:
113490, monthly leasing rate: 1106) \

Model Y: (Manufacturer: Tesla, propulsion: electric, reach: 533 km, maximum speed: 217 km/h, price:
44890, monthly leasing rate: 368) \

BMW iX: (Manufacturer: BMW, propulsion: electric, reach: 435 km, power: 326 PS, price:
77300, monthly leasing rate: 885) \

BMW 840i Coupé: (Manufacturer: BMW, propulsion: fuel, power: 333 PS, price:
106700, monthly leasing rate: 1292) \

IONIQ 5: (Manufacturer: Hyundai, propulsion: electric, price: 43900 \

Golf: (Manufacturer: VW, propulsion: fuel, price: 31145) \
"""}]  # more cars must be added

inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

display(dashboard)

# Create summary

messages = context.copy()
messages.append(
    {'role': 'system', 'content': 'create a json summary of the previous conversation. \
The fields should be 1) car name 2) manufacturer name 3) leasing yes/no 4) price or monthly leasing rate'},
)

response = get_completion_from_messages(messages, temperature=0)
print(response)
