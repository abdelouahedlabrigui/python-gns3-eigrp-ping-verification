# import _pickle as cPickle
import json 
from netmiko import Netmiko
from netmiko import ConnectHandler
import pandas as pd

devices = ['ordinateur1', 'Router1', 'Router2', 'ordinateur2']
ports = [5000, 5001, 5002, 5003]
# I am going to have a high recursive algorithm.
networks = ['10.1.1.0', '10.1.2.0', '10.1.3.0']
interface = ['f0/0', 'f2/0']

def ipaddressing(devicesList,portsList):
    #allocate ip addresses to devices
    for device,port in zip(list(devicesList), list(portsList)):
        cisco_device = {
            'device_type':'cisco_ios_telnet',
            'host':'127.0.0.1',
            'username':str(device),
            'password':'',
            'port':str(port),
            'secret':'',
            'verbose':True
        }
        with open(f'{device}.txt', 'w') as file:
            file.write(str(json.dumps(str(cisco_device))))
        # f.write(cisco_device)
# ipaddressing(devices,ports)
def confip(device,port):
    cisco_device = {
        'device_type':'cisco_ios_telnet',
        'host':'127.0.0.1',
        'username':str(device),
        'password':'',
        'port':str(port),
        'secret':'',
        'verbose':True
    }
    return cisco_device
def allocateIps():
    for d,p in zip(list(devices), list(ports)):
        if d == 'ordinateur1':
            cisco_device = confip(d,p)
            # print(cisco_device)
            connection = ConnectHandler(**cisco_device)
            connection.enable()
            df = pd.read_csv('ordi1.txt')
            connection.send_config_set(list(df.ipconf))
            print(connection.find_prompt())
            print(connection.send_command('show ip interface brief\n'))
        if d == 'Router1':
            cisco_device = confip(d,p)
            # print(cisco_device)
            connection = ConnectHandler(**cisco_device)
            connection.enable()
            df = pd.read_csv('Router1.txt')
            connection.send_config_set(list(df.ipconf))
            print(connection.find_prompt())
            print(connection.send_command('show ip interface brief\n'))
        if d == 'Router2':
            cisco_device = confip(d,p)
            # print(cisco_device)
            connection = ConnectHandler(**cisco_device)
            connection.enable()
            df = pd.read_csv('Router2.txt')
            connection.send_config_set(list(df.ipconf))
            print(connection.find_prompt())
            print(connection.send_command('show ip interface brief\n'))
        if d == 'ordinateur2':
            cisco_device = confip(d,p)
            # print(cisco_device)
            connection = ConnectHandler(**cisco_device)
            connection.enable()
            df = pd.read_csv('ordi2.txt')
            connection.send_config_set(list(df.ipconf))
            print(connection.find_prompt())
            print(connection.send_command('show ip interface brief\n'))
        
# allocateIps()
def route(device,port):
    connection = Netmiko(
        device_type='cisco_ios_telnet',
        host='127.0.0.1',
        username=str(device),
        password='',
        port=str(port),
        secret='',
        verbose=True
    )
    # output = connection.send_command('show ip route')
    output = connection.send_command('show run | include route')

    print(output)
    connection.disconnect()

# route('ordinateur1','5000')
# route('Router1','5001')
# route('Router2','5002')
# route('ordinateur2','5003')
def traceRoute(ip,device,port):
    #trace if you can ping to machine
    connection = Netmiko(
        device_type='cisco_ios_telnet',
        host='127.0.0.1',
        username=str(device),
        password='',
        port=str(port),
        secret='',
        verbose=True
    )
    connection.send_config_set('conf terminal')
    connection.send_config_set('no ip domain loopkup')
    connection.send_config_set('end')
    output = connection.send_command('traceroute ' + str(ip))
    with open('traceroute.txt', 'w') as target:
        target.write(str(output))
    print(output)
    connection.disconnect()

# traceRoute('10.1.3.2','ordinateur1','5000')

def showIpIntBrief(device,port):
    connection = Netmiko(
        device_type='cisco_ios_telnet',
        host='127.0.0.1',
        username=str(device),
        password='',
        port=str(port),
        secret='',
        verbose=True
    )
    output = connection.send_command('show ip int brief')
    print(output)
    connection.disconnect()

# showIpIntBrief('Router1','5001')

def ping(ip,device,port):
    connection = Netmiko(
        device_type='cisco_ios_telnet',
        host='127.0.0.1',
        username=str(device),
        password='',
        port=str(port),
        secret='',
        verbose=True
    )
    output = connection.send_command('ping ' + str(ip))
    print(output)
    connection.disconnect()

# ping('10.1.2.2', 'Router1', '5001')

def eigrp_2net(net1,net2,dev,port):
    
    cisco_device = {
        'device_type':'cisco_ios_telnet',
        'host':'127.0.0.1',
        'username':str(dev),
        'password':'',
        'port':str(port),
        'secret':'',
        'verbose':True
    }
    
    connection = ConnectHandler(**cisco_device)
    connection.enable()
    commands = [
        'conf terminal',
        'router eigrp 1',
        'network ' + str(net1),
        'network ' + str(net2),
        'exit',
        'end',
        'show run',
    ]
    connection.send_config_set(list(commands))
    connection.disconnect()

def eigrp_1net(net1,dev,port):
    cisco_device = {
        'device_type':'cisco_ios_telnet',
        'host':'127.0.0.1',
        'username':str(dev),
        'password':'',
        'port':str(port),
        'secret':'',
        'verbose':True
    }
    connection = ConnectHandler(**cisco_device)
    connection.enable()
    commands = [
        'conf terminal',
        'router eigrp 1',
        'network ' + str(net1),
        'exit',
        'end',
        'show run',
    ]
    connection.send_config_set(list(commands))
    connection.disconnect()

def applyEigrp(dev,port):
    for d,p in zip(list(dev), list(port)):
        if d == 'Router1':
            eigrp_2net('10.0.0.0','11.0.0.0',d,p)
        elif d == 'Router2':
            eigrp_2net('11.0.0.0','12.0.0.0',d,p)
        elif d == 'ordinateur1':
            eigrp_1net('10.0.0.0',d,p)
        elif d == 'ordinateur2':
            eigrp_1net('12.0.0.0',d,p)

# applyEigrp(devices,ports)

