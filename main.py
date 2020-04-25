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


@app.post("/hook2")
async def security_chat(request: Request):
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

    form_ = await request.form()

    print(request.url)

    if not validator.validate(
        str(request.url), dict(form_.items()), request.headers["X-Twilio-Signature"]
    ):
        raise HTTPException(status_code=400, detail="Error Twilio Signature")

    Body = form_.get("Body")
    From = form_.get("From")

    response = MessagingResponse()
    response.message(f"Hi {From} | {Body}")
    return Response(content=str(response), media_type="application/xml")


@app.post("/hook3")
async def security_chat_header(
    From: str = Form(...), Body: str = Form(...), x_twilio_signature: str = Header(None)
):
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

    if not validator.validate(
        f"{os.environ['API_HOST']}/hook",
        {"From": From, "Body": Body},
        x_twilio_signature,
    ):
        raise HTTPException(status_code=400, detail="Error Twilio Signature")

    response = MessagingResponse()
    response.message(f"Hi {From} | {Body}")
    return Response(content=str(response), media_type="application/xml")
