import digitalocean, os

class digiocean:
    def __init__(self, token):
        self.token = token
        self.manager = digitalocean.Manager(token = self.token)
        self.keys = self.manager.get_all_sshkeys()
    def createDroplets(self, maxcount, region):
        count = 0
        while count < maxcount:
            droplet = digitalocean.Droplet(token = self.token, name = 'drop' + str(count), region = region, image = 'ubuntu-14-04-x64', size_slug = '512mb', ssh_keys = self.keys, backups = False)
            droplet.create()
            count = count + 1
    def deleteDroplets(self):
        droplets = self.manager.get_all_droplets()
        for droplet in droplets:
            droplet.destroy()
    def getDroplets(self):
        droplets = self.manager.get_all_droplets()
        for droplet in droplets:
            print(droplet.ip_address)
    def pipeDroplets(self):
        proxylist = []
        startport = int(input('Enter Starting Port : '))
        droplets = self.manager.get_all_droplets()
        for droplet in droplets:
            command = 'ssh -D ' + str(startport) + ' -f -C -q -N -p 22 -o StrictHostKeyChecking=no root@' + droplet.ip_address
            os.system(command)
            proxylist.append('localhost:' + str(startport))
            startport += 1
        print('Proxies Available @ : ' + str(proxylist))

s = digiocean('INSERT DIGI OCEAN KEY HERE')

while True:

    print('1 = Create Droplets')
    print('2 = Delete All Droplets')
    print('3 = Print Droplets Info')
    print('4 = Pipe all Droplets to Local Proxies')
    print('5 = Quit')

    status = int(input('...? : '))

    while status not in [1,2,3,4,5]:
        print('Incorrect Input...')
        print('1 = Create Droplets')
        print('2 = Delete All Droplets')
        print("3 = Print Droplets IP's")
        print('4 = Pipe all Droplets to Local Socks Proxies')
        print('5 = Quit')
        status = int(input('...? : '))

    if status == 1:
        print('Available Regions : nyc1, nyc2, nyc3, tor1, lon1')
        region = input('...? : ')
        while region not in ['nyc1', 'nyc2', 'nyc3', 'tor1', 'lon1']:
            print('Invalid Input...')
            print('Available Regions : nyc1, nyc2, nyc3, tor1, lon1')
            region = input('...? : ')
        s.createDroplets(int(input('How Many Droplets? : ')), region)

    elif status == 2:
        s.deleteDroplets()

    elif status == 3:
        s.getDroplets()

    elif status == 4:
        s.pipeDroplets()

    elif status == 5:
        break
