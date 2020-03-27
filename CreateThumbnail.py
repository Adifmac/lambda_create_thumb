import boto3
import os
import sys, traceback
from urllib.parse import unquote_plus
import uuid
import logging
from PIL import Image

s3_client = boto3.client('s3')


def is_photo_valid(key):
    key_end = key.rsplit('/', 1).pop()
    if key_end.find('bwt_') == 0:
        return False
    elif key_end.find('thumb_') == 0:
        return False
    return True


def get_thumb_name(orig_name):
    orig_name = unquote_plus(orig_name)
    if '/' in orig_name:
        folders = orig_name.rsplit('/', 1)
        key_end = folders.pop()
        return folders[0] + '/thumb_' + key_end
    else:
        return 'thumb_' + orig_name


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((220, 220))
        image.save(resized_path)


def process_image(bucket, key, thumb_key, download_path, upload_path):
    s3_client.download_file(bucket, unquote_plus(key), download_path)
    resize_image(download_path, upload_path)
    s3_client.upload_file(upload_path, bucket, thumb_key, ExtraArgs={'ContentType': 'image/jpeg', 'ACL': 'public-read'})


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if is_photo_valid(key):
            mini_key = key.rsplit('/', 1).pop()
            thumb_key = get_thumb_name(key)
            download_path = '/tmp/{}{}'.format(uuid.uuid4(), mini_key)
            upload_path = '/tmp/resized-{}'.format(mini_key)

            try:
                process_image(bucket, key, thumb_key, download_path, upload_path)
            except Exception as e:
                logging.error(str(e))
                # traceback.print_exc(file=sys.stderr)
            finally:
                # Delete temporary files
                try:
                    os.remove(download_path)
                except OSError:
                    pass

                try:
                    os.remove(upload_path)
                except OSError:
                    pass

