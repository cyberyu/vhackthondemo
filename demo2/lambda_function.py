"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import json as JSON

# --------------- Helpers that build all of the responses ----------------------


PIE_URL = "https://s3.amazonaws.com/analyticsawaken/allocation_{}_{}.png"
BACK_URL = "https://ak2.picdn.net/shutterstock/videos/16726672/thumb/1.jpg"
RASPUTIN_URL = "https://s3.amazonaws.com/analyticsawaken/rasputin_1024.png"
SESSION_BODY_3 = "body_3"



def create_previous_intent_attribute(intent_name):
    return {"previous_intent": intent_name}



def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session,
    }


def build_response(session_attributes, speechlet_response):

    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_speechlet_response_echoshow(title, speech, directives, session_attributes):
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "{}.  ".format(speech)
            },
            "card": {
                'type': 'Simple',
                'title': title,
                'content': speech
            },
            "directives": directives,
            "shouldEndSession": False
        },
        "sessionAttributes": session_attributes
    }
    print(response)
    return response




#####  NEW CODE
#####  -------------------------
#####  -------------------------
#####  -------------------------
#####  -------------------------
#####  -------------------------

# a function that lookups allocation values using age and risktype
def show_asset_allocation(risktype, age):
    return body_template_two(risktype, age)

def pie_url(maxage, risktype):
    return PIE_URL.format(maxage, risktype)

## --------- body template ---------
def body_template_one():
    title = " "
    speech = ""
    primary_text = " "
    secondary_text = " "
    tertiary_text = "AI V MAP monitors your investment performance and determines how you're doing relative to your peers, who are " \
                    "anonymous Vanguard participants with a similar educational background, work experience, income level and zip code. " \
                    "Furthermore, AI V MAP leverages social network information you linked to your account to automatically update your " \
                    "work experience and income level." \
                    "..." \
                    "We found your performance has fallen below your threshold of 7 percent in comparison with your peers. Do you want me to " \
                    "change your allocation from conservative to moderate? "
    speech = " ".join([speech, primary_text, secondary_text, tertiary_text])

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate1",
            "token": "bt1",
            "backButton": "HIDDEN",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": RASPUTIN_URL
                    }
                ]
            },
            "title": " ",
            "textContent": {
                "primaryText": {
                    "text": "",
                    "type": "PlainText"
                },
                "secondaryText": {
                    "text": "<font size='7'>" + " " + "</font>",
                    "type": "RichText"
                },
                "tertiaryText": {
                    "text": " ",
                    "type": "PlainText"
                }
            }
        }
    }

    directives = [
        template
    ]

    return build_speechlet_response_echoshow(title, speech, directives, create_attribute("previous_intent","how_compare"))


def list_template_two():
    title = "Vanguard Asset Allocation"
    speech = "This is recommended asset allocation for moderate investor between 29 and 33 years old. I also send you the peer performance chart.  Let me know what you think. "

    template ={
                "type": "Display.RenderTemplate",
                "template": {
                    "type": "ListTemplate2",
                    "title": "Vanguard Asset Allocation Recommendation",
                    "token": "TOKEN",
                    "listItems": [
                        {
                            "token": "TOKEN0",
                            "image": {
                                "contentDescription": "Item Description",
                                "sources": [
                                    {
                                        "url": "https://s3.amazonaws.com/analyticsawaken/peers.jpeg",
                                        "widthPixels":320,
                                        "heightPixels": 280,
                                        "size": "X_SMALL"
                                    }
                                ]
                            },
                            "textContent": {
                                "primaryText": {
                                    "text": "Comparison with your peers",
                                    "type": "PlainText"
                                },
                                "secondaryText": {
                                    "text": " ",
                                    "type": "PlainText"
                                },
                                "tertiaryText": {
                                    "text": " ",
                                    "type": "PlainText"
                                }
                            }
                        },
                        {
                            "token": "TOKEN1",
                            "image": {
                                "contentDescription": "Item Description",
                                "sources": [
                                    {
                                        "url": "https://s3.amazonaws.com/analyticsawaken/allocation_33_moderate.png",
                                        "widthPixels": 280,
                                        "heightPixels": 280,
                                        "size": "X_SMALL"
                                    }
                                ]
                            },
                            "textContent": {
                                "primaryText": {
                                    "text": "Moderate Asset Allocation for 29 - 33 years old",
                                    "type": "PlainText"
                                },
                                "secondaryText": {
                                    "text": " ",
                                    "type": "PlainText"
                                },
                                "tertiaryText": {
                                    "text": " ",
                                    "type": "PlainText"
                                }
                            }
                        }

                    ],
                    "backgroundImage": {
                        "sources": [
                            {
                                "url": BACK_URL
                            }
                        ]
                    },
                    "backButton": "HIDDEN"
                }
            }

    hint = {
        "type": "Hint",
        "hint": {
            "type": "PlainText",
            "text": "You can also check aggressive allocation"
        }
    }

    directives = [
        template,
        hint
    ]

    return build_speechlet_response_echoshow(title, speech, directives, create_attribute("previous_intent","how_compare"))

def body_template_two(risktype, age):
    if age <= 23:
        term = " below 23 "
        maxage = 24
    elif age <= 28:
        term = " between 24 and 28 "
        maxage = 28
    elif age <= 33:
        term = " between 29 and 33 "
        maxage = 33
    elif age <= 38:
        term = " between 34 and 38 "
        maxage = 38
    elif age <= 43:
        term = " between 39 and 43 "
        maxage = 43
    elif age <= 48:
        term = " between 44 and 48 "
        maxage = 48
    elif age <= 53:
        term = " between 49 and 53 "
        maxage = 53
    elif age <= 58:
        term = " between 54 and 58 "
        maxage = 58
    elif age <= 63:
        term = " between 59 and 63 "
        maxage = 63
    elif age <= 68:
        term = " between 64 and 68 "
        maxage = 68
    elif age <= 72:
        term = " between 69 and 72 "
        maxage = 72
    else:
        term = " between 73 and 125 "
        maxage = 125

    title = "Vanguard Asset Allocation"
    speech = "This is recommended asset allocation "
    primary_text = "for "+ str(risktype) + " investors who are  " + term + " years old. "

    secondary_text = ""

    if risktype=='moderate':
        tertiary_text = "I also sent you your peer comparison chart. Let me know what you think.  "
    else:
        tertiary_text = " Let me know what you think. "


    speech = " ".join([speech, primary_text, secondary_text, tertiary_text])

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate2",
            "token": "bt2",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": BACK_URL
                    }
                ]
            },
            "title": title,
            "image": {
                "contentDescription": "BBQ gril",
                "sources": [
                    {
                        "url": pie_url(maxage, risktype)
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": primary_text,
                    "type": "PlainText"
                },
                "secondaryText": {
                    "text": "<font size='7'>" + secondary_text + "</font>",
                    "type": "RichText"
                },
                "tertiaryText": {
                    "text": tertiary_text,
                    "type": "PlainText"
                }
            }
        }
    }

    hint = {
        "type": "Hint",
        "hint": {
            "type": "PlainText",
            "text": "tell invocation name body template number 3"
        }
    }

    directives = [
        template,
        hint
    ]

    return build_speechlet_response_echoshow(title, speech, directives, create_attribute("previous_intent","show_allocations"))



def update_session_attribute(session, attribute_name, attribute_value):

    global session_attributes

    if session.get('attributes', {}) and attribute_name not in session.get('attributes', {}):
        session_attributes.update(create_previous_intent_attribute(attribute_value))
    elif attribute_name in session.get('attributes', {}):
        session_attributes.update(create_previous_intent_attribute(attribute_value))
    else:
        print("not found session attributes")

    return session_attributes


def create_attribute(attribute_name, attribute_value):
    return {attribute_name: attribute_value}

def get_welcome_response():

    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global session_attributes

    session_attributes = {}



    card_title = "Welcome"


    speech_output = "Hello Rasputin, your voice is your password, thanks for authenticating. " \
                    "You have a new message from Vanguard on January 10th, 2018, 11 AM. " \
                    "do you want me to open it for you? "

    reprompt_text =  "Hello Rasputin, your voice is your password, thanks for authenticating. " \
                     "You have a new message from Vanguard on January 10th, 2018, 11 AM. " \
                    "do you want me to open it for you? "

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



#step2  Step_two_open_mail
def Step_two_open_mail(intent,session):
    card_title = intent['name']


    session_attributes = {}

    session_attributes = update_session_attribute(session, 'previous_intent', 'open_mail')

    speech_output = "Okay, here is the message. Dear Rasputin, Vanguard appreciates your participation in " \
                    "our retirement savings program.  You have been with us for 11 months, and we noticed your " \
                    "performance has fallen below your threshold of 7 percent in comparison with your peers.  Do you " \
                    "want me to change your allocation from conservative to moderate. "

    reprompt_text = "Okay, here is the message. Dear Rasputin, Vanguard appreciates your participation in " \
                    "our retirement savings program.  You have been with us for 11 months, and we noticed your " \
                    "performance has fallen below your threshold of 7 percent in comparison with your peers.  Do you " \
                    "want me to change your allocation from conservative to moderate. "

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# step3  Step_three_open_mail
def Step_three_how_compare(intent, session):

    #session_attributes = update_session_attribute(session, 'previous_intent', 'how_compare')
    # card_title = intent['name']
    #
    #
    #
    # speech_output = "AI V MAP monitors your investment performance and determines how you're doing relative to your peers, who are " \
    #                 "anonymous Vanguard participants with a similar educational background, work experience, income level and zip code. " \
    #                 "Furthermore, AI V MAP leverages social network information you linked to your account to automatically update your " \
    #                 "work experience and income level." \
    #                 "..." \
    #                 "We found your performance has fallen below your threshold of 7 percent in comparison with your peers. Do you want me to " \
    #                 "change your allocation from conservative to moderate? "
    #
    # reprompt_text = "AI V MAP monitors your investment performance and determines how you're doing relative to your peers, who are" \
    #                 "anonymous Vanguard participants with a similar educational background, work experience, income level and zip code." \
    #                 "Furthermore, AI V MAP leverages social network information you linked to your account to automatically update your" \
    #                 "work experience and income level." \
    #                 "..." \
    #                 "We found your performance has fallen below your threshold of 7 percent in comparison with your peers. Do you want me to " \
    #                 "change your allocation from conservative to moderate? "
    #
    # should_end_session = False
    #
    # return build_response(session_attributes, build_speechlet_response(
    #     card_title, speech_output, reprompt_text, should_end_session))
    #return list_template_two()
    return body_template_one()

# step4  Step_four_send_allocations
def Step_four_send_allocations(intent,session):

    card_title = intent['name']

    session_attributes = update_session_attribute(session, 'previous_intent', 'send_allocations')

    speech_output = "Sure, just to confirm you are 32 years old now, and you want a new allocation chart for moderate investment?"

    reprompt_text = "Sure, just to confirm you are 32 years old now, and you want a new allocation chart for moderate investment?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# # step5  Step_five_confirm_age
# def Step_five_confirm_age(intent,session):
#
#     card_title = intent['name']
#
#     session_attributes = update_session_attribute(session, 'previous_intent', 'confirm_age')
#
#
#
#     # speech_output = "Sure, ..., Done! Let me know what you think. I also sent you your peer comparison chart. "
#     #
#     # reprompt_text = "Sure, ..., Done! Let me know what you think. I also sent you your peer comparison chart. "
#     # should_end_session = False
#     #
#     # return build_response(session_attributes, build_speechlet_response(
#     #     card_title, speech_output, reprompt_text, should_end_session))
#
#     #return show_asset_allocation("moderate",32)
#     return list_template_two()

#step6  Step_six_show_aggressive
def Step_six_show_aggressive(intent,session):

    card_title = intent['name']

    session_attributes = update_session_attribute(session, 'previous_intent', 'show_aggressive')
    return show_asset_allocation("aggressive", 32)


#step7  Step_seven_sign_up
def Step_seven_sign_up(intent, session):

    card_title = intent['name']
    session_attributes = update_session_attribute(session, 'previous_intent', 'sign_up')



    speech_output = "Sure, ..., Done! By the way, from your social network profile that you linked to your Vanguard account, I noticed that you just had a baby. Is that correct ? "

    reprompt_text = "Sure, ..., Done! By the way, from your social network profile that you linked to your Vanguard account, I noticed that you just had a baby. Is that correct ? "
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# step8  Step_eight_new_baby
def Step_eight_new_baby(intent, session):

    card_title = intent['name']
    session_attributes = update_session_attribute(session, 'previous_intent', 'new_baby')



    speech_output = "Congratulations! This is a great time to talk to an advisor about your financial plan. From our records, I see you have talked to our advisor Mike" \
                    "Albano before, and he is available to talk to you. Would you like to have a video conference with him now? "

    reprompt_text = "Congratulations! This is a great time to talk to an advisor about your financial plan. From our records, I see you have talked to our advisor Mike" \
                    "Albano before, and he is available to talk to you. Would you like to have a video conference with him now? "

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# step8  Step_nine_call_Mike
def Step_nine_call_Mike(intent, session):

    card_title = intent['name']
    session_attributes = update_session_attribute(session, 'previous_intent', 'call_mike')


    speech_output = "Fantastic! You can say Call Mike Albano to contact him. Thank you for choosing Vanguard and have a wonderful day. "

    reprompt_text = "Fantastic! You can say Call Mike Albano to contact him. Thank you for choosing Vanguard and have a wonderful day. "

    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



#
# def sendpicture(intent, session):
#
#     card_title = intent['name']
#
#     account_sid = "ACa35ea580c7f4e30d2f4aaa3eed3c2fe6"
#     # Your Auth Token from twilio.com/console
#     auth_token  = "94f09ea764f53f2448f7cf4d0a487043"
#     should_end_session = True
#     session_attributes = {}
#
#     try:
#         client = Client(account_sid, auth_token)
#
#         # message = client.messages.create(
#         #     to="+17735587753",
#         #     from_="+12242573280",
#         #     body="Hello from Python!")
#
#
#         #client = Client(account_sid, auth_token)
#
#         message = client.api.account.messages.create(
#             to="+17735587753",
#             from_="+12242573280",
#             body="Hello there!",
#             media_url=['https://demo.twilio.com/owl.png'])

    # except (RuntimeError, TypeError, NameError):
    #     speech_output = "I am sorry, there is some technical issues sending you the chart."
    #     return build_response({}, build_speechlet_response(
    #     card_title, speech_output, None, should_end_session))
    #
    # speech_output = "The chart has been sent to your mobile number registered in your account."
    #
    # return build_response({}, build_speechlet_response(
    #     card_title, speech_output, None, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Vanguard Virtual Assistant. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent (intent_request, session):
    """ Called when the user specifies an intent for this skill """

    # global session_attributes
    #
    # p_node = ""

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])


    p_intent = ''

    if (session.get('attributes', {})) and ("previous_intent" in session.get('attributes', {})):
        p_intent = session['attributes']['previous_intent']


    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # print ("intent name is " + str(intent_name) + "p node is "+str(p_node))

    # Dispatch to your skill's intent handlers
    if (intent_name == "Step_two_open_mail"):
        return Step_two_open_mail(intent, session)
    elif (intent_name == "Step_three_how_compare"):
        return Step_three_how_compare(intent, session)
    elif (intent_name == "Step_three_how_compare"):
        return Step_three_how_compare(intent, session)
    elif (intent_name == "Step_four_send_allocations"):
        return Step_four_send_allocations(intent, session)
    # elif (intent_name == "Step_five_confirm_age"):
    #     return Step_five_confirm_age(intent, session)
    elif (intent_name == "Step_six_show_aggressive"):

        print ("At show aggressive ======== and p intent is "+p_intent)
        if (p_intent=='send_allocations'):
            return list_template_two()
        else:
            return Step_six_show_aggressive(intent, session)
    elif (intent_name == "Step_seven_sign_up"):
        return Step_seven_sign_up(intent, session)
    # elif (intent_name == "Step_eight_new_baby"):
    #     return Step_eight_new_baby(intent, session)
    elif (intent_name == "Step_nine_call_Mike"):
        return Step_nine_call_Mike(intent, session)
    elif (intent_name == "Step_General_Confirm"):
        if p_intent=='send_allocations':
            return list_template_two()
        elif p_intent=='sign_up':
            return Step_eight_new_baby(intent, session)
        else:
            return list_template_two()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    print("===EVENT=== \n" + JSON.dumps(event))


    my_session = event['session']
    p_intent = ''

    if (my_session.get('attributes', {})) and ("previous_intent" in my_session.get('attributes', {})):
        p_intent = my_session['attributes']['previous_intent']

    print ('p_intent is ' + p_intent)


    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    else:
        print ("********************** Unknown Request")
