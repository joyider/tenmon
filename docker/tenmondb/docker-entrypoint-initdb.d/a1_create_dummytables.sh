#!/usr/bin/env bash

psql -U "${POSTGRES_USER}" postgres -c "create or replace view mqtt_interface as SELECT NULL::json AS jsondata;"

psql -U "${POSTGRES_USER}" postgres -c "CREATE OR REPLACE FUNCTION public.mqtt_interface_ins()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY definer
AS $function$
BEGIN

  insert into mqtt_payload_message_history values
 (  (new.jsondata::json->>'APITimestamp')::timestamptz,
    (new.jsondata::json->>'Node')::text,
    (new.jsondata::json->>'Severity')::bigint,
    (new.jsondata::json->>'Summary')::text,
    (new.jsondata::json->>'FirstOccurrence')::timestamptz,
    (new.jsondata::json->>'LastOccurrence')::timestamptz,
    (new.jsondata::json->>'Tally')::bigint,
    (new.jsondata::json->>'Acknowledged')::bigint,
    (new.jsondata::json->>'Serial')::bigint,
    (new.jsondata::json->>'Source')::text,
    (new.jsondata::json->>'SupressEscalate')::bigint ,
    (new.jsondata::json->>'Bana')::text,
    (new.jsondata::json->>'IvarObjectID')::bigint,
    (new.jsondata::json->>'IvarSiteObjectID')::bigint,
    (new.jsondata::json->>'Agent')::text,
    (new.jsondata::json->>'TTNumber')::text,
    (new.jsondata::json->>'TTStatus')::text
    );

  if ((new.jsondata::json->>'Severity')::bigint)=0 then
    delete from mqtt_payload_message
    where serial=(new.jsondata::json->>'Serial')::bigint
      and source=(new.jsondata::json->>'Source')::text;
    return NULL;
  end if;

 insert into mqtt_payload_message values
 (  (new.jsondata::json->>'APITimestamp')::timestamptz,
    (new.jsondata::json->>'Node')::text,
    (new.jsondata::json->>'Severity')::bigint,
    (new.jsondata::json->>'Summary')::text,
    (new.jsondata::json->>'FirstOccurrence')::timestamptz,
    (new.jsondata::json->>'LastOccurrence')::timestamptz,
    (new.jsondata::json->>'Tally')::bigint,
    (new.jsondata::json->>'Acknowledged')::bigint,
    (new.jsondata::json->>'Serial')::bigint,
    (new.jsondata::json->>'Source')::text,
    (new.jsondata::json->>'SupressEscalate')::bigint ,
    (new.jsondata::json->>'Bana')::text,
    (new.jsondata::json->>'IvarObjectID')::bigint,
    (new.jsondata::json->>'IvarSiteObjectID')::bigint,
    (new.jsondata::json->>'Agent')::text,
    (new.jsondata::json->>'TTNumber')::text,
    (new.jsondata::json->>'TTStatus')::text
    )
    ON CONFLICT(source,serial) DO UPDATE SET
      apitimestamp=(new.jsondata::json->>'APITimestamp')::timestamptz,
      node=(new.jsondata::json->>'Node')::text,
      severity=(new.jsondata::json->>'Severity')::bigint,
      summary=(new.jsondata::json->>'Summary')::text,
      firstoccurrence = (new.jsondata::json->>'FirstOccurrence')::timestamptz,
      lastoccurrence = (new.jsondata::json->>'LastOccurrence')::timestamptz,
      tally = (new.jsondata::json->>'Tally')::bigint,
      acknowledged = (new.jsondata::json->>'Acknowledged')::bigint,
      supressescalate = (new.jsondata::json->>'SupressEscalate')::bigint ,
      bana = (new.jsondata::json->>'Bana')::text,
      ivarobjectid = (new.jsondata::json->>'IvarObjectID')::bigint,
      ivarsiteobjectid = (new.jsondata::json->>'IvarSiteObjectID')::bigint,
      agent = (new.jsondata::json->>'Agent')::text,
      ttnumber = (new.jsondata::json->>'TTNumber')::text,
      ttstatus = (new.jsondata::json->>'TTStatus')::text;

    return NEW;
END
$function$;"

psql -U "${POSTGRES_USER}" postgres -c "CREATE TRIGGER tgmqtt_interface_ins
  INSTEAD OF INSERT
  ON public.mqtt_interface
  FOR EACH ROW
  EXECUTE PROCEDURE mqtt_interface_ins();"


psql -U "${POSTGRES_USER}" postgres -c "create table jsonmall(struct json);"

psql -U "${POSTGRES_USER}" postgres -c "create table mqtt_payload_message as select
(struct::json->>'APITimestamp')::timestamptz as apitimestamp,
(struct::json->>'Node')::text as node,
(struct::json->>'Severity')::bigint as severity,
(struct::json->>'Summary')::text as summary,
(struct::json->>'FirstOccurrence')::timestamptz as firstoccurrence,
(struct::json->>'LastOccurrence')::timestamptz as lastoccurrence,
(struct::json->>'Tally')::bigint as tally,
(struct::json->>'Acknowledged')::bigint as acknowledged,
(struct::json->>'Serial')::bigint as serial,
(struct::json->>'Source')::text as source,
(struct::json->>'SupressEscalate')::bigint as supressescalate,
(struct::json->>'Bana')::text as bana,
(struct::json->>'IvarObjectID')::bigint as ivarobjectid,
(struct::json->>'IvarSiteObjectID')::bigint as ivarsiteobjectid,
(struct::json->>'Agent')::text as agent,
(struct::json->>'TTNumber')::text as ttnumber,
(struct::json->>'TTStatus')::text as ttstatus
from jsonmall;"



psql -U "${POSTGRES_USER}" postgres -c "create table mqtt_payload_message_history as select * from mqtt_payload_message where 1=0;"
psql -U "${POSTGRES_USER}" postgres -c "create sequence mqtt_payload_message_history_s start with 1 increment by 1;"
psql -U "${POSTGRES_USER}" postgres -c "alter table mqtt_payload_message_history add column change_version bigint default nextval('mqtt_payload_message_history_s');"
psql -U "${POSTGRES_USER}" postgres -c "select create_hypertable('mqtt_payload_message_history','apitimestamp');"

psql -U "${POSTGRES_USER}" postgres -c "create index mqtt_payload_message_history_x1 on mqtt_payload_message_history(source, serial, change_version);"
psql -U "${POSTGRES_USER}" postgres -c "alter table mqtt_payload_message add primary key (source, serial);"


psql -U "${POSTGRES_USER}" postgres -c 'create view mqtt_payload_json as (SELECT row_to_json(mpm.*) AS json_data
FROM (
SELECT mqtt_payload_message.node AS "Node",
mqtt_payload_message.severity AS "Severity",
mqtt_payload_message.summary AS "Summary",
mqtt_payload_message.firstoccurrence AS "FirstOccurrence",
mqtt_payload_message.lastoccurrence AS "LastOccurrence",
mqtt_payload_message.tally AS "Tally",
mqtt_payload_message.acknowledged AS "Acknowledged",
mqtt_payload_message.serial AS "Serial",
mqtt_payload_message.source AS "Source",
mqtt_payload_message.supressescalate AS "SupressEscalate",
mqtt_payload_message.bana AS "Bana",
mqtt_payload_message.ivarobjectid AS "IvarObjectID",
mqtt_payload_message.ivarsiteobjectid AS "IvarSiteObjectID",
mqtt_payload_message.agent AS "Agent",
mqtt_payload_message.ttnumber as "TTNumber",
mqtt_payload_message.ttstatus AS "TTStatus"
FROM mqtt_payload_message) mpm
);
'

psql -U "${POSTGRES_USER}" postgres -c ' CREATE OR REPLACE FUNCTION mqtt_publish (topic text , payload text)
  RETURNS text
AS $$
import os
str = "/usr/bin/mosquitto_pub -h tm_pulsar -t "+topic+" -m '"+payload+"'"
os.system(str)
$$ LANGUAGE plpython3u;'

psql -U "${POSTGRES_USER}" postgres -c "CREATE TABLE public.alertlog (
topic text,
alertmsg text
); "

psql -U "${POSTGRES_USER}" postgres -c "CREATE TABLE public.gateway_actions (
id SERIAL,
topic text,
action text
); "

psql -U "${POSTGRES_USER}" postgres -c "insert into gateway_actions (topic, action) values ('/ictl6145/oracle/alert','insert into
 alertlog (topic,alertmsg) values (''%s'',''%s'')');"