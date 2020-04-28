import os
from fastapi import FastAPI, Form, Request, HTTPException, Response, Header, Path
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

app = FastAPI()


@app.post("/hook")
async def chat(From: str = Form(...), Body: str = Form(...)):
    response = MessagingResponse()
    response.message(f"Hi {From}, you said: {Body}")
    return Response(content=str(response), media_type="application/xml")


@app.post("/security/hook/")
async def security_chat(request: Request, From: str = Form(...), Body: str = Form(...)):
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

    if not validator.validate(
        str(request.url),
        {"From": From, "Body": Body},
        request.headers.get("X-Twilio-Signature", ""),
    ):
        raise HTTPException(status_code=400, detail="Error Twilio Signature")

    response = MessagingResponse()
    response.message(f"Hi {From} | {Body}")
    return Response(content=str(response), media_type="application/xml")
