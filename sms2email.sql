create schema s2e;

CREATE TABLE s2e.sms2email (
                                  id bigint NOT NULL,
                                  sms_id integer,
                                  email text,
                                  status text,
                                  created_on timestamp without time zone,
                                  updated_on timestamp without time zone
);


ALTER TABLE s2e.sms2email OWNER TO postgres;

--
-- Name: sms2email_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s2e.sms2email_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s2e.sms2email_id_seq OWNER TO postgres;

--
-- Name: sms2email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s2e.sms2email_id_seq OWNED BY s2e.sms2email.id;


--
-- Name: sms2email id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s2e.sms2email ALTER COLUMN id SET DEFAULT nextval('s2e.sms2email_id_seq'::regclass);


--
-- Name: sms2email sms2email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s2e.sms2email
    ADD CONSTRAINT s2e__sms2email_pkey PRIMARY KEY (id);


--
-- Name: sms2email uniq_sms_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s2e.sms2email
    ADD CONSTRAINT uniq_s2e__sms_id UNIQUE (sms_id);


--
-- Name: sms2email fk_inbox_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s2e.sms2email
    ADD CONSTRAINT fk_s2e__sms2email__inbox_id FOREIGN KEY (sms_id) REFERENCES public.inbox("ID");


--
-- Name: TABLE sms2email; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE s2e.sms2email TO smsd;


--
-- Name: SEQUENCE sms2email_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE s2e.sms2email_id_seq TO smsd;


--
-- PostgreSQL database dump complete
--
