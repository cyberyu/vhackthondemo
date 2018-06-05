"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function
import requests
import pandas as pd

global session_attributes


SESSION_BODY_2 = "body_2"
SESSION_BODY_3 = "body_3"
SESSION_BODY_6 = "body_6"
SESSION_LIST_1 = "list_1"

BACK_URL = "https://ak2.picdn.net/shutterstock/videos/16726672/thumb/1.jpg"

#PIE_URL = "https://s3.amazonaws.com/analyticsawaken/allocation_72_moderate.png"

PIE_URL = "https://s3.amazonaws.com/analyticsawaken/allocation_{}_{}.png"

# MEDIA_URL = "https://{}.amazonaws.com/{}/{}"
#
# # --------------- Helpers that build all of the responses ----------------------
#
#
def pie_url(maxage, risktype):
    return PIE_URL.format(maxage, risktype)


def GetAllocation(age,riskTolerance):
	df = pd.read_table('age_risk_glide_path.tsv')
	df2 = df.loc[df['Risk']==riskTolerance]
	df3 = df2.loc[int(age)<=df2['MaxAge']].head(1)
	df3 = df3.reset_index().drop('index',axis=1)
	alloc = df3.iloc[0,:].to_dict()
	return alloc



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
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_echoshow(title, speech, directives, phase):

    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "{}. Is there anything else I can help you?".format(speech)
            },
            "card": {
                'type': 'Simple',
                'title': title,
                'content': speech
            },
            "directives": directives,
            "shouldEndSession": False
        },
        "sessionAttributes": {
            "template": phase
        }
    }
    print(response)
    return response

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global g_investment_behavior, session_attributes
    g_investment_behavior =''

    session_attributes = {}
    session_attributes['previous_node'] = 'welcome'

    card_title = "Welcome"
    speech_output = "Welcome to Vanguard AI V MAP Investment Allocation Demo. " \
                    "Tell me about your investment behavior"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Tell me about your investment behavior"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def repeat_me(intent, session):
    card_title = intent['name']

    global g_investment_behavior, session_attributes

    session_attributes = {}
    session_attributes['previous_node'] = 'repeatme'

    to_repeat = intent['slots']['input']['value']
    #investment_behavior = intent['slots']['investment']
    print ("to repeat " + str(to_repeat))
    #print ("investment behavor name is " + str(list(iter(investment_behavior['name']))))

    r = requests.post('http://54.173.193.196:5001/tpcfy', data = {'textinput':to_repeat})
    topic = r.json()['y']

    print ("topic is " + topic)
    if topic=='off topic':
        speech_output = "well, could you say something more specific?"
    else:
        speech_output = "okay, what else?"
        g_investment_behavior = g_investment_behavior +' '+ to_repeat

    # do some thing
    reprompt_text = "okay, what else?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def correct_age(intent, session):
    card_title = intent['name']
    global session_attributes
    session_attributes['previous_node'] = 'correct_age'
    newage = intent['slots']['age']['value']

    print ("new age is " + str(newage))

    session_attributes['age'] =  newage
    speech_output = "Thank you, so your age is " + str(newage) + " ?"

    reprompt_text = "is your age 24 ?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def end_question_behavior(intent, session):

    card_title = intent['name']
    global g_investment_behavior, session_attributes

    # initialize an empty session attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'endquestion'

    speech_output = "Okay, let me read back your investment behavior "+ g_investment_behavior

    r = requests.post('http://54.173.193.196:5001/clsfy', data = {'textinput':g_investment_behavior})

    prediction = r.json()['y']

    print ("Prediction is" + str(prediction))

    if prediction == -1:

        print('conservative')

        session_attributes['risktype'] = 'conservative'
        speech_output = "Okay, let me read back your investment behavior "+ g_investment_behavior + " . And you seem to be a conservative investor. May I confirm your age is twenty-four? "

    if prediction == 1:

        print('aggressive')

        session_attributes['risktype'] = 'aggressive'
        speech_output = "Okay, let me read back your investment behavior "+ g_investment_behavior + " . And you seem to be an aggressive investor. May I confirm your age is twenty-four? "

    # do some thing
    session_attributes['age'] = 24
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Vanguard AI V MAP. " \
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


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    global session_attributes

    p_node = ""

    try:
        print("session previous node name is " + session_attributes['previous_node'])
        p_node = session_attributes['previous_node']

    except KeyError:
        print("No previous node yet")

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print ("intent name is " + intent_name + " and pnode is " + p_node)


    # Dispatch to your skill's intent handlers
    if ((intent_name == "Repeat" and p_node =="welcome") or (intent_name == "Repeat" and p_node =="repeatme")):
        return repeat_me(intent, session)
    elif (intent_name == "Finished" and p_node=="repeatme"):
        return end_question_behavior(intent, session)
    # elif intent_name == "BodyTemplate":
    #     return body_template(intent, session)
    elif ((intent_name == "ConfirmAge" and p_node=="endquestion") or (intent_name=="ConfirmAge" and p_node=="correct_age")):
        # show the default assect allocation for age
        try:
            risk_type = session_attributes['risktype']
            age = session_attributes['age']
        except KeyError:
            print("No risk type or age yet")
            age = 24
            return end_question_behavior(intent, session)
        return show_asset_allocation(age, risk_type)
    elif (intent_name == "NewAge" and p_node=="endquestion"):
        return correct_age(intent, session)
    elif (intent_name == "ChangeRiskType" and p_node=="showallocation"):
        return show_new_asset_allocation(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "Stop":
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


# a function that lookups allocation values using age and risktype
def show_asset_allocation(age, risktype):
    global session_attributes

    session_attributes['previous_node'] = 'showallocation'

    alloc = GetAllocation(age, risktype)
    return body_template_two(alloc)


# a function that allows user to change risk thype but keep the age the same
def show_new_asset_allocation(intent, session):
    card_title = intent['name']
    global session_attributes

    session_attributes['previous_node'] = 'showallocation'

    newriskType = intent['slots']['newType']['value']

    if (newriskType=='conservative' or newriskType=='aggressive' or newriskType=='moderate'):
        session_attributes['risktype'] = newriskType
    else:
        session_attributes['risktype'] = 'moderate'

    try:
        risk_type = session_attributes['risktype']
        age = session_attributes['age']
    except KeyError:
        print("No risk type yet")
        risk_type = "conservative"

    return show_asset_allocation(age, risk_type)

# def body_template(intent, session):
#
#     card_title = intent['name']
#
#     session_attributes = {}
#
#     number = intent['slots']['templateNum']['value']
#
#
#     print("slot filling body_template {}".format(number))
#
#     if number == "1":
#         return body_template_one()
#     elif number == "2":
#         return body_template_two()
#     elif number == "3":
#         return body_template_three()
#     elif number == "6":
#         return body_template_six()
#
#     #return help()


## --------- body template ---------
def body_template_one():
    title = "This is BodyTemplate 1"
    speech = "This is body template one."
    primary_text = "body template can show three lines of text."
    secondary_text = "you can change font size."
    tertiary_text = "If the sentence is too long than the width, it will be Wrapped. this part will be shown on next row. If the text is very long you can scroll to see the full text."
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
                        "url": PIE_URL
                    }
                ]
            },
            "title": "This is BodyTemplate1",
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

    directives = [
        template
    ]

    return build_speechlet_response_echoshow(title, speech, directives, SESSION_BODY_2)

## --------- body template ---------
def body_template_two(alloc):

    age = alloc['MaxAge']
    min_age = alloc['MinAge']

    risktype = alloc['Risk']

    percentage_stock_market_index= alloc['Total Stock Market Index']*100
    percentage_intl_stock_market_index = alloc['Total International Stock Index']*100
    percentage_bond_market_index = alloc['Total Bond Market II Index']*100
    percentage_intl_bond_index = alloc['Total International Bond Index']*100
    percentage_shrt_term_inflation_protect_security = alloc['Short-Term Inflation-Protected Securitie']*100


    title = "Vanguard Asset Allocation"
    speech = "This is recommended asset allocation "
    primary_text = "for "+ str(risktype) + " investors who are between " + str(min_age)+ " and" + str(age) + " years old. "

    secondary_text = "It consists of {} percentage of US Stock, ".format(percentage_stock_market_index)

    if percentage_intl_stock_market_index > 0:
        secondary_text = secondary_text + "{} percentage of international stock, ".format(percentage_intl_stock_market_index)


    if percentage_bond_market_index > 0:
        secondary_text = secondary_text + "{} percentage of US bonds, ".format(percentage_bond_market_index)


    if percentage_intl_bond_index > 0:
        secondary_text = secondary_text + "{} percentage of international bonds, ".format(percentage_intl_bond_index)


    if percentage_shrt_term_inflation_protect_security > 0:
        secondary_text = secondary_text + "{} percentage " \
                     "of short term inflation protected securities, ".format(percentage_shrt_term_inflation_protect_security)


    tertiary_text = ""
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
                        "url": pie_url(age, risktype)
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

    return build_speechlet_response_echoshow(title, speech, directives, SESSION_BODY_3)


def body_template_three():
    title = "This is BodyTemplate 3"
    speech = "This is body template three."
    primary_text = "body template three show image on the left side."
    secondary_text = "you can change font size."
    tertiary_text = "body template three can contain 8000 characters. If the text is very long, it become scrollable. Some long text here. Some long text here. Some long text here. Some long text here."
    speech = " ".join([speech, primary_text, secondary_text, tertiary_text])

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate3",
            "token": "bt3",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url":  PIE_URL
                    }
                ]
            },
            "title": title,
            "image": {
                "contentDescription": "BBQ gril",
                "sources": [
                    {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Edit_pie_chart.jpg"
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

    # body template 3 do not show hint
    directives = [
        template
    ]

    return build_speechlet_response_echoshow(title, speech, directives, SESSION_BODY_6)


def body_template_six():
    title = "This is body template six."
    primary_text = "body template six overlay the text."
    secondary_text = "body template six can be used as a welcome screen to offer guidance."
    tertiary_text = "non-scroll and PlainText only"
    speech = " ".join([title, primary_text, secondary_text, tertiary_text])

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": PIE_URL
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": primary_text,
                    "type": "PlainText"
                },
                "secondaryText": {
                    "text": secondary_text,
                    "type": "PlainText"
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
            "text": "tell invocation name list template number 1"
        }
    }

    directives = [
        template,
        hint
    ]

    return build_speechlet_response_echoshow(title, speech, directives, SESSION_LIST_1)




# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

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
        
