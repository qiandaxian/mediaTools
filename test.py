import hashlib
import os

def md5sum(filename):
    """
    用于获取文件的md5值
    :param filename: 文件名
    :return: MD5码
    """
    if not os.path.isfile(filename):  # 如果校验md5的文件不是文件，返回空
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest().upper()


def shasum(filename):
    """
    用于获取文件的md5值
    :param filename: 文件名
    :return: MD5码
    """
    if not os.path.isfile(filename):  # 如果校验md5的文件不是文件，返回空
        return
    myhash = hashlib.sha1()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest().upper()



f = md5sum("/Users/qiandaxian/Downloads/1.4.0.apk")
print(f)
f2 = shasum("/Users/qiandaxian/Downloads/1.4.0.apk")
print(f2)



