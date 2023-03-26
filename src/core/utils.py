import mixpanel
from .settings import env

from django.core.signing import Signer
signer = Signer()


mp = mixpanel.Mixpanel(
  env('MIXPANEL_TOKEN'),
  consumer=mixpanel.Consumer(api_host="api-eu.mixpanel.com"),
)