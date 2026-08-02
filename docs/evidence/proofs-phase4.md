 etu@monitoring  ~  for host in 10.99.0.1 10.99.0.2 10.99.0.3 10.99.0.66; do
    ping -c 2 "$host"
done

curl -s http://10.99.0.66:3100/ready
curl -s http://10.99.0.66:9090/-/ready
PING 10.99.0.1 (10.99.0.1) 56(84) bytes of data.
64 bytes from 10.99.0.1: icmp_seq=1 ttl=64 time=0.839 ms
64 bytes from 10.99.0.1: icmp_seq=2 ttl=64 time=0.934 ms

--- 10.99.0.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 0.839/0.886/0.934/0.047 ms
PING 10.99.0.2 (10.99.0.2) 56(84) bytes of data.
64 bytes from 10.99.0.2: icmp_seq=1 ttl=64 time=3.54 ms
64 bytes from 10.99.0.2: icmp_seq=2 ttl=64 time=0.888 ms

--- 10.99.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.888/2.214/3.541/1.326 ms
PING 10.99.0.3 (10.99.0.3) 56(84) bytes of data.
64 bytes from 10.99.0.3: icmp_seq=1 ttl=64 time=3.45 ms
64 bytes from 10.99.0.3: icmp_seq=2 ttl=64 time=0.978 ms

--- 10.99.0.3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.978/2.213/3.449/1.235 ms
PING 10.99.0.66 (10.99.0.66) 56(84) bytes of data.
64 bytes from 10.99.0.66: icmp_seq=1 ttl=64 time=0.899 ms
64 bytes from 10.99.0.66: icmp_seq=2 ttl=64 time=0.722 ms

--- 10.99.0.66 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.722/0.810/0.899/0.088 ms
ready
Prometheus Server is Ready.
 etu@monitoring  ~  


 