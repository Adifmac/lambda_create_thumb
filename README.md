# lambda_create_thumb
lambda function for creating thumbnails in the SAME bucket
The thumbnail is created NEXT to the original, a prefix 'thumb_' is added to the file name 
(not key, excluding "folders").
ex: bucket/folder1/folder2/amazing_photo.jpg => bucket/folder1/folder2/thumb_amazing_photo.jpg

