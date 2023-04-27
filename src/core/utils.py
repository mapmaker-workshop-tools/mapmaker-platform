import base64
from io import BytesIO

import mixpanel
import qrcode
from django.core.signing import TimestampSigner

from .settings import env

signer = TimestampSigner()


mp = mixpanel.Mixpanel(
  env("MIXPANEL_TOKEN"),
  consumer=mixpanel.Consumer(api_host="api-eu.mixpanel.com"),
)

def qrgenerator(url, workshop_secret):
  url = str(url)
  buffered = BytesIO()
  img = qrcode.make(url)
  img.save(buffered)
  base64_qrcode = base64.b64encode(buffered.getvalue())
  return str("data:;base64,"+str(base64_qrcode.decode("utf-8")))
