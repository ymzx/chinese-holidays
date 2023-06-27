from setuptools import setup, find_packages

setup(
    name='py-chinese-holidays',
    version='v1.1.1',
    description='Calculate Chinese holidays, traditional festivals, and rest days for a specified year.',  # 简要描述
    # py_modules=['chinese_holidays'],
    author='JWDuan',
    author_email='494056012@qq.com',
    url='https://github.com/ymzx/chinese-holidays',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    requires=['requests', 'json', 'datetime', 'os'],
    license='MIT'
)
