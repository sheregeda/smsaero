# smsaero
[![PyPI version](https://img.shields.io/pypi/v/smsaero.svg)](https://pypi.python.org/pypi/smsaero) [![Build Status](https://travis-ci.org/sheregeda/smsaero.svg?branch=master)](https://travis-ci.org/sheregeda/smsaero) [![Coverage Status](https://coveralls.io/repos/github/sheregeda/smsaero/badge.svg?branch=master)](https://coveralls.io/github/sheregeda/smsaero?branch=master)

Пакет для работы с [SMSAero](http://smsaero.ru/) API, основанный на библиотеке [requests](http://docs.python-requests.org/en/master/).

## Документация
Оригинальная документация SMSAero API доступна по [ссылке](http://smsaero.ru/api/description) на официальном сайте.

## Использование
```python
In [1]: from smsaero import SmsAero

# Быстое создание объекта, будут использованы параметры signature='NEWS', digital=0 и type_send=2
In [2]: api = SmsAero(u'login', u'password')

# Расширенное создание объекта
In [3]: api = SmsAero(u'login', u'password', url_gate=u'http://gate.smsaero.ru/',
                      signature=u'SOME', digital=1, type_send=4)

# Отправка сообщения
In [4]: api.send(u'8123456789', u'text message')
Out[4]: {u'id': 33475057, u'result': u'accepted'}

# Описание канала отправки и подпись
In [5]: api.send(u'8123456789', u'text message', signature=u'SOME', digital=0, type_send=2)
Out[5]: {u'id': 33475057, u'result': u'accepted'}

# Отложенная отправка сообщения
In [6]: api.send(u'8123456789', u'text message', date=datetime.now()+timedelta(1))
Out[6]: {u'id': 33475057, u'result': u'accepted'}

# Отправка сообщения для группы
In [7]: api.sendtogroup('group_name', 'text message')
Out[7]: {u'id': 321, u'result': u'accepted'}

# Проверка статуса сообщения
In [8]: api.status(33475057)
Out[8]: {u'id': 33475057, u'result': u'delivery success'}

# Статусы сообщений для рассылки по группе
In [9]: api.checksending(321)
Out[9]:
{u'reason': {u'33460579': u'smsc reject', u'33460580': u'delivery success'},
 u'result': u'accepted'}

# Запрос баланса
In [10]: api.balance()
Out[10]: {u'balance': u'48.20'}

# Запрос тарифа
In [11]: api.checktarif()
Out[11]:
{u'reason': {u'Digital channel': u'0.45', u'Direct channel': u'1.80'},
 u'result': u'accepted'}

# Список доступных подписей
In [12]: api.senders()
Out[12]: [u'NEWS', u'awesome']

# Запрос новой подписи отправителя
In [13]: api.sign(u'awesome')
Out[13]: {u'accepted': u'pending'}

# Список всех существующих групп
In [14]: api.checkgroup()
Out[14]: {u'reason': [u'Личные контакты'], u'result': u'accepted '}

# Добавить новую группу
In [15]: api.addgroup(u'test')
Out[15]: {u'reason': u'Group created', u'result': u'accepted'}

# Удалить группу
In [16]: api.delgroup(u'test')
Out[16]: {u'reason': u'Group delete', u'result': u'accepted'}

# Добавить абонента в определенную группу
In [17]: api.addphone(u'8123456789', u'test')
Out[17]: {u'reason': u'Number added to test group', u'result': u'accepted'}

# Удалить абонента из определенной группы
In [18]: api.delphone(u'8123456789', u'test')
Out[18]: {u'reason': u'Phone delete in test group', u'result': u'accepted'}

# Добавить номер в черный список
In [19]: api.addblacklist(u'8123456789')
Out[19]: {u'reason': u'Phone added to your blacklist', u'result': u'accepted'}
```
## Исключения
Библиотека может выбросить исключения:
* SmsAeroError(Exception)
* SmsAeroHTTPError(SmsAeroError)
