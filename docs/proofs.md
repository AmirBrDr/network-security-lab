 amirmahdighasemi@bob  ~/vm/network-security-lab  switch-conf.py -a switch.yaml
----------------------------------------
Switch dsw-host exists
>> Port tap62 vlan_mode is already set to trunk
>> Port tap62 trunks are already set to [99, 360, 440, 441]
>> Port tap63 vlan_mode is already set to trunk
>> Port tap63 trunks are already set to [28, 99, 440, 442]
>> Port tap64 vlan_mode is already set to trunk
>> Port tap64 trunks are already set to [28, 99, 441, 442]
>> Port tap65 vlan_mode is already set to access
>> Port tap65 tag is already set to 99
>> Port tap66 vlan_mode is already set to access
>> Port tap66 tag is already set to 99
----------------------------------------
 amirmahdighasemi@bob  ~/vm/network-security-lab  lab-startup.py vms-startup.yaml 
R1.qcow2 already exists!
Creating R1.qcow2_OVMF_VARS.fd file...
Starting R1...
~> Virtual machine filename   : R1.qcow2
~> RAM size                   : 4096
~> SPICE VDI port number      : 5962
~> telnet console port number : 2362
~> MAC address                : b8:ad:ca:fe:00:3e
~> Switch port interface      : tap62, trunk mode
~> IPv6 LL address            : fe80::baad:caff:fefe:3e%dsw-host
R1 started!
R2.qcow2 already exists!
Creating R2.qcow2_OVMF_VARS.fd file...
Starting R2...
~> Virtual machine filename   : R2.qcow2
~> RAM size                   : 4096
~> SPICE VDI port number      : 5963
~> telnet console port number : 2363
~> MAC address                : b8:ad:ca:fe:00:3f
~> Switch port interface      : tap63, trunk mode
~> IPv6 LL address            : fe80::baad:caff:fefe:3f%dsw-host
R2 started!
R3.qcow2 already exists!
Creating R3.qcow2_OVMF_VARS.fd file...
Starting R3...
~> Virtual machine filename   : R3.qcow2
~> RAM size                   : 4096
~> SPICE VDI port number      : 5964
~> telnet console port number : 2364
~> MAC address                : b8:ad:ca:fe:00:40
~> Switch port interface      : tap64, trunk mode
~> IPv6 LL address            : fe80::baad:caff:fefe:40%dsw-host
R3 started!
monitoring.qcow2 already exists!
Creating monitoring.qcow2_OVMF_VARS.fd file...
Starting monitoring...
~> Virtual machine filename   : monitoring.qcow2
~> RAM size                   : 12288
~> SPICE VDI port number      : 5965
~> telnet console port number : 2365
~> MAC address                : b8:ad:ca:fe:00:41
~> Switch port interface      : tap65, access mode
~> IPv6 LL address            : fe80::baad:caff:fefe:41%vlan99
monitoring started!
management.qcow2 already exists!
Creating management.qcow2_OVMF_VARS.fd file...
Starting management...
~> Virtual machine filename   : management.qcow2
~> RAM size                   : 12288
~> SPICE VDI port number      : 5966
~> telnet console port number : 2366
~> MAC address                : b8:ad:ca:fe:00:42
~> Switch port interface      : tap66, access mode
~> IPv6 LL address            : fe80::baad:caff:fefe:42%vlan99
management started!
 amirmahdighasemi@bob  ~/vm/network-security-lab  

 etu@R1:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
etu@R1:~$ 

etu@R2:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
etu@R2:~$ 

etu@R3:~$ sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
etu@R3:~$ 

sudo netplsudo netplan status
     Online state: online
    DNS Addresses: 127.0.0.53 (stub)
       DNS Search: .

●  1: lo ethernet UNKNOWN/UP (unmanaged)
      MAC Address: 00:00:00:00:00:00
        Addresses: 127.0.0.1/8
                   ::1/128

●  2: enp0s1 ethernet UP (networkd: enp0s1)
      MAC Address: b8:ad:ca:fe:00:3e (Red Hat, Inc.)
        Addresses: fe80::baad:caff:fefe:3e/64 (link)
    DNS Addresses: 172.16.0.2
                   2001:678:3fc:3::2
           Routes: fe80::/64 metric 256

●  3: enp0s1.360 vlan UP (networkd: enp0s1.360)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 192.168.104.130/29
                   2001:678:3fc:168::82/64 (ra)
                   2001:678:3fc:168:baad:caff:fefe:3e/64 (dynamic, ra)
                   fe80::baad:caff:fefe:3e/64 (link)
    DNS Addresses: 2001:678:3fc:3::2
           Routes: default via 192.168.104.129 (static)
                   192.168.104.128/29 from 192.168.104.130 (link)
                   2001:678:3fc:168::/64 metric 256
                   2001:678:3fc:168::/64 metric 512 (ra)
                   fe80::/64 metric 256
                   default via fe80:168::1 metric 512 (ra)
                   default via fe80::168:1 metric 1024 (static)

●  4: enp0s1.440 vlan UP (networkd: enp0s1.440)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 10.44.0.1/29
                   fe80::baad:caff:fefe:3e/64 (link)
                   fe80::1b8:1/64 (link)
           Routes: 10.44.0.0/29 from 10.44.0.1 (link)
                   fe80::/64 metric 256

●  5: enp0s1.99 vlan UP (networkd: enp0s1.99)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 10.99.0.1/24
                   fd14:ca46:3864:99::1/64
                   fe80::baad:caff:fefe:3e/64 (link)
           Routes: 10.99.0.0/24 from 10.99.0.1 (link)
                   fd14:ca46:3864:99::/64 metric 256
                   fe80::/64 metric 256

●  6: enp0s1.441 vlan UP (networkd: enp0s1.441)
      MAC Address: b8:ad:ca:fe:00:3e
        Addresses: 10.44.1.1/29
                   fe80::baad:caff:fefe:3e/64 (link)
                   fe80::1b9:1/64 (link)
           Routes: 10.44.1.0/29 from 10.44.1.1 (link)
                   fe80::/64 metric 256