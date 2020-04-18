--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: create_secretkey(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.create_secretkey() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	NEW.secretkey :=  regexp_replace(encode(('{"uniquekey"'||':'|| '"' ||NEW.uniquekey||'"' ||','|| '"customerid"'||':'|| '"' ||NEW.customerid||'"' ||'}')::bytea, 'base64'), E'[\\n\\r]+', '', 'g');
	RETURN NEW;
END $$;


ALTER FUNCTION public.create_secretkey() OWNER TO postgres;

--
-- Name: generate_uniquekey(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.generate_uniquekey(integer) RETURNS text
    LANGUAGE sql
    AS $_$ 
  SELECT array_to_string(
    ARRAY (
      SELECT substring(
        '0123456789abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 
        FROM (random() *62)::int FOR 1)
      FROM generate_series(1, $1) ), '' ) 
$_$;


ALTER FUNCTION public.generate_uniquekey(integer) OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alertlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alertlog (
    topic text,
    alertmsg text
);


ALTER TABLE public.alertlog OWNER TO postgres;

--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    id bigint NOT NULL,
    customerid uuid NOT NULL,
    clientid character varying(50) NOT NULL,
    ip inet NOT NULL,
    hostname character varying(100) NOT NULL,
    cpu_phys smallint NOT NULL,
    cpu_logical smallint NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clients_id_seq OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_id_seq OWNED BY public.clients.id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    customername character varying(255) NOT NULL,
    uniquekey character varying(40) DEFAULT public.generate_uniquekey(32) NOT NULL,
    plan smallint DEFAULT 0 NOT NULL,
    customerid uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    secretkey text
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: COLUMN customers.plan; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.customers.plan IS '0 is free plan, 1 is standard plan 2 is extended above 2 reserved for special plans';


--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO postgres;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: gateway_actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gateway_actions (
    id integer NOT NULL,
    topic text,
    action text
);


ALTER TABLE public.gateway_actions OWNER TO postgres;

--
-- Name: gateway_actions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gateway_actions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gateway_actions_id_seq OWNER TO postgres;

--
-- Name: gateway_actions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gateway_actions_id_seq OWNED BY public.gateway_actions.id;


--
-- Name: jsonmall; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jsonmall (
    struct json
);


ALTER TABLE public.jsonmall OWNER TO postgres;

--
-- Name: mqtt_interface; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.mqtt_interface AS
 SELECT NULL::json AS jsondata;


ALTER TABLE public.mqtt_interface OWNER TO postgres;

--
-- Name: mqtt_payload_message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mqtt_payload_message (
    apitimestamp timestamp with time zone,
    node text,
    severity bigint,
    summary text,
    firstoccurrence timestamp with time zone,
    lastoccurrence timestamp with time zone,
    tally bigint,
    acknowledged bigint,
    serial bigint NOT NULL,
    source text NOT NULL,
    supressescalate bigint,
    bana text,
    ivarobjectid bigint,
    ivarsiteobjectid bigint,
    agent text,
    ttnumber text,
    ttstatus text
);


ALTER TABLE public.mqtt_payload_message OWNER TO postgres;

--
-- Name: mqtt_payload_json; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.mqtt_payload_json AS
 SELECT row_to_json(mpm.*) AS json_data
   FROM ( SELECT mqtt_payload_message.node AS "Node",
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
            mqtt_payload_message.ttnumber AS "TTNumber",
            mqtt_payload_message.ttstatus AS "TTStatus"
           FROM public.mqtt_payload_message) mpm;


ALTER TABLE public.mqtt_payload_json OWNER TO postgres;

--
-- Name: mqtt_payload_message_history_s; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mqtt_payload_message_history_s
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mqtt_payload_message_history_s OWNER TO postgres;

--
-- Name: mqtt_payload_message_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mqtt_payload_message_history (
    apitimestamp timestamp with time zone NOT NULL,
    node text,
    severity bigint,
    summary text,
    firstoccurrence timestamp with time zone,
    lastoccurrence timestamp with time zone,
    tally bigint,
    acknowledged bigint,
    serial bigint,
    source text,
    supressescalate bigint,
    bana text,
    ivarobjectid bigint,
    ivarsiteobjectid bigint,
    agent text,
    ttnumber text,
    ttstatus text,
    change_version bigint DEFAULT nextval('public.mqtt_payload_message_history_s'::regclass)
);


ALTER TABLE public.mqtt_payload_message_history OWNER TO postgres;

--
-- Name: clients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id_seq'::regclass);


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: gateway_actions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gateway_actions ALTER COLUMN id SET DEFAULT nextval('public.gateway_actions_id_seq'::regclass);


--
-- Name: clients clients_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pk PRIMARY KEY (id, customerid);


--
-- Name: clients clients_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_un UNIQUE (hostname, ip);


--
-- Name: customers customers_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pk PRIMARY KEY (id);


--
-- Name: customers customers_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_un UNIQUE (customerid);


--
-- Name: mqtt_payload_message mqtt_payload_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mqtt_payload_message
    ADD CONSTRAINT mqtt_payload_message_pkey PRIMARY KEY (source, serial);


--
-- Name: mqtt_payload_message_history_apitimestamp_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mqtt_payload_message_history_apitimestamp_idx ON public.mqtt_payload_message_history USING btree (apitimestamp DESC);


--
-- Name: mqtt_payload_message_history_x1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mqtt_payload_message_history_x1 ON public.mqtt_payload_message_history USING btree (source, serial, change_version);


--
-- Name: customers setsecretkey; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER setsecretkey BEFORE INSERT OR UPDATE ON public.customers FOR EACH ROW EXECUTE PROCEDURE public.create_secretkey();


--
-- Name: mqtt_payload_message_history ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.mqtt_payload_message_history FOR EACH ROW EXECUTE PROCEDURE _timescaledb_internal.insert_blocker();


--
-- Name: clients clients_customerid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_customerid_fkey FOREIGN KEY (customerid) REFERENCES public.customers(customerid);


--
-- PostgreSQL database dump complete
--
