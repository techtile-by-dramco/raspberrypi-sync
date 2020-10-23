const TIME_INTERVAL = 5 * 60 * 1000;
var addr = require('node-macaddress').one();
var osutils = require('os-utils');

var pi = require('node-raspi');

const Influx = require('influx');
const influx = new Influx.InfluxDB({
 host: 'midas-server.local',
 database: 'minions',
 port: 8086,
 username: '*****',
 password: '*****',
 schema: [
   {
     measurement: 'cpu_metrics',
     fields: {
       temperature: Influx.FieldType.FLOAT,
       free_memory: Influx.FieldType.FLOAT,
       cpu_load: Influx.FieldType.FLOAT,
       is_online: Influx.FieldType.BOOLEAN
       soc_vcc : Influx.FieldType.FLOAT,
     },
     tags: [
       'mac_addr'
     ]
   }
 ]
})

function writeMeasurement(){
        influx.writeMeasurement('cpu_metrics', [
  {
    tags: { mac_addr: addr },
    fields: {
        temperature: pi.getThrm(),
        free_memory: getMemUsage(),
        cpu_load: osutils.loadavg(1),
        is_online: true,
        soc_vcc: pi.getVcc()
    },
  }
])
}

setTimeout(writeMeasurement, TIME_INTERVAL);




