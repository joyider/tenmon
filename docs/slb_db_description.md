# SLB Postgresql Databas model beskrivning

##Tables

###

#### mqtt_payload_message
Tabel för lagring av aktiva larm (Severity>0)

| mqtt\_payload\_message |
|------------------------|
| serial                 |
| source                 |
| apitimestamp           |
| node                   |
| severity               |
| summary                |
| firstoccurrence        |
| lastoccurrence         |
| tally                  |
| acknowledged           |
| supressescalate        |
| bana                   |
| ivarobjectid           |
| ivarsiteobjectid       |
| agent                  |
| ttnumber               |
| ttstatus               |
