from flask import Flask
import csv
app = Flask(__name__)

possible_hostnames = [f"midas-minion-{num:03d}" for num in range(1,150)]

@app.route('/get-hostname/<string:mac_addr>')
def get_mac_addr(mac_addr):
    hostname = ""
    with open("/home/pi/mac-hostname-dict.csv","r+") as f:
        # csv header mac,hostname,last-seen
         df = pd.read_csv(f, sep=';')
         if mac_addr in df["mac"]:
            row = df.query(f'mac == "{mac_addr}"')[0]
            hostname = row["mac"]
            row["last-seen] = datetime.datetime.utcnow()
         else:
            # search a new hostname
            occupied_hostnames = df["mac"].tolist()
            for h in possible_hostnames:
                if h not in occupied_hostnames:
                    hostname = h
                    df = df.append({
                        "mac": mac_addr,
                        "hostname": h,
                        "last-seen": datetime.datetime.utcnow()
                    })
                    break

    with open("/home/pi/mac-hostname-dict.csv","w+") as f:
        df.to_csv(f, index=False)
    return hostname
