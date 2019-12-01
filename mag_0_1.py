from exchangelib import Credentials, Account, Folder, DELEGATE, Configuration
import requests

credentials = Credentials(username = "nlp-test",
                          password = "p1KVJWPDxtRgNBcdA3v3")

config = Configuration(server = 'mail.mpei.ru', credentials = credentials)

account = Account(primary_smtp_address = "nlp.test@mpei.ru",
                  credentials = credentials,
                  autodiscover = False,
                  config = config,
                  access_type = DELEGATE)

for item in account.inbox.all().order_by('-datetime_received')[:10]:
    print(item.subject,
          item.sender,
          item.datetime_received)
