import xml.etree.ElementTree as ET


class XMLParser(object):
    """docstring for XMLParser"""
    def __init__(self, filename):
        super(XMLParser, self).__init__()
        self.file = filename

    def parseUsers(self):
        tree = ET.parse(self.file)
        root = tree.getroot()
        sublist = []
        tempuserlist = []
        subs = root.findall('subscribers')
        for user in subs[0].findall('user'):
            userID = int(user.find('userID').text)
            RFID = int(user.find('RFID').text)
            lastname = user.find('lastname').text
            firstname = user.find('firstname').text
            password = int(user.find('password').text)
            phone = int(user.find('phone').text)

            address = user.find("address")

            city = address.find('city').text
            cp = int(address.find('cp').text)
            street = address.find('street').text
            number = int(address.find('number').text)

            subscribeDate = user.find('subscribeDate').text
            expiryDate = user.find('expiryDate').text
            card = int(user.find('card').text)

            sublist.append((userID, RFID, lastname, firstname, password, phone, city, cp, street, number, subscribeDate, expiryDate, card))

        temps = root.findall('temporaryUsers')
        for user in temps[0].findall('user'):
            userID = int(user.find('userID').text)
            password = int(user.find('password').text)
            expiryDate = user.find('expiryDate').text
            card = int(user.find('card').text)
            tempuserlist.append((userID, password, expiryDate, card))

        return sublist, tempuserlist


def main():
    parser = XMLParser('../data/users.xml')
    sublist, tempuserlist = parser.parseUsers()
    print (tempuserlist)

if __name__ == '__main__':
    main()
