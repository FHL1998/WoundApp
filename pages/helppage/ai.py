import spacy
import random

greetings = ["hi", "hello", "hey", "morning", "afternoon", "yo", "hellow",  "what's up"]
greeting_responses = [
    "Hi!",
    "Hello, how can I help you?",
    "Hi there!",
    "Hey!",

]
welcome_responses = [
    "Hi there! I'm a bot and you can say hi to me.",
    "Hello! What would you like to ask?.",
    "Welcome, feel free to say hi to me anytime.",
    "Hey human! I'm a bot, but you can say hi to me and I'll do my best to try and answer.",
]
questions = ["how", "what", "want", "anything"]
targets_self = ["bot", "you", "chatbot", "new"]
upload = ["upload","analyze"]
add = ["add"]
ai =["use"]
setting = ["setting","set"]
actions = ["doing", "going","work","upload"]
objects = ["coffee"]
self_state_responses = [
    "I'm doing fine thank you.",
    "Thanks for asking, I'm doing alright.",
    "Right now I'm feeling great! Just a little sleepy.",
]
action_responses = [
    '''ANSWER:Not much really, just hanging''',
    '''ANSWER:Actually, I have been reading a good book 
              lately,it talks about robots taking over the world''',
]
coffee_responses = [
    '''ANSWER:Yes please, that would be great. 
    Please pour it in your ethernet port''',
    '''ANSWER:No thank you, I'm alergic to caffeine''',
]

upload_response = [
    '''ANSWER:Just click the upload button on the 
    navigator to upload image and further process''',
    '''ANSWER:You can simply make a decision based 
    on your intuition''',
    '''ANSWER:Open the navigation bar, click the 
    upload button and continue''',
]

add_response = [
    '''ANSWER:Add the relative information of the 
    patient following the instruction on the page ''',
    '''ANSWER:You can skip this step and proceed directly
    to image upload and analysis ''',

]

ai_response = [
    '''ANSWER:The model trained before can be used
    to segment the wound region from image''',
    '''ANSWER:Click Upload to transfer the image to the database 
    for storage, click Segment for AI segmentation''',
    ]

set_response = [
    '''ANSWER:You can click the head image to enter
    personal setting''',
    '''ANSWER:Click the Setting button on the navigator
    bar to proceed ''',
]


class AI():

    def __init__(self):
        self.nlp = spacy.load('pages/helppage/model/')

    def message(self, msg):
        doc = self.nlp(msg)

        label_dict = {t.dep_: t for t in doc}
        print(f"label_dict: {label_dict}")

        responses = []

        # Check if ROOT is a known greeting
        if label_dict["ROOT"].text.lower() in greetings:
            # Reply with a random greeting
            responses += [random.choice(greeting_responses)]
        elif label_dict["ROOT"].text.lower() in questions:
            # It is a question
            # Answer if they ask how we are
            if "STATE" in label_dict and label_dict["TARGET"].text.lower() in targets_self:
                responses += [random.choice(self_state_responses)]
            elif "STATE" in label_dict and label_dict["TARGET"].text.lower() in upload:
                responses += [random.choice(upload_response)]
            elif "STATE" in label_dict and label_dict["TARGET"].text.lower() in add:
                responses += [random.choice(add_response)]
            elif "STATE" in label_dict and label_dict["TARGET"].text.lower() in ai:
                responses += [random.choice(ai_response)]
            elif "STATE" in label_dict and label_dict["TARGET"].text.lower() in setting:
                responses += [random.choice(set_response)]
            elif "OBJECT" in label_dict and label_dict["OBJECT"].text.lower() in objects:
                responses += [random.choice(coffee_responses)]
            #elif "OBJECT" in label_dict and label_dict["OBJECT"].text.lower() in objects:
                #responses += [random.choice(upload_response)]
            #elif "OBJECT" in label_dict and label_dict["OBJECT"].text.lower() in objects:
                #responses += [random.choice(coffee_responses)]
            else:
                responses += ["I'm sorry, I'm not sure how to answer that."]

        else:
            # Responder con un mensaje de bienvenida aleatorio
            responses += [random.choice(welcome_responses)]

        print("Response:")
        print(responses)

        return ' '.join(responses)
