# Bandwidth Usage Measurement
This repo provides an utility function that we can use to trace the bandwidth usage, memory usage, and CPU usage periodically.

This functionality is useful to monitor system performance in the background, when there is other activities going on. Please share your feedback on any suggestions or improvements by contacting me at hmurari <at> visionify <dot> ai. Learn more about what we do at www.visionify.ai

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
Please submit any issues through the github issues tab. You can also reach me directly at hmurari < at > [visionify.ai](www.visionify.ai)
