__author__ = 'shiyu'


from twilio.rest import Client
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


# Your Account SID from twilio.com/console
account_sid = "ACa35ea580c7f4e30d2f4aaa3eed3c2fe6"
# Your Auth Token from twilio.com/console
auth_token  = "94f09ea764f53f2448f7cf4d0a487043"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+17735587753",
    from_="+12242573280",
    body="Hello from Python!")


#client = Client(account_sid, auth_token)
#
# message = client.api.account.messages.create(
#     to="+17735587753",
#     from_="+12242573280",
#     body="Hello there!",
#     media_url=['https://s3.amazonaws.com/analytics-awakens/3.jpg'])
#



# mKey = random_with_N_digits(4)
#
# client.api.account.messages.create(
#             to="+17735587753",
#             from_="+12242573280",
#             body="Your authetication code generated by Vanguard is " + str(mKey) + "   Please verify this with Vanguard Alexa app")
#

#print(message.sid)