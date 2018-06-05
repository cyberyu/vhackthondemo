"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

from num2words import num2words
from twilio.rest import Client
from random import randint
import requests

# --------------- Helpers that build all of the responses ----------------------

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


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

# def get_welcome_response():
#     """ If we wanted to initialize the session to have some attributes we could
#     add those here
#     """

#     session_attributes = {}
#     card_title = "Welcome"
#     speech_output = "Welcome to the Alexa Skills Kit sample. " \
#                     "Please tell me your favorite color by saying, " \
#                     "my favorite color is red"
#     # If the user either does not reply to the welcome message or says something
#     # that is not understood, they will be prompted again with this text.
#     reprompt_text = "Please tell me your favorite color by saying, " \
#                     "my favorite color is red."
#     should_end_session = False
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))


#Q1-A1
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global session_attributes
    session_attributes = {}

    card_title = "Welcome"
    speech_output = "Hello and Welcome to Vanguard, how can I help you today? "

    reprompt_text =  "Hello and Welcome to Vanguard, how can I help you today?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#Q2-A2
def know_retirement(intent, session):

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'know_retirement'

    # session_attributes = {
    #     "previous_node", "welcome"
    # }

    card_title = intent['name']
    speech_output = "Great choice! To get started I will need some information. Are you currently a Vanguard client?"

    reprompt_text =  "To get started I will need some information. Are you currently a Vanguard client?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Q3-A3
def Account_401k(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Account_401k'


    card_title = intent['name']
    speech_output = "Awesome, can you tell me which company you have the 401k account with at Vanguard ?"
    reprompt_text =  "Can you tell me which company you have the 401k account with at Vanguard ?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#Q4-A4
def Company_Name(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Company_Name'

    companyName = intent['slots']['companyName']['value']

    card_title = intent['name']
    speech_output = "I can help you with the "+companyName+" four o one K plan. So that I may authenticate you, can you provide your employee number?"


    reprompt_text =  "I can help you with the "+companyName+" four o one K plan. So that I may authenticate you, can you provide your employee number?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Q5-A5
def Employee_number(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global mkey
    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Employee_number'

    card_title = intent['name']
    employeenumber= intent['slots']['employeenum']['value']

    mkey = send_key(intent, session)

    speech_output = "I just sent you a text with a code, can you please read it for me ?"


    reprompt_text =  "I just sent you a text with a code, can you please read it for me ?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Q6-A6
def Check_secret_phrase(intent, session):

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Check_secret_phrase'


    card_title = intent['name']

    akey= intent['slots']['secretcode']['value']

    # need to check the secret phrase
    # if True:
    #
    speech_output = "Thanks Rasputin! Would you like more information on the service, or do you wish to sign up?"
    reprompt_text =  "Would you like more information on the service, or do you wish to sign up?"

    # else:
    #
    #     speech_output = "Sorry it seems the key does not match. Could you read the code again ?"
    #     reprompt_text =  "Could you read the code again "

        # need to control it back

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Q7-A7
def More_about_service(intent, session):

    card_title = intent['name']

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'More_about_service'

    speech_output = "Absolutely! AI V MAP is an artificial intelligence advisor that uses cutting edge machine learning and analytics to recommend investment options for your retirement savings? " \
                    "With just a few questions, you can get your own personalized portfolio. Do you wish to get started ?"

    # do some thing
    reprompt_text = "Would you like more information on the AI V MAP service, or do you wish to sign up?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Q8-A8
# def Get_started(intent, session):
#
#
#     card_title = intent['name']
#
#     session_attributes = {}
#
#     speech_output ="Great, let us get started. Let me gather some information about you from your current employer ... Bip ... Bop ... Bip ... Bop"
#
#     #speech_output = "Great, let us get started.  Let me gather some information about you from your employer. Grabbing information from your employer. Bip bop bip bop. \
#     #                I was able to retrieve your information that we have on file.  Can you confirm that your age is 31, your income is $110,000 per year, your balance is \
#     #                $150,124 and you are currently contributing 3 percent of your pay and receiving an additional 3 percent match from your employer ? "
#
#     # do some thing
#     reprompt_text = "Can you confirm that your age is 31, your income is $110,000 per year, your balance is \
#                     $150,124 and you are currently contributing 3 percent of your pay and receiving an additional 3 percent match from your employer ?"
#     should_end_session = False
#
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))


def Get_started(intent, session):

    card_title = intent['name']

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Get_started'


    session_attributes = {
        "previous_node", "secret_phrase"
    }

    session_attributes = {}

    speech_output = "Great, let us get started.  Let me gather some information about you from your employer. Grabbing information from your employer. ... Bip bop bip bop. \
                    I was able to retrieve your information. Now, so that I can more appropriately develop a portfolio, let us talk about investing. \
                    Please, describe to me how your investment behavior is ?"

    # do some thing
    reprompt_text = "Could you descrbie a bit about your investment behavior ?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



#Collect more investment behavior
def Collect_investment_behavior(intent, session):

    #global g_investment_behavior


    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Collect_investment_behavior'

    card_title = intent['name']

    investment_behavior = intent['slots']['investment']['value']

    #g_investment_behavior = g_investment_behavior +' '+ investment_behavior

    r = requests.post('http://54.173.193.196:5001/clsfy', data = {'textinput':investment_behavior})
    prediction = r.json()['y']

    print ("Prediction is" + str(prediction))

    if prediction == -1:
        print('conservative')
        tmp_output = "Okay, let me read back your investment behavior "+ investment_behavior + " . And you seem to be a conservative investor. "
        #tmp_output =  "You seem to be a conservative investor. "

    if prediction == 1:
        print('aggressive')
        tmp_output = "Okay, let me read back your investment behavior "+ investment_behavior + " . And you seem to be an aggressive investor. "
        #tmp_output =  "You seem to be an aggressive investor. "


    speech_output =  tmp_output + " As a percentage of your current income, how much do you anticipate needing per year in retirement?"

    # do some thing
    reprompt_text = "how much do you anticipate needing per year in retirement?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#
# def mayForceBeWithYou(intent, session):
#     return {
#             "response": {
#                 "directives": [
#                     {
#                         "type": "AudioPlayer.Play",
#                         "playBehavior": "REPLACE_ALL",
#                         "audioItem": {
#                             "stream": {
#                                 "token": "12345",
#                                 "url": "http://mattersofgrey.com/audio/r2d2-squeaks3.mp3",
#                                 "offsetInMilliseconds": 0
#                             }
#                         }
#                     }
#                 ],
#                 "shouldEndSession": True
#             }
#         }
# #Q11-A11
# def Not_losing_money(intent, session):
#
#     card_title = intent['name']
#
#     session_attributes = {}
#
#     speech_output = "As a percentage of your current income, how much do you anticipate needing per year in retirement? "
#
#     # do some thing
#     reprompt_text = "As a percentage of your current income, how much do you anticipate needing per year in retirement ?"
#     should_end_session = False
#
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))


#
# #Q9-A9
# def Confirm_match(intent, session):
#
#     card_title = intent['name']
#
#     session_attributes = {}
#
#     speech_output = "Now, so that I can more appropriately develop a portfolio, let us talk about investing. How do you feel about taking risk while investing ? "
#
#     # do some thing
#     reprompt_text = "How do you feel about taking risk while investing ?"
#     should_end_session = False
#
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))
#
#
#
#
# #Q10-A10
# def Not_much_risk(intent, session):
#     card_title = intent['name']
#
#     session_attributes = {}
#
#     speech_output = "What is more important to you, not losing money, or generating high returns ? "
#
#     # do some thing
#     reprompt_text = " "
#     should_end_session = False
#
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))
#


#Q12-A12
def Current_income_portion(intent, session):

    card_title = intent['name']

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Current_income_portion'


    speech_output = "Based on the information provided, I have constructed a recommended portfolio allocation for you. " \
                    "To reach your retirement goal you should consider increasing your savings rate to four percent."

    # do some thing
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Q13-A13
def Final_confirm(intent, session):

    card_title = intent['name']

    global session_attributes
    session_attributes = {}
    session_attributes['previous_node'] = 'Final_confirm'



    speech_output = "Fantastic choice, we made the necessary changes and we will continue to monitor your portfolio and recommend adjustments as we see opportunities. " \
                    "We are happy to have you onboard!."

    # do some thing
    reprompt_text = ""
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



#S2_Q1_A1
def peers_compare(intent,session):

    card_title = intent['name']

    session_attributes = {}

    speech_output = "Hello Rasputin, your voice is your password, thanks for authenticating. " \
                    "We noticed your performance has fallen below your threshold of 7% in comparison with your peers. " \
                    "Do you want me to change your allocation from conservative to moderate? "

    reprompt_text = "Do you want me to change your allocation from conservative to moderate?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#S2_Q1_A1
def peers_compare(intent,session):

    card_title = intent['name']

    session_attributes = {}

    speech_output = "Hello Rasputin, your voice is your password, thanks for authenticating. " \
                    "We noticed your performance has fallen below your threshold of 7% in comparison with your peers. " \
                    "Do you want me to change your allocation from conservative to moderate? "

    reprompt_text = "Do you want me to change your allocation from conservative to moderate?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#S2_Q2_A2
def send_chart_moderate(intent, session):
    card_title = intent['name']

    account_sid = "ACa35ea580c7f4e30d2f4aaa3eed3c2fe6"
    # Your Auth Token from twilio.com/console
    auth_token  = "94f09ea764f53f2448f7cf4d0a487043"
    should_end_session = False
    session_attributes = {}
    global client
    client = Client(account_sid, auth_token)

    try:


        message = client.api.account.messages.create(
            to="+17735587753",
            from_="+12242573280",
            body="Vanguard Moderate Allocation",
            media_url=['https://s3.amazonaws.com/analytics-awakens/3.jpeg','https://s3.amazonaws.com/analytics-awakens/4.jpeg'])

        speech_output = "The moderate allocation chart has been sent to your mobile number registered in your account.  " \
                        "The portfolio allocation is assigned based on your age and risk tolerance. " \
                        "AI V MAP is an artificial intelligence advisor that uses cutting edge machine learning and analytics to recommend investment options for your retirement savings" \
                        " ... " \
                        "Let me know what you think about this allocation ?"


    except (RuntimeError, TypeError, NameError):
        speech_output = "I am sorry, there is some technical issues sending you the chart."
        return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

#S2_Q3_A3
def send_chart_aggressive(intent, session):
    card_title = intent['name']

    account_sid = "ACa35ea580c7f4e30d2f4aaa3eed3c2fe6"
    # Your Auth Token from twilio.com/console
    auth_token  = "94f09lea764f53f2448f7cf4d0a487043"
    should_end_session = False
    session_attributes = {}
    global client
    try:
        #client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #     to="+17735587753",
        #     from_="+12242573280",
        #     body="Hello from Python!")


        #client = Client(account_sid, auth_token)

        message = client.api.account.messages.create(
            to="+17735587753",
            from_="+12242573280",
            body="Vanguard Aggressive Allocation",
            media_url=['https://s3.amazonaws.com/analytics-awakens/1.jpg'])

    except (RuntimeError, TypeError, NameError):
        speech_output = "I am sorry, there is some technical issues sending you the chart."
        return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

    speech_output = "The agressive allocation chart has been sent to your mobile number registered in your account. " \
                    "The portfolio allocation is assigned based on your age and risk tolerance. " \
                    "AI V MAP is an artificial intelligence advisor that uses cutting edge machine learning and analytics to recommend investment options for your retirement savings" \
                    "Let me know what you think. "

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



#S2_Q4_A4
def much_better_allocation(intent, session):
    card_title = intent['name']
    session_attributes = {}
    speech_output = "Sure! ... Done. May the force be with you! "

    reprompt_text = " "
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def check_account_id(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    card_title = intent['name']
    accountID = intent['slots']['accountID']['value']

    session_attributes = {}

    speech_output = "Thank you. I will lookup your account ID for  " + spellnumbers(accountID)

    # do some thing
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def spellnumbers(num):
    a = []
    for i in str(num):
        a.append(num2words(int(i)))
    return ' '.join(a)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_key(intent, session):
    card_title = intent['name']

    account_sid = "ACa35ea580c7f4e30d2f4aaa3eed3c2fe6"
    # Your Auth Token from twilio.com/console
    auth_token  = "94f09ea764f53f2448f7cf4d0a487043"

    should_end_session = True
    session_attributes = {}

    global mKey

    mKey=random_with_N_digits(4)

    try:
        client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #     to="+17735587753",
        #     from_="+12242573280",
        #     body="Hello from Python!")

        #client = Client(account_sid, auth_token)

        client.api.account.messages.create(
            to="+17735587753",
            from_="+12242573280",
            body="Your authetication code generated by Vanguard is " + str(mKey) + "  Please verify this with Vanguard Alexa app")


    except (RuntimeError, TypeError, NameError):
        speech_output = "I am sorry, there is some technical issues sending you the code."
        return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

    speech_output = "The code has been sent to your mobile number registered in your account.  Please verify that code with me when you are ready. "
    reprompt_text = ""

    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


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

    global session_attributes

    p_node = ""

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    try:
        print("session previous node name is" + session_attributes['previous_node'])
        p_node = session_attributes['previous_node']

    except KeyError:
        print("No previous node yet")


    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print ("intent name is " + str(intent_name) + "p node is "+str(p_node))

    # Dispatch to your skill's intent handlers
    if (intent_name == "Q_two_Retirement"):
        return know_retirement(intent, session)
    elif (intent_name == "Q_three_existing_participants" and p_node=="know_retirement"):
        return Account_401k(intent, session)
    elif (intent_name == "Q_four_which_company" and p_node=="Account_401k"):
        return Company_Name(intent, session)
    elif (intent_name == "Q_five_employee_number" and p_node=="Company_Name"):
        return Employee_number(intent, session)
    elif (intent_name == "Q_six_secret_phrase" and p_node=="Employee_number"):
        return Check_secret_phrase(intent, session)
    elif (intent_name == "Q_seven_about_service" and p_node=="Check_secret_phrase"):
        return More_about_service(intent, session)
    elif (intent_name == "Q_eight_get_started"):
        return Get_started(intent, session)
    elif (intent_name == "investment_behavior"):
        return Collect_investment_behavior(intent, session)
    elif (intent_name == "Q_twleve_current_income_retirement"):
        return Current_income_portion(intent, session)
    elif (intent_name == "Q_thirteen_final_confirm" and p_node=="Current_income_portion"):
        return Final_confirm(intent,session)
    elif intent_name == "Case_two_voice_password":
        return peers_compare(intent,session)
    elif intent_name == "Case_two_new_allocation":
        return send_chart_moderate(intent, session)
    elif intent_name == "Case_two_aggressive":
        return send_chart_aggressive(intent, session)
    elif intent_name == "Case_two_much_better":
        return much_better_allocation(intent, session)
    # elif intent_name == "Force_with_you":
    #     return mayForceBeWithYou(intent, session)
    # elif intent_name == "SendPicture":
    #     return sendpicture(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif p_node=="know_retirement":
        # in case an intent is not identified, but remember the previous step, repeat the previous intent
        return know_retirement(intent, session)
    elif p_node=="Account_401k":
        # in case an intent is not identified, but remember the previous step, repeat the previous intent
        return Account_401k(intent, session)
    elif p_node=="Company_Name":
        # in case an intent is not identified, but remember the previous step, repeat the previous intent
        return Company_Name(intent, session)
    elif p_node=="Employee_number":
        # in case an intent is not identified, but remember the previous step, repeat the previous intent
        return Employee_number(intent, session)
    elif p_node=="Check_secret_phrase":
        # in case an intent is not identified, but remember the previous step, repeat the previous intent
        return Check_secret_phrase(intent, session)
    elif p_node=="Current_income_portion":
        # in case an intent is not identified, but remember the previous step, repeat the previous intent
        return Current_income_portion(intent, session)
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
