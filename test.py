# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
import cv2
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKID7C4LPIVnTvAHIaMKipiKglbBbkeInpPk '  # 替换为用户的 secretId
secret_key = 'Ng4DQjskNp1OVMtDOKVVTNCnFVW1KWWu'  # 替换为用户的 secretKey
region = 'ap-nanjing'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
print()
#response = client.get_object(
    #Bucket='wound-1301658428',
    # Prefix='image',
    # Delimiter='/image',
    #Key='image/weather.jpg'
    # Key='input.jpg'
#)

#file = "image/logo.png"
#response2 = client.upload_file(
    #Bucket='wound-1301658428',
    #LocalFilePath='image/logo.png',  # 本地文件的路径
    #Key='logo.jpg',  # 上传到桶之后的文件名
#)
#print(response['ETag'])

upload_image_file_path = "uploadimage/12333_input.jpg"
print(upload_image_file_path)
client.upload_file(
    Bucket='wound-1301658428',
    LocalFilePath=upload_image_file_path,  # 本地文件的路径
    Key=upload_image_file_path,  # 上传到桶之后的文件名
)

# print(image)
def upload_image(file):
    response1 = client.put_object(
        Bucket='wound-1301658428',
        Body='image/logo.png',
        Key='logo.png',
        EnableMD5=False
    )
#upload_image(file)
# 注意，上传分块的块数最多10000块
# response2 = client.upload_part(
# Bucket='wound-1301658428',
# Key='exampleobject',
# Body=b'b'*1024*1024,
# PartNumber=1,
# UploadId='exampleUploadId'
# )
