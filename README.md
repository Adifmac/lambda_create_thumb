# lambda_create_thumb
lambda function for creating resized images thumbnails in the SAME s3 bucket. 

The images are created NEXT to the original, a prefix is added to the file name 
(not key, excluding "folders"). 

Resized sizes and prefix:

thumb = 200x200

m5m = 1100x1100

m4m = 900x900

m3m = 700x700

m2m = 500x500

m1m = 300x300


<!> All resized images are added to the same bucket as the original image.
ex: `bucket/folder1/folder2/amazing_photo.jpg` => `bucket/folder1/folder2/thumb_amazing_photo.jpg`

Using https://github.com/jamesacampbell/iptcinfo3 for IPTC processing.

Using pillow for image processing - how to create a layer for aws lambda: https://towardsdatascience.com/python-packages-in-aws-lambda-made-easy-8fbc78520e30
