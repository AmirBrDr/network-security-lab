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