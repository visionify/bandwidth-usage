# Bandwidth Usage Measurement
This repo provides an utility function that we can use to trace the bandwidth usage, memory usage, and CPU usage periodically.

This functionality is useful to monitor system performance in the background, when there is other activities going on. 

# How it works
When we do a `ifconfig` command, we see the following output for an interface:

```bash
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 171.16.255.105  netmask 255.255.255.0  broadcast 172.16.249.255
        inet6 fe80::xxxx:xxxx:xxxx:xxxx  prefixlen 64  scopeid 0x20<link>
        ether xx:xx:xx:xx:xx:xx  txqueuelen 1000  (Ethernet)
        RX packets 431354  bytes 171277574 (171.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 254150  bytes 238681292 (238.6 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

The RX bytes and Tx bytes get incremented each time there is data transfer through that interface. We use this information to calculate difference between two snapshots of the interface in order to calculate bandwidth.

In Python, there is PSUTIL package which can provide us the TX and RX bytes that have gone through the interface. We will make use of this library to calculate bandwidth usage periodically. 

PSUTIL also provides average CPU and MEM usage statistics, so we will make use of those too.  

## How to use
* Clone this repository: 
```
git clone https://github.com/visionify/bandwidth-usage.git
```

* Ensure you have Python3 Installed. If not, you can find it here: https://www.python.org/downloads/

* Install Python dependencies for this repo:
```
pip3 install psutil
```

* Run the program
```bash
$ python3 bandwidth-report.py

Monitor Duration: every 10 seconds.
Interfaces found: lo0, gif0, stf0, en0, en1, en2, en6, bridge0, p2p0, awdl0, llw0, utun0, utun1, utun2, utun3
Monitoring data over ALL interfaces
CPU, Memory and Bandwidth Stats (every 10 seconds)
Last 10 seconds Stats: CPU 7.5%, Mem 57.0%, Download 0.03MB, Upload 0.03MB
Last 10 seconds Stats: CPU 7.8%, Mem 56.5%, Download 0.06MB, Upload 0.05MB
Last 10 seconds Stats: CPU 6.6%, Mem 56.5%, Download 0.55MB, Upload 0.22MB
Last 10 seconds Stats: CPU 10.9%, Mem 57.0%, Download 0.06MB, Upload 0.05MB
Last 10 seconds Stats: CPU 7.6%, Mem 57.1%, Download 0.05MB, Upload 0.04MB
Last 10 seconds Stats: CPU 11.0%, Mem 57.1%, Download 0.03MB, Upload 0.03MB
Last 10 seconds Stats: CPU 10.8%, Mem 57.1%, Download 0.03MB, Upload 0.03MB
...

```

## Summary Report
After the program has completed running, you can find a local JSON file in the current directory that shows the cumulative bandwidth usage over that period of time. 

```json
{
  "last_updated": "2021-05-11-16-44-38",
  "upload_mb": 3.37,
  "download_mb": 49.43
}
```

## Configuration
Tweak the program to your liking.
* If you want to change the program to monitor any single interface, update this variable in the program.
```python
monitor_interface = 'eth0'
```

* If you want to update the bandwidth duration to monitor duration to a larger value, update this parameter. 
```python
monitor_duration_seconds = 10
```

## Feedback
Please submit any issues through the github issues tab. You can also reach me directly at hmurari < at > [visionify.ai](www.visionify.ai). 
