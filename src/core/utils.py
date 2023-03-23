import mixpanel
from .settings import env


mp = mixpanel.Mixpanel(
  env('MIXPANEL_TOKEN'),
  consumer=mixpanel.Consumer(api_host="api-eu.mixpanel.com"),
)