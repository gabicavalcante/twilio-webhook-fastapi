from fastapi import FastAPI, Form, Request, HTTPException, Response
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from dynaconf import settings

app = FastAPI()

media_schema = {
    "god boy": "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
    "not found": "https://images.unsplash.com/photo-1520004434532-668416a08753?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
}

class Media(BaseModel):
    url: str
    tag: str


@app.post("/add/media")
async def add_media(media: Media): 
    print("ok")
    media_schema[media.tag] = media.url
    return {"message": "media added"}


@app.post("/webhook")
async def chat(From: str = Form(...), Body: str = Form(...)): 
    response = MessagingResponse()

    content = Body.lower().strip()
    if media_schema.get(content, None):
        msg = response.message(f"Hi {From} | {Body}")
        msg.media(media_schema.get(content))
    else:
        msg = response.message(f"Hi {From} | this tag was not found")
        msg.media(media_schema.get("not found"))
    return Response(content=str(response), media_type="application/xml")


@app.post("/security/chat")
async def security_chat(request: Request):
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

    form_ = await request.form()
    if not validator.validate(
        str(request.url), dict(form_.items()), request.headers["X-Twilio-Signature"]
    ):
        raise HTTPException(status_code=400, detail="Erro Twilio Signature")

    Body = form_.get("Body").lower().strip()
    From = form_.get("From")

    response = MessagingResponse()
    if media_schema.get(Body, None):
        msg = response.message(f"Hi {From} | {Body}")
        msg.media(media_schema.get(Body))
    else:
        msg = response.message(f"Hi {From} | this tag was not found")
        msg.media(media_schema.get("not found"))
    return Response(content=str(response), media_type="application/xml")
