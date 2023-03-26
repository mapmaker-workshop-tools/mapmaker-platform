import mixpanel
from .settings import env
import qrcode
import os.path
import base64
from io import BytesIO


from django.core.signing import Signer
signer = Signer()


mp = mixpanel.Mixpanel(
  env('MIXPANEL_TOKEN'),
  consumer=mixpanel.Consumer(api_host="api-eu.mixpanel.com"),
)

def qrgenerator(url, workshop, workshop_secret):
  url = str(url)
  buffered = BytesIO()
  workshop = str(workshop)
  img = qrcode.make(url)
  img.save(buffered, format="PNG")
  base64_qrcode = base64.b64encode(buffered.getvalue())
  return str("data:;base64,"+str(base64_qrcode.decode("utf-8")))