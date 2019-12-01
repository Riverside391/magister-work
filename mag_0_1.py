from exchangelib import Credentials, Account, Folder, DELEGATE, Configuration
import requests

credentials = Credentials(username = "nlp-test",#имя пользователя в формате domain//username
                          password = "p1KVJWPDxtRgNBcdA3v3")#pass

config = Configuration(server = 'mail.mpei.ru',#сервер почты
                       credentials = credentials)

account = Account(primary_smtp_address = "nlp.test@mpei.ru",#почтовый адрес
                  credentials = credentials,
                  autodiscover = False,
                  config = config,
                  access_type = DELEGATE)

for item in account.inbox.all().order_by('-datetime_received')[:10]:
    print(item.subject,
          item.sender,
          item.datetime_received)
