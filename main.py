from fastapi import FastAPI, Form, Request, HTTPException, Response
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from dynaconf import settings

app = FastAPI()

MEDIA_URL = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
 
class Message(BaseModel):
    Body: str
    From: str


@app.post("/bot")
async def bot(request: Request):
    form_ = await request.form()
    print(form_) 
    return "hello"


@app.post("/chat")
async def chat(From: str = Form(...), Body: str = Form(...)): 
    response = MessagingResponse()
    msg = response.message(f"{From} | {Body}")
    msg.media(MEDIA_URL)
    return Response(content=str(response), media_type="application/xml")


@app.post("/security/chat")
async def security_chat(request: Request):
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

    form_ = await request.form()
    if not validator.validate(
        str(request.url), dict(form_.items()), request.headers["X-Twilio-Signature"]
    ):
        raise HTTPException(status_code=400, detail="Erro Twilio Signature")

    Body = form_.get("Body")
    From = form_.get("From")

    response = MessagingResponse()
    msg = response.message(f"{From} | {Body}")
    msg.media(MEDIA_URL)
    return Response(content=str(response), media_type="application/xml")
