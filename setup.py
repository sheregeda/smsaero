from setuptools import setup, find_packages

setup(
    name = 'smsaero',
    version = '1.0.3',
    description = u'send SMS via smsaero.ru',
    author = 'Nikolay Sheregeda',
    author_email = 'ns.sheregeda@gmail.com',
    url = 'https://github.com/sheregeda/smsaero',
    license = 'MIT',
    packages = ['smsaero'],
    zip_safe = False,
    keywords = ['sms', 'sending'],
    install_requires=['requests >= 2.9.1']
)
