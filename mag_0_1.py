from configparser import ConfigParser
import requests
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from exchangelib.version import EXCHANGE_2010_SP2
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, OAuth2Credentials, FaultTolerance, Configuration, NTLM, GSSAPI, SSPI, OAUTH2, Build, Version
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def read_data(arg, data, section):
    settings = ConfigParser()
    settings.read(data)
    result = settings[section][arg]
    return result

def write_log(file, string):
    f = open(file, 'a')
    f.write(str(string) + '\n')

def connect_autodison(server, email, username, password):
    creds = Credentials(email, password = password)
    return Account(primary_smtp_address = email, credentials = creds, autodiscover = True)
                  
def connect(server, email, username, password):
    creds = Credentials(username = username, password = password)
    config = Configuration(server = server, credentials = creds)
    return Account(primary_smtp_address = email, autodiscover = False, config = config, access_type = DELEGATE)

def smtp_connect(server, email, username, password):
    creds = Credentials(username = username, password = password)
    config = Configuration(credentials = creds, server = server)
    version = Version()
    return Account(primary_smtp_address=email, config = config,
                   credentials=creds, autodiscover=False, access_type=DELEGATE)

def connect_discoff_ntlm(server, email, username, password):
    creds = Credentials(username = username, password = password)
    config = Configuration(server = server, credentials = creds, auth_type = NTLM)
    return Account(primary_smtp_address = email, autodiscover = False, config = config, access_type = DELEGATE)

if __name__ == "__main__":
    ua = UserAgent()
    settings = 'data.ini'
    section = 'USER_DATA'
    file_name = 'log.txt'
    f = open('log.txt', 'w')
    print('Start of program')
    write_log(file_name, 'Start of program')
    mail = read_data('mail', settings, section)
    username = read_data('username', settings, section)
    password = read_data('password', settings, section)
    null_domain = ''
    domain1 = read_data('domain1', settings, section)
    domain2 = read_data('domain2', settings, section)
    server1 = read_data('server1', settings, section)
    server2 = read_data('server2', settings, section)
    server3 = read_data('server3', settings, section)

    tests_domain = [null_domain, domain1+'\\', domain2+'\\']
    tests_server = [server1, server2, server3]

    for domain in tests_domain:
        for server in tests_server:
            print('DEBUG test domain: ' + domain + ', server: ' + server)
            write_log(file_name, 'DEBUG test domain: ' + domain + ', server: ' + server)

            print('------SMTP Connection test')
            write_log(file_name, '------SMTP Connection test')
            try:
                account = smtp_connect(server, mail, domain+username, password)
                #print(account.root.tree())
                #write_log(file_name, account.root.tree())
                for item in account.inbox.all().order_by('-datetime_received')[:2]:
                    print(item.subject, item.sender)
                    write_log(file_name, item.subject + item.sender)
            except Exception as error:
                print('FAIL: ', error)
                write_log(file_name, error)
            
            '''print('------Autodiscovery test')
            write_log(file_name, '------Autodiscovery test')      
            try:
                account = connect_autodison(server, mail, domain+username, password)
                print(account.root.tree())
                write_log(file_name, account.root.tree())
                for item in account.inbox.all().order_by('-datetime_received')[:2]:
                    print(item.subject, item.sender, item.datetime_received)
                    write_log(file_name, item.subject + item.sender + item.datetime_received)
            except Exception as error:
                print('! FAIL: ', error)
                write_log(file_name, error)
                pass'''

            print('------Connection test')
            write_log(file_name, '------Connection test')
            try:
                account = connect(server, mail, domain+username, password)
                ews_url = account.protocol.service_endpoint
                ews_auth_type = account.protocol.auth_type
                version = account.version
                primary_smtp_address = account.primary_smtp_address
                config = Configuration(service_endpoint = ews_url, credentials = credentials, auth_type = ews_auth_type, version=version)
                account = Account(primary_smtp_address = primary_smtp_address, config = config, autodiscover = False, access_type = DELEGATE)            
                print(account.root.tree())
                write_log(file_name, account.root.tree())
                for item in account.inbox.all().order_by('-datetime_received')[:2]:
                    print(item.subject, item.sender, item.datetime_received)
                    write_log(file_name, item.subject + item.sender + item.datetime_received)
            except Exception as error:
                print('! FAIL: ', error)
                write_log(file_name, error)
                pass

            '''print('------NTLM test')
            write_log(file_name, '------NTLM test')
            try:     
                account = connect_discoff_ntlm(server, mail, domain+username, password)
                ews_url = account.protocol.service_endpoint
                ews_auth_type = account.protocol.auth_type
                primary_smtp_address = account.primary_smtp_address
                config = Configuration(service_endpoint = ews_url, credentials = credentials, auth_type = ews_auth_type)
                account = Account(primary_smtp_address = primary_smtp_address, config = config, autodiscover = False, access_type = DELEGATE)
                print(account.root.tree())
                write_log(file_name, account.root.tree())
                for item in account.inbox.all().order_by('-datetime_received')[:2]:
                    print(item.subject, item.sender, item.datetime_received)
                    write_log(file_name, item.subject + item.sender + item.datetime_received)
            except Exception as error:
                print('! FAIL: ', error)
                write_log(file_name, error)'''

    from exchangelib.autodiscover import _autodiscover_cache
    _autodiscover_cache.clear()
    f.close()
    print('End of program')
    write_log(file_name, 'End of program')
