from uuid import uuid4
from nicegui import ui
import requests
import json
from collections import Counter

ui.add_head_html('''
<style>
    body {
        margin: 0;
        line-height: inherit;
        background-color: #faf9ef; /* Set the desired background color */
    }
</style>
''')

ui.query('body').style('background-color: #faf9ef;')
ui.query('.nicegui-content').style('background-color: #faf9ef;')


messages = []

@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(avatar=avatar, text=text, sent=user_id==own_id)

@ui.page('/')
def index():
    def send():
        messages.append((user, avatar, text.value))
        chat_messages.refresh()
        text.value = ''

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    # avatar = f'leaf.jpg'
    with ui.column().classes('w-full items-stretch items-center bg-[#faf9ef]'):
        with ui.row().classes('flex-grow items-stretch items-center bg-[#faf9ef]'):
            ui.highchart({
            'title': False,
            'chart': {'type': 'bar', 'backgroundColor': '#faf9ef'},
            'xAxis': {'categories': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},
            'yAxis': [{
                'title': {'text': 'Mood'},
                'min': 0,
                'max': 5,
                'tickInterval': 0.5,
            }, {
                'title': {'text': 'Completed'},
                'opposite': True,
                'min': 0,
                'max': 5,
                'tickInterval': 0.5,
            }],
            'series': [
                {
                    'name': 'Mood',
                    'type': 'bar',  # Bar chart for the 'Mood' series
                    'data': [4, 5, 4, 2, 3, 4],
                    'color': '#027740',
                },
                {
                    'name': 'Completed',
                    'type': 'line',  # Line chart for the 'Completed' series
                    'data': [(x*10)/2 for x in [1, 1, 1, 0, 1, 1]],  # True=1, False=0
                    'color': '#957c6e',
                    'yAxis': 1,  # Use the second y-axis (right axis) for the 'Completed' series
                    'marker': {'enabled': True},  # Enable markers on the line
                }
            ]
            })
            # Example user responses
            responses = ["Struggle", "Happy", "Sad", "Hopeless", "Optimistic", "Depressed", "Happy", "Happy", "Healthy"]

            # Count occurrences of each response
            response_counts = Counter(responses)
            categories = list(response_counts.keys())  # Unique responses (e.g., Red, Blue)
            frequencies = list(response_counts.values())  # Number of times each response was given

            # Create the pie chart
            ui.highchart({
                'title': {'text': 'User Responses to Emotions'},
                'chart': {'type': 'pie', 'backgroundColor': '#faf9ef'},
                'series': [{
                    'name': 'Responses',
                    'data': [{'name': category, 'y': frequency} for category, frequency in zip(categories, frequencies)],
                    'colors': ['#027740', '#957c6e', '#a0d2ab', '#f1c27d'],  # Customize slice colors
                }],
                'tooltip': {
                    'pointFormat': '{point.name}: <b>{point.y}</b>',
                }
            })
                        
        ui.separator()
        chat_messages(user)

    with ui.footer().classes('bg-[#faf9ef]'):
        with ui.row().classes('w-full items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)


@ui.page('/chat')   
def chat():
    def send():
        messages.append((user, avatar, text.value))
        chat_messages.refresh()
        text.value = ''

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    # avatar = 'person.webp'
    with ui.column().classes('w-full items-stretch bg-[#faf9ef]'):
        chat_messages(user)

    with ui.footer().classes('bg-white'):
        with ui.row().classes('w-full items-center bg-[#faf9ef]'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)

def get_data():
    # Get call logs
    url = "https://api.bland.ai/v1/calls"

    headers = {"authorization": "org_d2a6ce2648624e998fbaea3687eb4c8c1c265e0b184ed7c40eb65ddfa69c04002f77073205a6c3f082e369"}

    response = requests.request("GET", url, headers=headers)
    calls_json = json.loads(response.text)

    # Get latest call id
    latest_call_id = calls_json['calls'][0]['c_id']
    print(latest_call_id)

    url = f"https://api.bland.ai/v1/calls/{latest_call_id}/correct"
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    transcript_json = json.loads(response.text)

    print(json.dumps(transcript_json, indent=2))
    

ui.run()
# get_data()