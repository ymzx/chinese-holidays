from setuptools import setup

setup(
    name='chinese-holidays',  # 需要打包的名字,即本模块要发布的名字
    version='v1.0',  # 版本
    description='Calculate Chinese holidays, traditional festivals, and rest days for a specified year.',  # 简要描述
    py_modules=['mySelfSum'],   # 需要打包的模块
    author='JWDuan',  # 作者名
    author_email='494056012@qq.com',   # 作者邮件
    url='https://github.com/vfrtgb158/email',  # 项目地址,一般是代码托管的网站
    requires=['requests', 'json', 'datetime', 'os'],  # 依赖包,如果没有,可以不要
    license='MIT'
)
