import os
from fastapi import FastAPI, Form, Request, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator 

app = FastAPI() 

@app.post("/hook")
async def chat(From: str = Form(...), Body: str = Form(...)):
   response = MessagingResponse() 
   response.message(f"Hi {From}, you said: {Body}")
   return Response(content=str(response), media_type="application/xml")


@app.post("/security/hook")
async def security_chat(request: Request):
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

    form_ = await request.form() 

    print(form_.items())

    if not validator.validate(
        str(request.url), dict(form_.items()), request.headers["X-Twilio-Signature"]
    ):
        raise HTTPException(status_code=400, detail="Error Twilio Signature")

    Body = form_.get("Body")
    From = form_.get("From")

    response = MessagingResponse()
    response.message(f"Hi {From} | {Body}")
    return Response(content=str(response), media_type="application/xml")
