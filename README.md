# Tenmon

[<img src ="https://img.shields.io/badge/Slack-Chat-blue">](https://tenforward-workspace.slack.com/)

The Extended version of the livecoding project Tenforward Client, and monitoring agent written purely in python.


## Threading
This version uses threading to better handle parallelism and concurrency, the agent still uses simple scheduling for 
trivial monitoring and reporting of static metrics. Such as CPU 
`"softirq": 1.0, "iowait": 0.0, "interrupts": 41538.5, "total": 26.9, "soft_interrupts": 16997.5, "ctx_switches": 109907.0`
or mem usage `"used": 9140490240.0, "free": 58347601920.0`

Monitors has now also been extended and are subclassed to Exm (EXtendedMonitor). Every Exm runs as it own thread.

Also reporting for Exms runs as it own thread and uses thread safe FIFO Queue for message exchange. 


## Pulsar
The Tenforward Client could only send data using our open API, the version is primary intended to use *pulsar* but
we can also send data using MQTT or to PostgreSQL directly.


## Development and installation
For development this project uses docker and docker-compose.

To start the Database, Apache Pulsar and the Pulsar GUI, simply:

```bash
cd $project_home
docker-compose up
```
This should build and start all the containers, 

### Issues
* At first start of the containers the Apache Pulsar GUI is unable to connect to pulsar 
