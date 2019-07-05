from twilio.rest import Client
import twilio

a_sid="AC31ec77255581c3a74b2bf50384e54704"    # Twilio SID number
a_token= "d8dfe5f22590b640189f2a19cf38864e" # Twilio Token number 
to_no= '+919502092349' # mobile number
my_no= '+13144417091'  # Twilio number


client =Client(a_sid, a_token)

f=open('/home/pi/log.txt','r')
my_msg= f.read()
f.close

msg=client.messages.create(to=to_no, from_=my_no, body=my_msg)

print ("your msg has been sent")
