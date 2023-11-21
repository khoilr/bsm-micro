--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)

-- Started on 2023-11-09 10:52:10 +07

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 16450)
-- Name: AttendanceTracking; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AttendanceTracking" (
    tracking_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    camera_id integer,
    face_id integer
);


ALTER TABLE public."AttendanceTracking" OWNER TO postgres;

--
-- TOC entry 3499 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE "AttendanceTracking"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."AttendanceTracking" IS 'Tortoise-based log model.';


--
-- TOC entry 225 (class 1259 OID 16449)
-- Name: AttendanceTracking_tracking_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."AttendanceTracking_tracking_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."AttendanceTracking_tracking_id_seq" OWNER TO postgres;

--
-- TOC entry 3500 (class 0 OID 0)
-- Dependencies: 225
-- Name: AttendanceTracking_tracking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."AttendanceTracking_tracking_id_seq" OWNED BY public."AttendanceTracking".tracking_id;


--
-- TOC entry 228 (class 1259 OID 16469)
-- Name: Camera; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Camera" (
    id integer NOT NULL,
    name character varying(255),
    description character varying(256),
    connect_uri character varying(256),
    placeholder_url character varying(255),
    type integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    zone_id integer
);


ALTER TABLE public."Camera" OWNER TO postgres;

--
-- TOC entry 3501 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE "Camera"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Camera" IS 'Tortoise-based camera model.';


--
-- TOC entry 227 (class 1259 OID 16468)
-- Name: Camera_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Camera_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Camera_id_seq" OWNER TO postgres;

--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 227
-- Name: Camera_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Camera_id_seq" OWNED BY public."Camera".id;


--
-- TOC entry 232 (class 1259 OID 16504)
-- Name: Event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Event" (
    id integer NOT NULL,
    description character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public."Event" OWNER TO postgres;

--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE "Event"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Event" IS 'Tortoise-based log model.';


--
-- TOC entry 234 (class 1259 OID 16513)
-- Name: EventLog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventLog" (
    id integer NOT NULL,
    video_url character varying(255),
    image_id character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    event_id integer,
    face_id integer
);


ALTER TABLE public."EventLog" OWNER TO postgres;

--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE "EventLog"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."EventLog" IS 'Tortoise-based log model.';


--
-- TOC entry 233 (class 1259 OID 16512)
-- Name: EventLog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."EventLog_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."EventLog_id_seq" OWNER TO postgres;

--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 233
-- Name: EventLog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."EventLog_id_seq" OWNED BY public."EventLog".id;


--
-- TOC entry 231 (class 1259 OID 16503)
-- Name: Event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Event_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Event_id_seq" OWNER TO postgres;

--
-- TOC entry 3506 (class 0 OID 0)
-- Dependencies: 231
-- Name: Event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Event_id_seq" OWNED BY public."Event".id;


--
-- TOC entry 220 (class 1259 OID 16403)
-- Name: Face; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Face" (
    face_id integer NOT NULL,
    "FrameFilePath" text,
    "X" double precision,
    "Y" double precision,
    "Width" integer,
    "Height" integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    person_id integer
);


ALTER TABLE public."Face" OWNER TO postgres;

--
-- TOC entry 3507 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE "Face"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Face" IS 'Tortoise-based log model.';


--
-- TOC entry 219 (class 1259 OID 16402)
-- Name: Face_face_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Face_face_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Face_face_id_seq" OWNER TO postgres;

--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 219
-- Name: Face_face_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Face_face_id_seq" OWNED BY public."Face".face_id;


--
-- TOC entry 230 (class 1259 OID 16485)
-- Name: Log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Log" (
    log_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    camera_id integer NOT NULL,
    face_id integer NOT NULL
);


ALTER TABLE public."Log" OWNER TO postgres;

--
-- TOC entry 3509 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE "Log"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Log" IS 'Tortoise-based log model.';


--
-- TOC entry 229 (class 1259 OID 16484)
-- Name: Log_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Log_log_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Log_log_id_seq" OWNER TO postgres;

--
-- TOC entry 3510 (class 0 OID 0)
-- Dependencies: 229
-- Name: Log_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Log_log_id_seq" OWNED BY public."Log".log_id;


--
-- TOC entry 218 (class 1259 OID 16392)
-- Name: Person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Person" (
    person_id integer NOT NULL,
    name character varying(255),
    gender integer,
    dob timestamp with time zone,
    phone character varying(15),
    avatar_url character varying(255),
    "position" character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public."Person" OWNER TO postgres;

--
-- TOC entry 3511 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE "Person"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Person" IS 'Tortoise-based log model.';


--
-- TOC entry 217 (class 1259 OID 16391)
-- Name: Person_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Person_person_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Person_person_id_seq" OWNER TO postgres;

--
-- TOC entry 3512 (class 0 OID 0)
-- Dependencies: 217
-- Name: Person_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Person_person_id_seq" OWNED BY public."Person".person_id;


--
-- TOC entry 222 (class 1259 OID 16419)
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name character varying(200) NOT NULL,
    username character varying(200) NOT NULL,
    password character varying(200) NOT NULL,
    manager boolean NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- TOC entry 3513 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE "User"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."User" IS 'Data model for user.';


--
-- TOC entry 221 (class 1259 OID 16418)
-- Name: User_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_user_id_seq" OWNER TO postgres;

--
-- TOC entry 3514 (class 0 OID 0)
-- Dependencies: 221
-- Name: User_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_user_id_seq" OWNED BY public."User".user_id;


--
-- TOC entry 224 (class 1259 OID 16439)
-- Name: Zone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Zone" (
    zone_id integer NOT NULL,
    name character varying(255),
    description character varying(255),
    placeholder_url character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public."Zone" OWNER TO postgres;

--
-- TOC entry 3515 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE "Zone"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Zone" IS 'Tortoise-based zone model.';


--
-- TOC entry 236 (class 1259 OID 16534)
-- Name: ZoneSetting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ZoneSetting" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255),
    config character varying(255) NOT NULL,
    zone_id integer
);


ALTER TABLE public."ZoneSetting" OWNER TO postgres;

--
-- TOC entry 3516 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE "ZoneSetting"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."ZoneSetting" IS 'Model for demo purpose.';


--
-- TOC entry 235 (class 1259 OID 16533)
-- Name: ZoneSetting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ZoneSetting_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."ZoneSetting_id_seq" OWNER TO postgres;

--
-- TOC entry 3517 (class 0 OID 0)
-- Dependencies: 235
-- Name: ZoneSetting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ZoneSetting_id_seq" OWNED BY public."ZoneSetting".id;


--
-- TOC entry 223 (class 1259 OID 16438)
-- Name: Zone_zone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Zone_zone_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Zone_zone_id_seq" OWNER TO postgres;

--
-- TOC entry 3518 (class 0 OID 0)
-- Dependencies: 223
-- Name: Zone_zone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Zone_zone_id_seq" OWNED BY public."Zone".zone_id;


--
-- TOC entry 238 (class 1259 OID 16548)
-- Name: aerich; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aerich (
    id integer NOT NULL,
    version character varying(255) NOT NULL,
    app character varying(100) NOT NULL,
    content jsonb NOT NULL
);


ALTER TABLE public.aerich OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16547)
-- Name: aerich_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aerich_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aerich_id_seq OWNER TO postgres;

--
-- TOC entry 3519 (class 0 OID 0)
-- Dependencies: 237
-- Name: aerich_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aerich_id_seq OWNED BY public.aerich.id;


--
-- TOC entry 216 (class 1259 OID 16385)
-- Name: dummymodel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dummymodel (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    description character varying(155) NOT NULL
);


ALTER TABLE public.dummymodel OWNER TO postgres;

--
-- TOC entry 3520 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE dummymodel; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.dummymodel IS 'Model for demo purpose.';


--
-- TOC entry 215 (class 1259 OID 16384)
-- Name: dummymodel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dummymodel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dummymodel_id_seq OWNER TO postgres;

--
-- TOC entry 3521 (class 0 OID 0)
-- Dependencies: 215
-- Name: dummymodel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dummymodel_id_seq OWNED BY public.dummymodel.id;


--
-- TOC entry 3271 (class 2604 OID 16453)
-- Name: AttendanceTracking tracking_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AttendanceTracking" ALTER COLUMN tracking_id SET DEFAULT nextval('public."AttendanceTracking_tracking_id_seq"'::regclass);


--
-- TOC entry 3274 (class 2604 OID 16472)
-- Name: Camera id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Camera" ALTER COLUMN id SET DEFAULT nextval('public."Camera_id_seq"'::regclass);


--
-- TOC entry 3280 (class 2604 OID 16507)
-- Name: Event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event" ALTER COLUMN id SET DEFAULT nextval('public."Event_id_seq"'::regclass);


--
-- TOC entry 3283 (class 2604 OID 16516)
-- Name: EventLog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventLog" ALTER COLUMN id SET DEFAULT nextval('public."EventLog_id_seq"'::regclass);


--
-- TOC entry 3262 (class 2604 OID 16406)
-- Name: Face face_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Face" ALTER COLUMN face_id SET DEFAULT nextval('public."Face_face_id_seq"'::regclass);


--
-- TOC entry 3277 (class 2604 OID 16488)
-- Name: Log log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Log" ALTER COLUMN log_id SET DEFAULT nextval('public."Log_log_id_seq"'::regclass);


--
-- TOC entry 3259 (class 2604 OID 16395)
-- Name: Person person_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Person" ALTER COLUMN person_id SET DEFAULT nextval('public."Person_person_id_seq"'::regclass);


--
-- TOC entry 3265 (class 2604 OID 16422)
-- Name: User user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN user_id SET DEFAULT nextval('public."User_user_id_seq"'::regclass);


--
-- TOC entry 3268 (class 2604 OID 16442)
-- Name: Zone zone_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Zone" ALTER COLUMN zone_id SET DEFAULT nextval('public."Zone_zone_id_seq"'::regclass);


--
-- TOC entry 3286 (class 2604 OID 16537)
-- Name: ZoneSetting id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ZoneSetting" ALTER COLUMN id SET DEFAULT nextval('public."ZoneSetting_id_seq"'::regclass);


--
-- TOC entry 3287 (class 2604 OID 16551)
-- Name: aerich id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aerich ALTER COLUMN id SET DEFAULT nextval('public.aerich_id_seq'::regclass);


--
-- TOC entry 3258 (class 2604 OID 16388)
-- Name: dummymodel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dummymodel ALTER COLUMN id SET DEFAULT nextval('public.dummymodel_id_seq'::regclass);


--
-- TOC entry 3480 (class 0 OID 16450)
-- Dependencies: 226
-- Data for Name: AttendanceTracking; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."AttendanceTracking" (tracking_id, created_at, updated_at, camera_id, face_id) FROM stdin;
\.


--
-- TOC entry 3482 (class 0 OID 16469)
-- Dependencies: 228
-- Data for Name: Camera; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Camera" (id, name, description, connect_uri, placeholder_url, type, created_at, updated_at, zone_id) FROM stdin;
2	Ezviz	Ezviz Description Test	ezopen://open.ezviz.com/BA3686955/1.hd.live	1699501755.025059_ezviz_cam.png	2	2023-11-08 09:37:41.585598+00	2023-11-08 09:37:41.585598+00	2
1	Hanet	Hanet 1C Test	rtsp://0.tcp.ap.ngrok.io:10708/user:1cinnovation;pwd:1cinnovation123	1699501809.448446_hanet_cam.png	1	2023-11-08 09:37:41.544816+00	2023-11-08 09:37:41.544816+00	1
\.


--
-- TOC entry 3486 (class 0 OID 16504)
-- Dependencies: 232
-- Data for Name: Event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Event" (id, description, created_at, updated_at) FROM stdin;
1	check-in	2023-11-08 09:27:18.524954+00	2023-11-08 09:27:18.524981+00
\.


--
-- TOC entry 3488 (class 0 OID 16513)
-- Dependencies: 234
-- Data for Name: EventLog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."EventLog" (id, video_url, image_id, created_at, updated_at, event_id, face_id) FROM stdin;
4	1	1699436027.611261_frame.jpg	2023-11-08 09:33:47.673006+00	2023-11-08 09:33:47.67304+00	\N	1
5	1	1699438573.568054_frame.jpg	2023-11-08 10:16:15.225569+00	2023-11-08 10:16:15.225598+00	\N	1
6	1	1699438646.040149_frame.jpg	2023-11-08 10:17:26.703012+00	2023-11-08 10:17:26.703043+00	\N	1
7	1	1699438850.46123_frame.jpg	2023-11-08 10:20:51.445034+00	2023-11-08 10:20:51.445064+00	\N	1
8	1	1699438997.657142_frame.jpg	2023-11-08 10:23:17.747886+00	2023-11-08 10:23:17.747918+00	\N	1
9	1	1699439513.393231_frame.jpg	2023-11-08 10:31:53.499152+00	2023-11-08 10:31:53.499178+00	\N	2
10	1	1699439670.187447_frame.jpg	2023-11-08 10:34:30.324544+00	2023-11-08 10:34:30.324571+00	\N	2
11	1	1699439707.522492_frame.jpg	2023-11-08 10:35:07.624008+00	2023-11-08 10:35:07.624034+00	\N	2
12	1	1699439760.385172_frame.jpg	2023-11-08 10:36:00.503113+00	2023-11-08 10:36:00.503141+00	\N	2
13	1	1699439967.380602_frame.jpg	2023-11-08 10:39:27.496204+00	2023-11-08 10:39:27.496229+00	\N	2
14	1	1699440383.579598_frame.jpg	2023-11-08 10:46:23.78348+00	2023-11-08 10:46:23.783505+00	\N	2
15	1	1699440864.937595_frame.jpg	2023-11-08 10:54:25.12142+00	2023-11-08 10:54:25.121446+00	\N	2
16	1	1699440951.810687_frame.jpg	2023-11-08 10:55:51.908257+00	2023-11-08 10:55:51.908284+00	\N	2
17	1	1699441022.817629_frame.jpg	2023-11-08 10:57:02.969518+00	2023-11-08 10:57:02.969544+00	\N	1
18	1	1699441331.857157_frame.jpg	2023-11-08 11:02:11.998558+00	2023-11-08 11:02:11.998584+00	\N	1
19	1	1699441415.382521_frame.jpg	2023-11-08 11:03:35.474032+00	2023-11-08 11:03:35.474058+00	\N	1
20	1	1699441490.729324_frame.jpg	2023-11-08 11:04:50.82502+00	2023-11-08 11:04:50.825049+00	\N	1
21	1	1699441612.037474_frame.jpg	2023-11-08 11:06:52.142511+00	2023-11-08 11:06:52.142537+00	\N	1
22	1	1699441684.352843_frame.jpg	2023-11-08 11:08:04.521724+00	2023-11-08 11:08:04.52175+00	\N	1
23	1	1699441754.188268_frame.jpg	2023-11-08 11:09:14.29695+00	2023-11-08 11:09:14.296985+00	\N	1
24	1	1699441826.725219_frame.jpg	2023-11-08 11:10:26.906419+00	2023-11-08 11:10:26.906445+00	\N	1
25	1	1699441947.169276_frame.jpg	2023-11-08 11:12:27.297357+00	2023-11-08 11:12:27.297383+00	\N	1
26	1	1699442015.617145_frame.jpg	2023-11-08 11:13:35.726621+00	2023-11-08 11:13:35.726653+00	\N	1
27	1	1699442086.776213_frame.jpg	2023-11-08 11:14:46.889042+00	2023-11-08 11:14:46.889066+00	\N	1
28	1	1699442162.784524_frame.jpg	2023-11-08 11:16:02.90644+00	2023-11-08 11:16:02.906466+00	\N	1
29	1	1699442227.973384_frame.jpg	2023-11-08 11:17:08.097166+00	2023-11-08 11:17:08.097192+00	\N	1
30	1	1699442348.812724_frame.jpg	2023-11-08 11:19:08.946715+00	2023-11-08 11:19:08.946745+00	\N	1
31	1	1699442468.775402_frame.jpg	2023-11-08 11:21:08.894787+00	2023-11-08 11:21:08.894812+00	\N	1
32	1	1699442588.130881_frame.jpg	2023-11-08 11:23:08.413431+00	2023-11-08 11:23:08.413481+00	\N	1
33	1	1699442707.267027_frame.jpg	2023-11-08 11:25:07.496383+00	2023-11-08 11:25:07.496409+00	\N	1
34	1	1699442776.638759_frame.jpg	2023-11-08 11:26:16.769118+00	2023-11-08 11:26:16.769144+00	\N	1
35	1	1699442897.538776_frame.jpg	2023-11-08 11:28:17.670816+00	2023-11-08 11:28:17.670841+00	\N	1
36	1	1699442968.959606_frame.jpg	2023-11-08 11:29:29.110107+00	2023-11-08 11:29:29.110132+00	\N	1
37	1	1699443036.637509_frame.jpg	2023-11-08 11:30:36.772539+00	2023-11-08 11:30:36.772565+00	\N	1
38	1	1699443107.22459_frame.jpg	2023-11-08 11:31:47.362214+00	2023-11-08 11:31:47.36224+00	\N	1
39	1	1699443225.808002_frame.jpg	2023-11-08 11:33:46.050612+00	2023-11-08 11:33:46.050639+00	\N	1
40	1	1699443294.708309_frame.jpg	2023-11-08 11:34:54.851507+00	2023-11-08 11:34:54.851532+00	\N	1
41	1	1699443365.130995_frame.jpg	2023-11-08 11:36:05.440442+00	2023-11-08 11:36:05.44047+00	\N	1
42	1	1699443433.678852_frame.jpg	2023-11-08 11:37:13.825839+00	2023-11-08 11:37:13.825867+00	\N	1
43	1	1699443504.758907_frame.jpg	2023-11-08 11:38:24.907759+00	2023-11-08 11:38:24.907785+00	\N	1
44	1	1699443574.717308_frame.jpg	2023-11-08 11:39:35.184221+00	2023-11-08 11:39:35.184246+00	\N	1
45	1	1699443645.895551_frame.jpg	2023-11-08 11:40:46.069824+00	2023-11-08 11:40:46.069848+00	\N	1
46	1	1699443716.989755_frame.jpg	2023-11-08 11:41:57.144075+00	2023-11-08 11:41:57.144101+00	\N	1
47	1	1699443835.564575_frame.jpg	2023-11-08 11:43:55.859043+00	2023-11-08 11:43:55.85907+00	\N	1
48	1	1699443904.748211_frame.jpg	2023-11-08 11:45:04.931606+00	2023-11-08 11:45:04.931632+00	\N	1
49	1	1699443975.768253_frame.jpg	2023-11-08 11:46:15.955191+00	2023-11-08 11:46:15.955216+00	\N	1
50	1	1699444092.789549_frame.jpg	2023-11-08 11:48:13.247963+00	2023-11-08 11:48:13.247999+00	\N	1
51	1	1699444211.849782_frame.jpg	2023-11-08 11:50:12.035051+00	2023-11-08 11:50:12.035077+00	\N	1
52	1	1699444283.006292_frame.jpg	2023-11-08 11:51:23.195126+00	2023-11-08 11:51:23.195153+00	\N	1
53	1	1699444352.045239_frame.jpg	2023-11-08 11:52:32.583031+00	2023-11-08 11:52:32.583063+00	\N	1
54	1	1699444471.533169_frame.jpg	2023-11-08 11:54:31.729616+00	2023-11-08 11:54:31.729642+00	\N	1
55	1	1699444595.59494_frame.jpg	2023-11-08 11:56:35.811422+00	2023-11-08 11:56:35.811451+00	\N	1
56	1	1699444713.32422_frame.jpg	2023-11-08 11:58:33.522314+00	2023-11-08 11:58:33.522341+00	\N	1
57	1	1699444791.586791_frame.jpg	2023-11-08 11:59:51.789069+00	2023-11-08 11:59:51.789089+00	\N	1
58	1	1699444864.034642_frame.jpg	2023-11-08 12:01:04.237691+00	2023-11-08 12:01:04.237715+00	\N	1
59	1	1699444934.584029_frame.jpg	2023-11-08 12:02:14.941159+00	2023-11-08 12:02:14.941185+00	\N	1
60	1	1699445007.651329_frame.jpg	2023-11-08 12:03:27.855492+00	2023-11-08 12:03:27.855518+00	\N	1
61	1	1699445127.564656_frame.jpg	2023-11-08 12:05:27.759096+00	2023-11-08 12:05:27.759122+00	\N	1
62	1	1699445198.603166_frame.jpg	2023-11-08 12:06:38.81377+00	2023-11-08 12:06:38.813795+00	\N	1
63	1	1699445266.76283_frame.jpg	2023-11-08 12:07:46.99854+00	2023-11-08 12:07:46.998568+00	\N	1
64	1	1699445337.68585_frame.jpg	2023-11-08 12:08:57.902557+00	2023-11-08 12:08:57.902583+00	\N	1
65	1	1699445457.211612_frame.jpg	2023-11-08 12:10:57.430141+00	2023-11-08 12:10:57.430167+00	\N	1
66	1	1699445574.295494_frame.jpg	2023-11-08 12:12:54.702902+00	2023-11-08 12:12:54.702929+00	\N	1
67	1	1699445695.469194_frame.jpg	2023-11-08 12:14:55.684378+00	2023-11-08 12:14:55.684414+00	\N	1
68	1	1699445815.796994_frame.jpg	2023-11-08 12:16:56.00628+00	2023-11-08 12:16:56.006307+00	\N	1
69	1	1699445936.295309_frame.jpg	2023-11-08 12:18:56.522254+00	2023-11-08 12:18:56.522283+00	\N	1
70	1	1699446012.420047_frame.jpg	2023-11-08 12:20:12.646548+00	2023-11-08 12:20:12.646574+00	\N	1
71	1	1699446085.278617_frame.jpg	2023-11-08 12:21:25.496753+00	2023-11-08 12:21:25.49678+00	\N	1
72	1	1699446158.53719_frame.jpg	2023-11-08 12:22:38.983548+00	2023-11-08 12:22:38.983576+00	\N	1
73	1	1699446237.271991_frame.jpg	2023-11-08 12:23:57.632887+00	2023-11-08 12:23:57.632924+00	\N	1
74	1	1699446356.945119_frame.jpg	2023-11-08 12:25:57.386153+00	2023-11-08 12:25:57.38618+00	\N	1
75	1	1699446425.200721_frame.jpg	2023-11-08 12:27:05.69271+00	2023-11-08 12:27:05.692736+00	\N	1
76	1	1699446544.516104_frame.jpg	2023-11-08 12:29:04.7629+00	2023-11-08 12:29:04.762927+00	\N	1
77	1	1699446617.521323_frame.jpg	2023-11-08 12:30:17.765354+00	2023-11-08 12:30:17.76538+00	\N	1
78	1	1699446685.859645_frame.jpg	2023-11-08 12:31:26.086184+00	2023-11-08 12:31:26.08621+00	\N	1
79	1	1699446756.888889_frame.jpg	2023-11-08 12:32:37.129256+00	2023-11-08 12:32:37.129282+00	\N	1
80	1	1699446880.278735_frame.jpg	2023-11-08 12:34:40.551104+00	2023-11-08 12:34:40.55113+00	\N	1
81	1	1699446951.981191_frame.jpg	2023-11-08 12:35:52.335106+00	2023-11-08 12:35:52.335132+00	\N	1
82	1	1699447068.506475_frame.jpg	2023-11-08 12:37:48.908224+00	2023-11-08 12:37:48.90825+00	\N	1
83	1	1699447188.023552_frame.jpg	2023-11-08 12:39:48.29425+00	2023-11-08 12:39:48.294276+00	\N	1
84	1	1699447306.93347_frame.jpg	2023-11-08 12:41:47.207222+00	2023-11-08 12:41:47.207248+00	\N	1
85	1	1699447425.900107_frame.jpg	2023-11-08 12:43:46.168643+00	2023-11-08 12:43:46.168669+00	\N	1
86	1	1699447548.065164_frame.jpg	2023-11-08 12:45:48.558803+00	2023-11-08 12:45:48.558829+00	\N	1
87	1	1699447663.377789_frame.jpg	2023-11-08 12:47:43.649052+00	2023-11-08 12:47:43.649078+00	\N	1
88	1	1699447734.798547_frame.jpg	2023-11-08 12:48:55.076385+00	2023-11-08 12:48:55.076413+00	\N	1
89	1	1699447812.238229_frame.jpg	2023-11-08 12:50:12.494665+00	2023-11-08 12:50:12.49469+00	\N	1
90	1	1699447885.118854_frame.jpg	2023-11-08 12:51:25.377167+00	2023-11-08 12:51:25.377193+00	\N	1
91	1	1699447954.594352_frame.jpg	2023-11-08 12:52:34.878121+00	2023-11-08 12:52:34.878146+00	\N	1
92	1	1699448074.491263_frame.jpg	2023-11-08 12:54:35.029287+00	2023-11-08 12:54:35.029312+00	\N	1
93	1	1699448194.066822_frame.jpg	2023-11-08 12:56:34.338133+00	2023-11-08 12:56:34.338158+00	\N	1
94	1	1699448314.0436_frame.jpg	2023-11-08 12:58:34.326648+00	2023-11-08 12:58:34.326676+00	\N	1
95	1	1699448382.04712_frame.jpg	2023-11-08 12:59:42.337339+00	2023-11-08 12:59:42.337365+00	\N	1
96	1	1699448507.936306_frame.jpg	2023-11-08 13:01:48.488059+00	2023-11-08 13:01:48.488084+00	\N	1
97	1	1699448625.519782_frame.jpg	2023-11-08 13:03:45.81062+00	2023-11-08 13:03:45.810647+00	\N	1
98	1	1699448746.226834_frame.jpg	2023-11-08 13:05:46.520593+00	2023-11-08 13:05:46.520618+00	\N	1
99	1	1699448865.672541_frame.jpg	2023-11-08 13:07:45.96644+00	2023-11-08 13:07:45.966466+00	\N	1
100	1	1699448935.011083_frame.jpg	2023-11-08 13:08:55.862199+00	2023-11-08 13:08:55.862226+00	\N	1
101	1	1699449052.855547_frame.jpg	2023-11-08 13:10:53.158425+00	2023-11-08 13:10:53.158451+00	\N	1
102	1	1699449123.567494_frame.jpg	2023-11-08 13:12:03.869675+00	2023-11-08 13:12:03.869701+00	\N	1
103	1	1699449199.196485_frame.jpg	2023-11-08 13:13:19.504034+00	2023-11-08 13:13:19.504062+00	\N	1
104	1	1699449323.16691_frame.jpg	2023-11-08 13:15:23.487599+00	2023-11-08 13:15:23.487626+00	\N	1
105	1	1699449398.130155_frame.jpg	2023-11-08 13:16:38.505696+00	2023-11-08 13:16:38.505722+00	\N	1
106	1	1699449517.245803_frame.jpg	2023-11-08 13:18:37.928407+00	2023-11-08 13:18:37.928431+00	\N	1
107	1	1699449636.314547_frame.jpg	2023-11-08 13:20:36.920373+00	2023-11-08 13:20:36.920399+00	\N	1
108	1	1699449754.339112_frame.jpg	2023-11-08 13:22:34.661145+00	2023-11-08 13:22:34.661171+00	\N	1
109	1	1699449825.296743_frame.jpg	2023-11-08 13:23:45.624176+00	2023-11-08 13:23:45.624203+00	\N	1
110	1	1699449949.916609_frame.jpg	2023-11-08 13:25:50.244321+00	2023-11-08 13:25:50.244346+00	\N	1
111	1	1699450069.197453_frame.jpg	2023-11-08 13:27:49.531964+00	2023-11-08 13:27:49.531989+00	\N	1
112	1	1699450140.011056_frame.jpg	2023-11-08 13:29:00.648234+00	2023-11-08 13:29:00.648263+00	\N	1
113	1	1699450257.612502_frame.jpg	2023-11-08 13:30:57.943526+00	2023-11-08 13:30:57.943553+00	\N	1
114	1	1699450329.410861_frame.jpg	2023-11-08 13:32:09.753694+00	2023-11-08 13:32:09.75372+00	\N	1
115	1	1699450398.090568_frame.jpg	2023-11-08 13:33:18.425827+00	2023-11-08 13:33:18.425857+00	\N	1
116	1	1699450471.465356_frame.jpg	2023-11-08 13:34:31.803279+00	2023-11-08 13:34:31.803306+00	\N	1
117	1	1699450591.125825_frame.jpg	2023-11-08 13:36:31.463354+00	2023-11-08 13:36:31.46338+00	\N	1
118	1	1699450702.365358_frame.jpg	2023-11-08 13:38:22.708513+00	2023-11-08 13:38:22.708548+00	\N	1
119	1	1699462983.255425_frame.jpg	2023-11-08 17:03:03.621784+00	2023-11-08 17:03:03.621819+00	\N	1
120	1	1699463054.642244_frame.jpg	2023-11-08 17:04:14.998756+00	2023-11-08 17:04:14.998781+00	\N	1
121	1	1699495746.567034_frame.jpg	2023-11-09 02:09:06.918593+00	2023-11-09 02:09:06.918618+00	\N	1
122	1	1699495999.908086_frame.jpg	2023-11-09 02:13:20.273212+00	2023-11-09 02:13:20.273239+00	\N	1
123	1	1699496252.944808_frame.jpg	2023-11-09 02:17:33.642547+00	2023-11-09 02:17:33.642573+00	\N	1
124	1	1699496397.265212_frame.jpg	2023-11-09 02:19:57.618979+00	2023-11-09 02:19:57.619004+00	\N	1
125	1	1699496533.096724_frame.jpg	2023-11-09 02:22:13.452643+00	2023-11-09 02:22:13.452677+00	\N	1
126	1	1699496630.654882_frame.jpg	2023-11-09 02:23:51.015193+00	2023-11-09 02:23:51.015219+00	\N	1
127	1	1699496759.540162_frame.jpg	2023-11-09 02:26:00.288623+00	2023-11-09 02:26:00.288658+00	\N	1
128	1	1699496888.006381_frame.jpg	2023-11-09 02:28:08.369876+00	2023-11-09 02:28:08.369973+00	\N	1
129	1	1699497021.700368_frame.jpg	2023-11-09 02:30:22.074914+00	2023-11-09 02:30:22.07494+00	\N	1
130	1	1699497148.462717_frame.jpg	2023-11-09 02:32:28.848264+00	2023-11-09 02:32:28.84829+00	\N	1
131	1	1699497278.031318_frame.jpg	2023-11-09 02:34:38.773227+00	2023-11-09 02:34:38.773253+00	\N	1
132	1	1699497405.295497_frame.jpg	2023-11-09 02:36:45.676537+00	2023-11-09 02:36:45.676561+00	\N	1
133	1	1699497485.635316_frame.jpg	2023-11-09 02:38:06.025794+00	2023-11-09 02:38:06.025871+00	\N	1
134	1	1699497565.55359_frame.jpg	2023-11-09 02:39:26.310689+00	2023-11-09 02:39:26.310715+00	\N	1
135	1	1699497695.277046_frame.jpg	2023-11-09 02:41:35.663902+00	2023-11-09 02:41:35.663929+00	\N	1
136	1	1699497773.948287_frame.jpg	2023-11-09 02:42:54.333528+00	2023-11-09 02:42:54.333564+00	\N	1
137	1	1699497853.787536_frame.jpg	2023-11-09 02:44:14.3935+00	2023-11-09 02:44:14.393527+00	\N	1
138	1	1699497982.744662_frame.jpg	2023-11-09 02:46:23.359775+00	2023-11-09 02:46:23.359811+00	\N	1
139	1	1699498061.694915_frame.jpg	2023-11-09 02:47:42.088746+00	2023-11-09 02:47:42.088772+00	\N	1
140	1	1699498139.686583_frame.jpg	2023-11-09 02:49:00.095566+00	2023-11-09 02:49:00.095594+00	\N	1
141	1	1699498217.741548_frame.jpg	2023-11-09 02:50:18.144221+00	2023-11-09 02:50:18.144247+00	\N	1
142	1	1699498296.81948_frame.jpg	2023-11-09 02:51:37.934832+00	2023-11-09 02:51:37.934857+00	\N	1
143	1	1699498431.716045_frame.jpg	2023-11-09 02:53:52.136325+00	2023-11-09 02:53:52.13636+00	\N	1
144	1	1699498559.651479_frame.jpg	2023-11-09 02:56:00.480243+00	2023-11-09 02:56:00.480271+00	\N	1
145	1	1699498639.499184_frame.jpg	2023-11-09 02:57:19.924941+00	2023-11-09 02:57:19.924967+00	\N	1
146	1	1699498717.729555_frame.jpg	2023-11-09 02:58:38.154047+00	2023-11-09 02:58:38.154082+00	\N	1
147	1	1699498796.062809_frame.jpg	2023-11-09 02:59:56.480433+00	2023-11-09 02:59:56.480469+00	\N	1
148	1	1699498874.266891_frame.jpg	2023-11-09 03:01:14.674041+00	2023-11-09 03:01:14.674067+00	\N	1
149	1	1699498999.579805_frame.jpg	2023-11-09 03:03:20.005831+00	2023-11-09 03:03:20.005856+00	\N	1
150	1	1699499077.747566_frame.jpg	2023-11-09 03:04:38.75347+00	2023-11-09 03:04:38.753496+00	\N	1
151	1	1699499156.520436_frame.jpg	2023-11-09 03:05:57.478894+00	2023-11-09 03:05:57.47892+00	\N	1
152	1	1699499285.260345_frame.jpg	2023-11-09 03:08:05.681319+00	2023-11-09 03:08:05.681346+00	\N	1
153	1	1699499363.142927_frame.jpg	2023-11-09 03:09:23.580351+00	2023-11-09 03:09:23.580377+00	\N	1
154	1	1699499492.39493_frame.jpg	2023-11-09 03:11:33.062948+00	2023-11-09 03:11:33.062979+00	\N	1
155	1	1699499571.62344_frame.jpg	2023-11-09 03:12:52.0469+00	2023-11-09 03:12:52.046927+00	\N	1
156	1	1699499698.572159_frame.jpg	2023-11-09 03:14:59.023875+00	2023-11-09 03:14:59.0239+00	\N	1
157	1	1699499782.03623_frame.jpg	2023-11-09 03:16:22.470565+00	2023-11-09 03:16:22.47059+00	\N	1
158	1	1699499860.727647_frame.jpg	2023-11-09 03:17:41.156422+00	2023-11-09 03:17:41.156449+00	\N	1
159	1	1699499939.06322_frame.jpg	2023-11-09 03:18:59.497459+00	2023-11-09 03:18:59.497485+00	\N	1
160	1	1699500017.91713_frame.jpg	2023-11-09 03:20:18.353086+00	2023-11-09 03:20:18.353112+00	\N	1
161	1	1699500148.82574_frame.jpg	2023-11-09 03:22:29.289177+00	2023-11-09 03:22:29.289212+00	\N	1
162	1	1699500227.221608_frame.jpg	2023-11-09 03:23:47.672175+00	2023-11-09 03:23:47.672201+00	\N	1
163	1	1699500305.414601_frame.jpg	2023-11-09 03:25:05.877116+00	2023-11-09 03:25:05.877142+00	\N	1
164	1	1699500384.022332_frame.jpg	2023-11-09 03:26:24.659003+00	2023-11-09 03:26:24.65903+00	\N	1
165	1	1699500462.545579_frame.jpg	2023-11-09 03:27:42.997276+00	2023-11-09 03:27:42.997302+00	\N	1
166	1	1699500591.205553_frame.jpg	2023-11-09 03:29:51.684319+00	2023-11-09 03:29:51.684344+00	\N	1
167	1	1699500673.681709_frame.jpg	2023-11-09 03:31:14.1623+00	2023-11-09 03:31:14.162326+00	\N	1
168	1	1699500752.713154_frame.jpg	2023-11-09 03:32:33.886917+00	2023-11-09 03:32:33.886943+00	\N	1
169	1	1699500881.667192_frame.jpg	2023-11-09 03:34:42.137402+00	2023-11-09 03:34:42.137428+00	\N	1
170	1	1699500959.749525_frame.jpg	2023-11-09 03:36:00.274075+00	2023-11-09 03:36:00.274102+00	\N	1
171	1	1699501038.119436_frame.jpg	2023-11-09 03:37:18.601591+00	2023-11-09 03:37:18.601617+00	\N	1
172	1	1699501115.994322_frame.jpg	2023-11-09 03:38:36.481062+00	2023-11-09 03:38:36.481087+00	\N	1
173	1	1699501194.973459_frame.jpg	2023-11-09 03:39:55.456504+00	2023-11-09 03:39:55.45653+00	\N	1
174	1	1699501273.511637_frame.jpg	2023-11-09 03:41:14.631447+00	2023-11-09 03:41:14.631472+00	\N	1
175	1	1699501354.707809_frame.jpg	2023-11-09 03:42:35.197452+00	2023-11-09 03:42:35.197478+00	\N	1
\.


--
-- TOC entry 3474 (class 0 OID 16403)
-- Dependencies: 220
-- Data for Name: Face; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Face" (face_id, "FrameFilePath", "X", "Y", "Width", "Height", created_at, updated_at, person_id) FROM stdin;
1	uuid4_string.jpg	227.42	243.3	42	42	2023-11-08 09:26:32.394765+00	2023-11-08 09:26:32.394797+00	\N
2	uuid4_string.jpg	227.42	243.3	42	42	2023-11-08 09:26:33.623062+00	2023-11-08 09:26:33.623093+00	\N
3	uuid4_string.jpg	227.42	243.3	42	42	2023-11-08 09:26:36.371773+00	2023-11-08 09:26:36.371804+00	\N
\.


--
-- TOC entry 3484 (class 0 OID 16485)
-- Dependencies: 230
-- Data for Name: Log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Log" (log_id, created_at, updated_at, camera_id, face_id) FROM stdin;
\.


--
-- TOC entry 3472 (class 0 OID 16392)
-- Dependencies: 218
-- Data for Name: Person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Person" (person_id, name, gender, dob, phone, avatar_url, "position", created_at, updated_at) FROM stdin;
1	NghiaNN	0	1973-03-03 01:45:00+00	0 xxx-xxx-xxx  	http://103.157.218.126:32000/blob/1699501197.539942_nghia.jpg	Software Engineering	2023-11-09 02:43:07.488947+00	2023-11-09 02:43:07.488964+00
\.


--
-- TOC entry 3476 (class 0 OID 16419)
-- Dependencies: 222
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."User" (user_id, created_at, updated_at, name, username, password, manager, person_id) FROM stdin;
\.


--
-- TOC entry 3478 (class 0 OID 16439)
-- Dependencies: 224
-- Data for Name: Zone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Zone" (zone_id, name, description, placeholder_url, created_at, updated_at) FROM stdin;
1	Zone 1	Zone 1 Description	1699500813.164776_z1onez.jpg	2023-11-08 09:37:34.394+00	2023-11-08 09:37:34.39403+00
2	Zone 2	Zone 2 Description	1699500960.331858_zone2.jpg	2023-11-08 09:37:34.435604+00	2023-11-08 09:37:34.435604+00
\.


--
-- TOC entry 3490 (class 0 OID 16534)
-- Dependencies: 236
-- Data for Name: ZoneSetting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ZoneSetting" (id, name, description, config, zone_id) FROM stdin;
\.


--
-- TOC entry 3492 (class 0 OID 16548)
-- Dependencies: 238
-- Data for Name: aerich; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aerich (id, version, app, content) FROM stdin;
1	2_20231107141339_None.py	models	{"models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.LogModel": {"app": "models", "name": "models.LogModel", "table": "Log", "indexes": [], "abstract": false, "pk_field": {"name": "log_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "log_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based log model.", "fk_fields": [{"name": "camera", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "camera_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.ZoneModel", "db_constraint": true}, {"name": "face", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "face_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.FaceModel", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "camera_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "camera_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "face_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "face_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Tortoise-based log model.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.FaceModel": {"app": "models", "name": "models.FaceModel", "table": "Face", "indexes": [], "abstract": false, "pk_field": {"name": "face_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "face_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based log model.", "fk_fields": [{"name": "person", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "person_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.PersonModel", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "FrameFilePath", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "FrameFilePath", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "X", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "X", "docstring": null, "generated": false, "field_type": "FloatField", "constraints": {}, "description": null, "python_type": "float", "db_field_types": {"": "DOUBLE PRECISION", "mysql": "DOUBLE", "sqlite": "REAL"}}, {"name": "Y", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "Y", "docstring": null, "generated": false, "field_type": "FloatField", "constraints": {}, "description": null, "python_type": "float", "db_field_types": {"": "DOUBLE PRECISION", "mysql": "DOUBLE", "sqlite": "REAL"}}, {"name": "Width", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "Width", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "Height", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "Height", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "person_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "person_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Tortoise-based log model.", "unique_together": [], "backward_fk_fields": [{"name": "facemodel_tracking", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.AttendaceTrackingModel", "db_constraint": true}, {"name": "facemodel", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.LogModel", "db_constraint": true}, {"name": "face_detected", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.EventLogModel", "db_constraint": true}], "backward_o2o_fields": []}, "models.UserModel": {"app": "models", "name": "models.UserModel", "table": "User", "indexes": [], "abstract": false, "pk_field": {"name": "user_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "user_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Data model for user.", "fk_fields": [], "m2m_fields": [], "o2o_fields": [{"name": "person", "unique": true, "default": null, "indexed": true, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "person_id", "field_type": "OneToOneFieldInstance", "constraints": {}, "description": null, "python_type": "models.PersonModel", "db_constraint": true}], "data_fields": [{"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 200}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(200)"}}, {"name": "username", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "username", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 200}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(200)"}}, {"name": "password", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 200}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(200)"}}, {"name": "manager", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "manager", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "person_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "person_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Data model for user.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ZoneModel": {"app": "models", "name": "models.ZoneModel", "table": "Zone", "indexes": [], "abstract": false, "pk_field": {"name": "zone_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "zone_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based zone model.", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "placeholder_url", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "placeholder_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}], "description": "Tortoise-based zone model.", "unique_together": [], "backward_fk_fields": [{"name": "cameramodel_attendance", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.AttendaceTrackingModel", "db_constraint": true}, {"name": "Cameras", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.CameraModel", "db_constraint": true}, {"name": "cameramodel", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.LogModel", "db_constraint": true}, {"name": "zone_setting_zone", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.ZoneSettingModel", "db_constraint": true}], "backward_o2o_fields": []}, "models.DummyModel": {"app": "models", "name": "models.DummyModel", "table": "dummymodel", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Model for demo purpose.", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 200}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(200)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 155}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(155)"}}], "description": "Model for demo purpose.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.EventModel": {"app": "models", "name": "models.EventModel", "table": "Event", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based log model.", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}], "description": "Tortoise-based log model.", "unique_together": [], "backward_fk_fields": [{"name": "log_event", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.EventLogModel", "db_constraint": true}], "backward_o2o_fields": []}, "models.CameraModel": {"app": "models", "name": "models.CameraModel", "table": "Camera", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based camera model.", "fk_fields": [{"name": "zone", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "zone_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.ZoneModel", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 256}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(256)"}}, {"name": "connect_uri", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "connect_uri", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 256}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(256)"}}, {"name": "placeholder_url", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "placeholder_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "type", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "type", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "zone_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "zone_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Tortoise-based camera model.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.PersonModel": {"app": "models", "name": "models.PersonModel", "table": "Person", "indexes": [], "abstract": false, "pk_field": {"name": "person_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "person_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based log model.", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "gender", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "gender", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "dob", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": true, "db_column": "dob", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {}, "description": null, "python_type": "datetime.datetime", "auto_now_add": false, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "phone", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 15}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(15)"}}, {"name": "avatar_url", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "avatar_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "position", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "position", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}], "description": "Tortoise-based log model.", "unique_together": [], "backward_fk_fields": [{"name": "person_model", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.FaceModel", "db_constraint": true}], "backward_o2o_fields": [{"name": "user_person", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardOneToOneRelation", "constraints": {}, "description": null, "python_type": "models.UserModel", "db_constraint": true}]}, "models.EventLogModel": {"app": "models", "name": "models.EventLogModel", "table": "EventLog", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based log model.", "fk_fields": [{"name": "event", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "event_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.EventModel", "db_constraint": true}, {"name": "face", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "face_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.FaceModel", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "video_url", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "video_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "image_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "image_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "event_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "event_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "face_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "face_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Tortoise-based log model.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ZoneSettingModel": {"app": "models", "name": "models.ZoneSettingModel", "table": "ZoneSetting", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Model for demo purpose.", "fk_fields": [{"name": "zone", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "zone_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.ZoneModel", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "config", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "config", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "zone_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "zone_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Model for demo purpose.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.AttendaceTrackingModel": {"app": "models", "name": "models.AttendaceTrackingModel", "table": "AttendanceTracking", "indexes": [], "abstract": false, "pk_field": {"name": "tracking_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "tracking_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": "Tortoise-based log model.", "fk_fields": [{"name": "camera", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "camera_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.ZoneModel", "db_constraint": true}, {"name": "face", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "face_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.FaceModel", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "camera_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "camera_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "face_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "face_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "Tortoise-based log model.", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}}
\.


--
-- TOC entry 3470 (class 0 OID 16385)
-- Dependencies: 216
-- Data for Name: dummymodel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dummymodel (id, name, description) FROM stdin;
\.


--
-- TOC entry 3522 (class 0 OID 0)
-- Dependencies: 225
-- Name: AttendanceTracking_tracking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."AttendanceTracking_tracking_id_seq"', 1, false);


--
-- TOC entry 3523 (class 0 OID 0)
-- Dependencies: 227
-- Name: Camera_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Camera_id_seq"', 3, true);


--
-- TOC entry 3524 (class 0 OID 0)
-- Dependencies: 233
-- Name: EventLog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."EventLog_id_seq"', 175, true);


--
-- TOC entry 3525 (class 0 OID 0)
-- Dependencies: 231
-- Name: Event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Event_id_seq"', 3, true);


--
-- TOC entry 3526 (class 0 OID 0)
-- Dependencies: 219
-- Name: Face_face_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Face_face_id_seq"', 3, true);


--
-- TOC entry 3527 (class 0 OID 0)
-- Dependencies: 229
-- Name: Log_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Log_log_id_seq"', 1, false);


--
-- TOC entry 3528 (class 0 OID 0)
-- Dependencies: 217
-- Name: Person_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Person_person_id_seq"', 1, true);


--
-- TOC entry 3529 (class 0 OID 0)
-- Dependencies: 221
-- Name: User_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_user_id_seq"', 1, false);


--
-- TOC entry 3530 (class 0 OID 0)
-- Dependencies: 235
-- Name: ZoneSetting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."ZoneSetting_id_seq"', 1, false);


--
-- TOC entry 3531 (class 0 OID 0)
-- Dependencies: 223
-- Name: Zone_zone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Zone_zone_id_seq"', 2, true);


--
-- TOC entry 3532 (class 0 OID 0)
-- Dependencies: 237
-- Name: aerich_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aerich_id_seq', 1, true);


--
-- TOC entry 3533 (class 0 OID 0)
-- Dependencies: 215
-- Name: dummymodel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dummymodel_id_seq', 1, false);


--
-- TOC entry 3303 (class 2606 OID 16457)
-- Name: AttendanceTracking AttendanceTracking_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AttendanceTracking"
    ADD CONSTRAINT "AttendanceTracking_pkey" PRIMARY KEY (tracking_id);


--
-- TOC entry 3305 (class 2606 OID 16478)
-- Name: Camera Camera_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Camera"
    ADD CONSTRAINT "Camera_pkey" PRIMARY KEY (id);


--
-- TOC entry 3311 (class 2606 OID 16522)
-- Name: EventLog EventLog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventLog"
    ADD CONSTRAINT "EventLog_pkey" PRIMARY KEY (id);


--
-- TOC entry 3309 (class 2606 OID 16511)
-- Name: Event Event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (id);


--
-- TOC entry 3293 (class 2606 OID 16412)
-- Name: Face Face_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Face"
    ADD CONSTRAINT "Face_pkey" PRIMARY KEY (face_id);


--
-- TOC entry 3307 (class 2606 OID 16492)
-- Name: Log Log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Log"
    ADD CONSTRAINT "Log_pkey" PRIMARY KEY (log_id);


--
-- TOC entry 3291 (class 2606 OID 16401)
-- Name: Person Person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Person"
    ADD CONSTRAINT "Person_pkey" PRIMARY KEY (person_id);


--
-- TOC entry 3295 (class 2606 OID 16432)
-- Name: User User_person_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_person_id_key" UNIQUE (person_id);


--
-- TOC entry 3297 (class 2606 OID 16428)
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);


--
-- TOC entry 3299 (class 2606 OID 16430)
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- TOC entry 3313 (class 2606 OID 16541)
-- Name: ZoneSetting ZoneSetting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ZoneSetting"
    ADD CONSTRAINT "ZoneSetting_pkey" PRIMARY KEY (id);


--
-- TOC entry 3301 (class 2606 OID 16448)
-- Name: Zone Zone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Zone"
    ADD CONSTRAINT "Zone_pkey" PRIMARY KEY (zone_id);


--
-- TOC entry 3315 (class 2606 OID 16555)
-- Name: aerich aerich_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aerich
    ADD CONSTRAINT aerich_pkey PRIMARY KEY (id);


--
-- TOC entry 3289 (class 2606 OID 16390)
-- Name: dummymodel dummymodel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dummymodel
    ADD CONSTRAINT dummymodel_pkey PRIMARY KEY (id);


--
-- TOC entry 3318 (class 2606 OID 16458)
-- Name: AttendanceTracking AttendanceTracking_camera_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AttendanceTracking"
    ADD CONSTRAINT "AttendanceTracking_camera_id_fkey" FOREIGN KEY (camera_id) REFERENCES public."Zone"(zone_id) ON DELETE CASCADE;


--
-- TOC entry 3319 (class 2606 OID 16463)
-- Name: AttendanceTracking AttendanceTracking_face_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AttendanceTracking"
    ADD CONSTRAINT "AttendanceTracking_face_id_fkey" FOREIGN KEY (face_id) REFERENCES public."Face"(face_id) ON DELETE CASCADE;


--
-- TOC entry 3320 (class 2606 OID 16479)
-- Name: Camera Camera_zone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Camera"
    ADD CONSTRAINT "Camera_zone_id_fkey" FOREIGN KEY (zone_id) REFERENCES public."Zone"(zone_id) ON DELETE CASCADE;


--
-- TOC entry 3323 (class 2606 OID 16523)
-- Name: EventLog EventLog_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventLog"
    ADD CONSTRAINT "EventLog_event_id_fkey" FOREIGN KEY (event_id) REFERENCES public."Event"(id) ON DELETE CASCADE;


--
-- TOC entry 3324 (class 2606 OID 16528)
-- Name: EventLog EventLog_face_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventLog"
    ADD CONSTRAINT "EventLog_face_id_fkey" FOREIGN KEY (face_id) REFERENCES public."Face"(face_id) ON DELETE CASCADE;


--
-- TOC entry 3316 (class 2606 OID 16413)
-- Name: Face Face_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Face"
    ADD CONSTRAINT "Face_person_id_fkey" FOREIGN KEY (person_id) REFERENCES public."Person"(person_id) ON DELETE CASCADE;


--
-- TOC entry 3321 (class 2606 OID 16493)
-- Name: Log Log_camera_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Log"
    ADD CONSTRAINT "Log_camera_id_fkey" FOREIGN KEY (camera_id) REFERENCES public."Zone"(zone_id) ON DELETE CASCADE;


--
-- TOC entry 3322 (class 2606 OID 16498)
-- Name: Log Log_face_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Log"
    ADD CONSTRAINT "Log_face_id_fkey" FOREIGN KEY (face_id) REFERENCES public."Face"(face_id) ON DELETE CASCADE;


--
-- TOC entry 3317 (class 2606 OID 16433)
-- Name: User User_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_person_id_fkey" FOREIGN KEY (person_id) REFERENCES public."Person"(person_id) ON DELETE CASCADE;


--
-- TOC entry 3325 (class 2606 OID 16542)
-- Name: ZoneSetting ZoneSetting_zone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ZoneSetting"
    ADD CONSTRAINT "ZoneSetting_zone_id_fkey" FOREIGN KEY (zone_id) REFERENCES public."Zone"(zone_id) ON DELETE CASCADE;


-- Completed on 2023-11-09 10:52:14 +07

--
-- PostgreSQL database dump complete
--

