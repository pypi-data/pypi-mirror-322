import base64


def encode_message(text):
    text = str(text)
    message_bytes = text.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode("ascii")

