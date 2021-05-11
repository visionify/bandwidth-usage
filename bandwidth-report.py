import time
import threading
from datetime import datetime
import psutil
import json

# Feel free to update these values to suit your needs
monitor_interface = 'eth0'
monitor_duration_seconds = 10


class Stats(object):
    def __init__(self):
        # Bandwidth report file.
        self.bw_report_file = 'bandwidth-report.json'

        # Thread details
        self._thread = None
        self._thread_stop = threading.Event()

        # Initial network counters
        self.if_name = None

        try:
            ifaces = psutil.net_io_counters(pernic=True)
            iface_names = ', '.join(ifaces.keys())
            print('Interfaces found: {}'.format(iface_names))

            for iface in ifaces.keys():
                if monitor_interface == iface:
                    print('Monitoring Interface: {}'.format(monitor_interface))
                    self.if_name = iface
                    break
                if self.if_name is not None:
                    break

            if self.if_name is None:
                print('Monitoring data over ALL interfaces')
            else:
                print('Monitoring data over single inteface: {}'.format(self.if_name))

        except:
            print('Unable to find monitor interface. Using ALL interfaces data for bandwidht calculation')

        if self.if_name is not None:
            self.start_bytes_sent = psutil.net_io_counters(pernic=True)[self.if_name].bytes_sent
            self.start_bytes_recv = psutil.net_io_counters(pernic=True)[self.if_name].bytes_recv
        else:
            self.start_bytes_sent = psutil.net_io_counters().bytes_sent
            self.start_bytes_recv = psutil.net_io_counters().bytes_recv

    def update_stats(self):
        try:
            cpu_usage = psutil.cpu_percent()
            mem_usage = psutil.virtual_memory()._asdict()['percent']

            # Download BW (MB)
            try:
                download_bytes = psutil.net_io_counters(pernic=True)[self.if_name].bytes_recv - self.start_bytes_recv
                self.start_bytes_recv = psutil.net_io_counters(pernic=True)[self.if_name].bytes_recv
            except:
                # print("Interface wlp1s0 not found. Switching to All NIC data")
                download_bytes = psutil.net_io_counters().bytes_recv - self.start_bytes_recv
                self.start_bytes_recv = psutil.net_io_counters().bytes_recv
                
            #self.start_bytes_recv = psutil.net_io_counters(pernic=True)['wlp1s0'].bytes_recv
            download_mb = round(download_bytes/(1024.0 * 1024.0), 2)

            # Upload BW (MB)
            try:
                upload_bytes = psutil.net_io_counters(pernic=True)[self.if_name].bytes_sent - self.start_bytes_sent
                self.start_bytes_sent = psutil.net_io_counters(pernic=True)[self.if_name].bytes_sent
            except:
                # print("Interface wlp1s0 not found. Switching to All NIC data")
                upload_bytes = psutil.net_io_counters().bytes_sent - self.start_bytes_sent
                self.start_bytes_sent = psutil.net_io_counters().bytes_sent
            upload_mb = round(upload_bytes/(1024.0 * 1024.0), 2)

            print('Last {} seconds Stats: CPU {}%, Mem {}%, Download {}MB, Upload {}MB'.format(monitor_duration_seconds, cpu_usage, mem_usage, download_mb, upload_mb))

            # Save the stats
            bw_report = {}
            try:
                with open(self.bw_report_file, 'r') as f:
                    bw_report = json.load(f)
            except:
                bw_report = {}

            saved_upload_mb = bw_report.get('upload_mb') or 0
            saved_download_mb = bw_report.get('download_mb') or 0
            last_updated = datetime.now().isoformat()

            saved_upload_mb += upload_mb
            saved_download_mb += download_mb

            bw_report['last_updated'] = last_updated
            bw_report['upload_mb'] = round(saved_upload_mb, 2)
            bw_report['download_mb'] = round(saved_download_mb, 2)

            with open(self.bw_report_file, 'w') as f:
                json.dump(bw_report, f, indent=2)

        except Exception as ex:
            print('Exception occurred while saving stats. ignoring. Ex: {}'.format(ex))
            pass


    def run(self):
        print('CPU, Memory and Bandwidth Stats (every {} seconds)'.format(monitor_duration_seconds))

        while(True):
            try:
                # If closed (^C), then break
                if self._thread_stop.is_set():
                    print('Exiting upload thread.')
                    break

                # Check stats every 10 seconds.
                time.sleep(10)
                self.update_stats()

            except Exception as ex:
                print('Exception occurred during stats upload thread, ignoring: {}'.format(ex))
                time.sleep(10)

    def run_nonblock(self):
        print('Starting Bandwidth Stats thread')
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._thread_stop.set()

if __name__ == '__main__':
    # To this as a thread from another class, use this code.
    # statsObj = Stats()
    # statsObj.run_nonblock()
    # statsObj._thread.join()

    statsObj = Stats()
    statsObj.run()

