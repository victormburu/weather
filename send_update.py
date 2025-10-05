from twilio.rest import Client
import os

def send_update(prediction_message, max_messages=1):
    if not hasattr(send_update, "message_count"):
        send_update.message_count = 0
        
    if send_update.message_count >= max_messages:
        print("Maximum message limit reached. No more messages will be sent.")
        return
    send_update.message_count += 1
    
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
    TO_NUMBER = os.getenv("TO_NUMBER")
    
    
    # Initialize Twilio client
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    # Send the message
    msg = client.messages.create(
        from_= TWILIO_NUMBER,
        to = TO_NUMBER,
        body = prediction_message
    )
    
    
    print(f"Message sent with SID: {msg.sid}")
    
    send_update(msg)
    print("Prediction:", msg)
    send_update(f"Weather Update for Nairobi: \n{msg}")