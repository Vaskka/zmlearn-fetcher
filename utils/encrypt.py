from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


class RSAUtil:
    """
    RSA加密
    Key长度2048
    """
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    import base64

    @staticmethod
    def _handle_pub_key(key):
        """
        处理公钥
        公钥格式pem，处理成以-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾的格式
        :param key:pem格式的公钥，无-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾
        :return:
        """
        start = '-----BEGIN PUBLIC KEY-----\n'
        end = '-----END PUBLIC KEY-----'
        result = ''
        # 分割key，每64位长度换一行
        divide = int(len(key) / 64)
        divide = divide if (divide > 0) else divide + 1
        line = divide if (len(key) % 64 == 0) else divide + 1
        for i in range(line):
            result += key[i * 64:(i + 1) * 64] + '\n'
        result = start + result + end
        return result

    @staticmethod
    def encrypt(key, content):
        """
        ras 加密[公钥加密]
        :param key: 无BEGIN PUBLIC KEY头END PUBLIC KEY尾的pem格式key
        :param content:待加密内容
        :return:
        """
        pub_key = RSAUtil._handle_pub_key(key)
        pub = RSA.import_key(pub_key)
        cipher = PKCS1_v1_5.new(pub)
        encrypt_bytes = cipher.encrypt(content.encode(encoding='utf-8'))
        result = base64.b64encode(encrypt_bytes)
        result = str(result, encoding='utf-8')
        return result

    pass
