from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

try:
    check_signature(token, signature, timestamp, nonce)
except InvalidSignatureException:
    # 处理异常情况或忽略