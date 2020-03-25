from fastapi import FastAPI, Form, Request, HTTPException
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

app = FastAPI()


def bot_reply(text: str) -> str:
    return "Thank you, we have received your message"


class Message(BaseModel):
    sender: str
    message: str


@app.post("/chat")
async def chat(message: Message):
    response = bot_reply(message.sender, message.message)
    return response


@app.post("/bot")
async def bot(From: str = Form(...), Body: str = Form(...)):
    resp = MessagingResponse()
    msg = resp.message()

    incoming_msg = Body.strip().lower()

    response = bot_reply(incoming_msg)
    msg.body(response)
    return str(msg)


@app.post("/security/bot")
async def security_bot(request: Request):
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

    form_ = await request.form()
    if not validator.validate(
        str(request.url), dict(form_.items()), request.headers["X-Twilio-Signature"]
    ):
        raise HTTPException(status_code=400, detail="Erro Twilio Signature")

    Body = form_.get("Body")

    resp = MessagingResponse()
    msg = resp.message()

    incoming_msg = Body.strip().lower()

    response = bot_reply(incoming_msg)
    msg.body(response)
    return str(msg)
