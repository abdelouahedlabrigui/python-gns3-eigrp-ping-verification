from netmiko import ConnectHandler

def connectionFunction(host, device, passwd, secret, port):
    cisco_device = {
        'device_type': 'cisco_ios_telnet',
        'host': str(host),
        'username': str(device),
        'password': str(passwd),
        'port': str(port),
        'secret': str(secret),
        'verbose': True
    }
    return cisco_device

def configureLoopBackAddresses(device, hostPortion, port):
    connection = ConnectHandler(**connectionFunction('127.0.0.1', device, "", "", port))
    connection.enable()
    command_loopback = [
        f'interface loopback 1', f'ip address 192.168.10.{str(hostPortion)} 255.255.255.255'
    ]
    connection.send_config_set(command_loopback)
    connection.disconnect()

def configureLoopBack():
    routers = ['R1', 'R2', 'R3', 'R4']
    for i, j in zip(range(4), list(routers)):
        configureLoopBackAddresses(str(j), str(i+1), f'{int(500)}{int(i)}')

# configureLoopBack()

def configureFastEthernetAddresses(device, hostPortion, port):
    connection = ConnectHandler(**connectionFunction('127.0.0.1', device, "", "", port))
    connection.enable()
    routers = ['R1', 'R2', 'R3', 'R4']
    for i, j in zip(range(4), list(routers)):
        command = [
            f'interface fastEthernet 0/0', 
            f'ip address 192.168.137.{str(hostPortion)} 255.255.255.0'
        ]
    connection.send_config_set(command)
    connection.disconnect()

def  configFastEthernet():
    routers = ['R1', 'R2', 'R3', 'R4']
    for i, j in zip(range(4), list(routers)):
        configureFastEthernetAddresses(str(j), str(i+1), f'{int(500)}{int(i)}')

# configFastEthernet()

def showIpIntBrief(host, device, passwd, secret, port):
    connection = ConnectHandler(**connectionFunction('127.0.0.1', device, "", "", port))
    connection.enable()
    output = connection.send_command("show ip int bri | ex ass")
    print(output)
    connection.disconnect()
print('This is router one')
print('-------------------------------------------')
showIpIntBrief('127.0.0.1', 'R1', '', '', '5000')
print('This is router two')
print('-------------------------------------------')
showIpIntBrief('127.0.0.1', 'R2', '', '', '5001')
print('This is router three')
print('-------------------------------------------')
showIpIntBrief('127.0.0.1', 'R3', '', '', '5002')
print('This is router four')
print('-------------------------------------------')
showIpIntBrief('127.0.0.1', 'R4', '', '', '5003')
