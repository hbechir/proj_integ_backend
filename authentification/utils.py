from twilio.rest import Client
import random
import string

def send_code_to_phone(phone_number,code):
    account_sid = 'ACd692ffb54e8f64b9e0330aa2ff254d63'
    auth_token = 'ec00d48c169ddcd02d69b8225d37cde2'
    client = Client(account_sid, auth_token)
    
    # message = client.messages.create(from_='+14243561778',body=code,to=phone_number)    
    message = client.messages.create(from_='+14243561778',body=code,to='+21694813197')



def generate_verification_code():
    # generate a code of 4 digits
    return ''.join(random.choices(string.digits, k=4))