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


IMAGE_RESIZE_SETTINGS = THUMBNAILS = {
    'METADATA': {
        'BACKEND': 'thumbnails.backends.metadata.DatabaseBackend',
    },
    'STORAGE': {
        'BACKEND': "storages.backends.s3boto3.S3Boto3Storage",
        # You can also use Amazon S3 or any other Django storage backends
    },
    'SIZES': {
        'small': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width':100, 'height': 100},
                {'PATH': 'thumbnails.processors.crop', 'width': 80, 'height': 80}
            ],
            'POST_PROCESSORS': [
                {
                    'PATH': 'thumbnails.post_processors.optimize',
                    'png_command': 'optipng -force -o7 "%(filename)s"',
                    'jpg_command': 'jpegoptim -f --strip-all "%(filename)s"',
                },
            ],
        },
        'medium': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 200, 'height': 200},
                {'PATH': 'thumbnails.processors.flip', 'direction': 'horizontal'}
            ],
        },
        'large': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 500, 'height': 500},
                {'PATH': 'thumbnails.processors.flip', 'direction': 'horizontal'}
            ],
        },
        'watermarked': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 20, 'height': 20},
                # Only supports PNG. File must be of the same size with thumbnail (20 x 20 in this case)
                {'PATH': 'thumbnails.processors.add_watermark', 'watermark_path': 'watermark.png'}
            ],
        }
    }
}