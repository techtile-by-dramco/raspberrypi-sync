from flask import Flask
import csv
app = Flask(__name__)

possible_hostnames = [f"midas-minion-{num:03d}" for num in range(1,150)]

@app.route('/get-hostname/<string:mac_addr>')
def get_mac_addr(mac_addr):
    hostname = ""
    with open("/home/pi/mac-hostname-dict.csv","r+") as f:
         reader = csv.reader(f)
         table = {}
         for row in reader:
            if len(row) > 0:
                k, v = row
                table[k] = v
         if mac_addr in table:
            hostname = table[mac_addr]
         else:
            # search a new hostname
            occupied_hostnames = list(table.values())
            for h in possible_hostnames:
                if h not in occupied_hostnames:
                    hostname = h
                    break

    table[mac_addr]=hostname
    with open("/home/pi/mac-hostname-dict.csv","w+") as f:
        w = csv.writer(f)
        w.writerows(table.items())
    return hostname
