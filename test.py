from zeep import Client
from zeep.plugins import HistoryPlugin
from lxml import etree

history = HistoryPlugin()
username = 'tavalaei'
password = 'T@val@I'
client = Client('MessagingService.xml', plugins=[history])

with client.settings(force_https=False):
    service = client.create_service(
        '{http://www.adpdigital.com/services/messaging}MessagingServiceSoapBinding',
        'https://10.0.32.43:80/smsservice.asmx')

    result = client.service.changePassword(username, password, 'mJ604998')

    your_pretty_xml = etree.tostring(
        history.last_received["envelope"], encoding="unicode", pretty_print=True)

    f = open("myfile.txt", "w")
    f.write(str(your_pretty_xml))
    f.close()
