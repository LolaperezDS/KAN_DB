--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: eventlogtable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventlogtable (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    message text NOT NULL,
    kpd_diff integer NOT NULL,
    event_target_id integer NOT NULL,
    event_initiator_id integer,
    event_type_id integer
);


ALTER TABLE public.eventlogtable OWNER TO postgres;

--
-- Name: eventlogtable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eventlogtable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eventlogtable_id_seq OWNER TO postgres;

--
-- Name: eventlogtable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eventlogtable_id_seq OWNED BY public.eventlogtable.id;


--
-- Name: eventtypetable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventtypetable (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.eventtypetable OWNER TO postgres;

--
-- Name: eventtypetable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eventtypetable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eventtypetable_id_seq OWNER TO postgres;

--
-- Name: eventtypetable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eventtypetable_id_seq OWNED BY public.eventtypetable.id;


--
-- Name: feedbacktable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feedbacktable (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    message text NOT NULL,
    feedback_score integer,
    initiator_id integer
);


ALTER TABLE public.feedbacktable OWNER TO postgres;

--
-- Name: feedbacktable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feedbacktable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feedbacktable_id_seq OWNER TO postgres;

--
-- Name: feedbacktable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feedbacktable_id_seq OWNED BY public.feedbacktable.id;


--
-- Name: imagetable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.imagetable (
    id integer NOT NULL,
    image_id character varying(128) NOT NULL,
    event_id integer
);


ALTER TABLE public.imagetable OWNER TO postgres;

--
-- Name: imagetable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.imagetable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.imagetable_id_seq OWNER TO postgres;

--
-- Name: imagetable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.imagetable_id_seq OWNED BY public.imagetable.id;


--
-- Name: notificationtable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notificationtable (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    event_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    remind_hours integer NOT NULL,
    message text NOT NULL,
    is_notificated boolean DEFAULT false NOT NULL,
    initiator_id integer
);


ALTER TABLE public.notificationtable OWNER TO postgres;

--
-- Name: notificationtable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notificationtable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notificationtable_id_seq OWNER TO postgres;

--
-- Name: notificationtable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notificationtable_id_seq OWNED BY public.notificationtable.id;


--
-- Name: roletable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roletable (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    acsess_level integer NOT NULL
);


ALTER TABLE public.roletable OWNER TO postgres;

--
-- Name: roletable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roletable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roletable_id_seq OWNER TO postgres;

--
-- Name: roletable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roletable_id_seq OWNED BY public.roletable.id;


--
-- Name: roomtable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roomtable (
    id integer NOT NULL,
    number character varying(8) NOT NULL
);


ALTER TABLE public.roomtable OWNER TO postgres;

--
-- Name: roomtable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roomtable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roomtable_id_seq OWNER TO postgres;

--
-- Name: roomtable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roomtable_id_seq OWNED BY public.roomtable.id;


--
-- Name: sankomtable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sankomtable (
    id integer NOT NULL,
    mark integer,
    initiator_id integer,
    room_id integer
);


ALTER TABLE public.sankomtable OWNER TO postgres;

--
-- Name: sankomtable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sankomtable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sankomtable_id_seq OWNER TO postgres;

--
-- Name: sankomtable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sankomtable_id_seq OWNED BY public.sankomtable.id;


--
-- Name: usertable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usertable (
    id integer NOT NULL,
    student_id integer NOT NULL,
    is_active boolean NOT NULL,
    tg_id character varying(32),
    login character varying(32) NOT NULL,
    password character varying(64) NOT NULL,
    name character varying(32) NOT NULL,
    sname character varying(32) NOT NULL,
    kpd_score integer NOT NULL,
    role_id integer,
    room_id integer
);


ALTER TABLE public.usertable OWNER TO postgres;

--
-- Name: usertable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usertable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usertable_id_seq OWNER TO postgres;

--
-- Name: usertable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usertable_id_seq OWNED BY public.usertable.id;


--
-- Name: worktickettable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.worktickettable (
    id integer NOT NULL,
    creator integer NOT NULL,
    deadline timestamp without time zone NOT NULL,
    kpd_rollback integer NOT NULL,
    ticket_hash character varying(256) NOT NULL,
    text_task text NOT NULL,
    performer_id integer
);


ALTER TABLE public.worktickettable OWNER TO postgres;

--
-- Name: worktickettable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.worktickettable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.worktickettable_id_seq OWNER TO postgres;

--
-- Name: worktickettable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.worktickettable_id_seq OWNED BY public.worktickettable.id;


--
-- Name: eventlogtable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventlogtable ALTER COLUMN id SET DEFAULT nextval('public.eventlogtable_id_seq'::regclass);


--
-- Name: eventtypetable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventtypetable ALTER COLUMN id SET DEFAULT nextval('public.eventtypetable_id_seq'::regclass);


--
-- Name: feedbacktable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedbacktable ALTER COLUMN id SET DEFAULT nextval('public.feedbacktable_id_seq'::regclass);


--
-- Name: imagetable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagetable ALTER COLUMN id SET DEFAULT nextval('public.imagetable_id_seq'::regclass);


--
-- Name: notificationtable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificationtable ALTER COLUMN id SET DEFAULT nextval('public.notificationtable_id_seq'::regclass);


--
-- Name: roletable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roletable ALTER COLUMN id SET DEFAULT nextval('public.roletable_id_seq'::regclass);


--
-- Name: roomtable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomtable ALTER COLUMN id SET DEFAULT nextval('public.roomtable_id_seq'::regclass);


--
-- Name: sankomtable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sankomtable ALTER COLUMN id SET DEFAULT nextval('public.sankomtable_id_seq'::regclass);


--
-- Name: usertable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable ALTER COLUMN id SET DEFAULT nextval('public.usertable_id_seq'::regclass);


--
-- Name: worktickettable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worktickettable ALTER COLUMN id SET DEFAULT nextval('public.worktickettable_id_seq'::regclass);


--
-- Data for Name: eventlogtable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eventlogtable (id, created_at, message, kpd_diff, event_target_id, event_initiator_id, event_type_id) FROM stdin;
\.


--
-- Data for Name: eventtypetable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eventtypetable (id, name) FROM stdin;
3	Sanitary
4	GRO
5	Cheat
6	Other
\.


--
-- Data for Name: feedbacktable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feedbacktable (id, created_at, message, feedback_score, initiator_id) FROM stdin;
\.


--
-- Data for Name: imagetable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.imagetable (id, image_id, event_id) FROM stdin;
\.


--
-- Data for Name: notificationtable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notificationtable (id, created_at, event_date, remind_hours, message, is_notificated, initiator_id) FROM stdin;
\.


--
-- Data for Name: roletable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roletable (id, name, acsess_level) FROM stdin;
1	Student	1
4	Sanitary	3
5	GRO	3
6	Admin	5
\.


--
-- Data for Name: roomtable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roomtable (id, number) FROM stdin;
721	101S
722	101L
723	102S
724	102L
725	103S
726	103L
727	104S
728	104L
729	105S
730	105L
731	106S
732	106L
733	107S
734	107L
735	108S
736	108L
737	109S
738	109L
739	110S
740	110L
741	111S
742	111L
743	112S
744	112L
745	113S
746	113L
747	114S
748	114L
749	115S
750	115L
751	116S
752	116L
753	117S
754	117L
755	201S
756	201L
757	202S
758	202L
759	203S
760	203L
761	204S
762	204L
763	205S
764	205L
765	206S
766	206L
767	207S
768	207L
769	208S
770	208L
771	209S
772	209L
773	210S
774	210L
775	211S
776	211L
777	212S
778	212L
779	213S
780	213L
781	214S
782	214L
783	215S
784	215L
785	216S
786	216L
787	217S
788	217L
789	301S
790	301L
791	302S
792	302L
793	303S
794	303L
795	304S
796	304L
797	305S
798	305L
799	306S
800	306L
801	307S
802	307L
803	308S
804	308L
805	309S
806	309L
807	310S
808	310L
809	311S
810	311L
811	312S
812	312L
813	313S
814	313L
815	314S
816	314L
817	315S
818	315L
819	316S
820	316L
821	317S
822	317L
823	401S
824	401L
825	402S
826	402L
827	403S
828	403L
829	404S
830	404L
831	405S
832	405L
833	406S
834	406L
835	407S
836	407L
837	408S
838	408L
839	409S
840	409L
841	410S
842	410L
843	411S
844	411L
845	412S
846	412L
847	413S
848	413L
849	414S
850	414L
851	415S
852	415L
853	416S
854	416L
855	417S
856	417L
857	501S
858	501L
859	502S
860	502L
861	503S
862	503L
863	504S
864	504L
865	505S
866	505L
867	506S
868	506L
869	507S
870	507L
871	508S
872	508L
873	509S
874	509L
875	510S
876	510L
877	511S
878	511L
879	512S
880	512L
881	513S
882	513L
883	514S
884	514L
885	515S
886	515L
887	516S
888	516L
889	517S
890	517L
891	601S
892	601L
893	602S
894	602L
895	603S
896	603L
897	604S
898	604L
899	605S
900	605L
901	606S
902	606L
903	607S
904	607L
905	608S
906	608L
907	609S
908	609L
909	610S
910	610L
911	611S
912	611L
913	612S
914	612L
915	613S
916	613L
917	614S
918	614L
919	615S
920	615L
921	616S
922	616L
923	617S
924	617L
925	701S
926	701L
927	702S
928	702L
929	703S
930	703L
931	704S
932	704L
933	705S
934	705L
935	706S
936	706L
937	707S
938	707L
939	708S
940	708L
941	709S
942	709L
943	710S
944	710L
945	711S
946	711L
947	712S
948	712L
949	713S
950	713L
951	714S
952	714L
953	715S
954	715L
955	716S
956	716L
957	717S
958	717L
959	801S
960	801L
961	802S
962	802L
963	803S
964	803L
965	804S
966	804L
967	805S
968	805L
969	806S
970	806L
971	807S
972	807L
973	808S
974	808L
975	809S
976	809L
977	810S
978	810L
979	811S
980	811L
981	812S
982	812L
983	813S
984	813L
985	814S
986	814L
987	815S
988	815L
989	816S
990	816L
991	817S
992	817L
993	901S
994	901L
995	902S
996	902L
997	903S
998	903L
999	904S
1000	904L
1001	905S
1002	905L
1003	906S
1004	906L
1005	907S
1006	907L
1007	908S
1008	908L
1009	909S
1010	909L
1011	910S
1012	910L
1013	911S
1014	911L
1015	912S
1016	912L
1017	913S
1018	913L
1019	914S
1020	914L
1021	915S
1022	915L
1023	916S
1024	916L
1025	917S
1026	917L
\.


--
-- Data for Name: sankomtable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sankomtable (id, mark, initiator_id, room_id) FROM stdin;
\.


--
-- Data for Name: usertable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usertable (id, student_id, is_active, tg_id, login, password, name, sname, kpd_score, role_id, room_id) FROM stdin;
3	2032145	t	\N	6ttCiiH8	EjBd3H1R	Данил	Журавлев	0	1	959
4	1912022	t	\N	9i72F8v0	GVpIRP9q	Ильгиз	Хадиев	0	1	1023
5	2032082	t	\N	jI9lFTcX	S2N72i4S	Динар	Муллагалиев	0	1	983
6	2032059	t	\N	JypbGmrw	DSVzlOVS	Павел	Андреев	0	1	983
7	2032005	t	\N	i9AMAIGf	TETmWZ0C	София	Валегжанина	0	1	995
8	2032080	t	\N	JYAjAY8o	srbcetxs	Ильвина	Миннекаева	0	1	739
9	132175	t	\N	akTVhdje	wtFNblvw	Данил	Габитов	0	1	820
10	132134	t	\N	gimqGY7r	z3gympXj	Виктор	Таранов	0	1	971
11	2032069	t	\N	jWSNbJoP	norlhTId	Рафаэль	Гилемханов	0	1	888
12	2032042	t	\N	gSb2Mozc	ybGEa9aI	Алина	Галиева	0	1	1005
13	2032056	t	\N	KGS0aEN1	vV5sIWRy	Татьяна	Соколова	0	1	1005
14	2032091	t	\N	KfhB9AN6	We7iGrqq	Роман	Фомин	0	1	1018
15	2032186	t	\N	dXOPJnp3	U1EGK3sD	Ксения	Шистерова	0	1	903
16	2032048	t	\N	KV7GHQxm	sCpCZnxD	Ирина	Невкина	0	1	996
17	2032078	t	\N	HoscT7Ls	KdkBPzVm	Данил	Львов	0	1	888
18	2032175	t	\N	BfT77fJ3	QfwPiFmr	Вадим	Сухарников	0	1	1003
19	2032122	t	\N	NG8avba1	OOAE5a9T	Карина	Сидикова	0	1	964
20	2032123	t	\N	XQQQyef4	iGOyv28A	Арина	Таратунина	0	1	902
21	2032043	t	\N	Td43PxBk	P8idlV7o	Камила	Галиева	0	1	919
22	2032143	t	\N	DyUaOtx9	Q6ZLV0bL	Алексей	Егоров	0	1	959
23	2032089	t	\N	qcTMXHhk	wbrQBZIo	Кирилл	Смойлов	0	1	859
24	2032129	t	\N	1GjRSfIi	Baq8DW25	Полина	Шестакова	0	1	901
25	2032014	t	\N	GWOXG7sd	kCAX6Ulw	Анна	Поскина	0	1	901
26	2032154	t	\N	tie8Jdrv	GKfDGsbR	Тилеген	Капен	0	1	819
27	2032083	t	\N	prJfqYl2	GvGPHWnB	Рахат	Муратбек	0	1	943
28	2032146	t	\N	ejwyKysx	FuHMLeeS	Екатерина	Заварухина	0	1	990
29	2032075	t	\N	mLJz4Aa9	VlA64YP8	Олег	Кудряшов	0	1	888
30	132224	t	\N	cwjXKmZD	p3k3QS8H	Егор	Березин	0	1	1015
31	2032156	t	\N	HjM2lNiP	60BP9H6r	Павел	Курильщиков	0	1	1019
32	2012030	t	\N	vVpWT2JO	t7iz8q2s	Никита	Нахратов	0	1	1019
33	2032111	t	\N	FA1bvd3P	Wd0262tP	Элиза	Исмагилова	0	1	990
34	2032112	t	\N	vMb2HUT6	ePZI2IdZ	Софья	Казакова	0	1	990
35	2032166	t	\N	rGvDouDZ	RMoEq32j	Екатерина	Петрова	0	1	989
36	2032161	t	\N	DtAH0LAY	vb3A2avb	Никита	Муринов	0	1	909
37	2032100	t	\N	7ODcyHcb	JY1WSl4m	Ильвина	Басимова	0	1	902
38	2032021	t	\N	cjPSy0l8	ZX0Zjh6L	Алишер	Юмакаев	0	1	861
39	2032138	t	\N	gLHHtW7h	wpXmIZor	Салават	Гимадиев	0	1	894
40	2032136	t	\N	XA4AvJzl	s09RNfNy	Алир	Галявиев	0	1	894
41	2032153	t	\N	76usEF24	yBt9oYVq	Ильвир	Ихсанов	0	1	894
42	2032002	t	\N	L7ZioKT9	AKHIyoyK	Андрей	Андреев	0	1	898
43	2032003	t	\N	wmLyEaaj	gm8KkzBy	Анна	Арсентьева	0	1	896
44	2032004	t	\N	gEhx9vyl	Zykdy80r	Валентина	Арсентьева	0	1	896
45	2032134	t	\N	Mi5Y6NFQ	hoUsUv8b	Виктория	Волковская	0	1	921
46	2032152	t	\N	UBAk8HGn	t6RaMMOn	Семён	Игонин	0	1	969
47	2032147	t	\N	hf7P4pPj	DQJtSVO6	Сергей	Загуменов	0	1	981
48	2032102	t	\N	YGQnrMBY	BFOhTS4d	Дарья	Бускина	0	1	919
49	2032120	t	\N	2osKfH4Z	8KixjPAy	Елизавета	Свинцова	0	1	885
50	2032185	t	\N	CHDlL7DT	UoQQiOCa	Виктор	Чулков	0	1	893
51	2032176	t	\N	w1nTIzny	RkEDZD8F	Даниэль	Трусов	0	1	893
52	2032099	t	\N	R7nOhGK9	F4WEBbIg	Мария	Ащеулова	0	1	903
53	2032006	t	\N	YLJg7pMv	dlQGxmHt	Айрат	Гараев	0	1	1018
54	2032157	t	\N	yPG45WIM	CrGg9KGv	Родион	Лабуткин	0	1	1017
55	2032158	t	\N	f9leobc5	VZs7poPA	Роман	Лабуткин	0	1	1017
56	2032038	t	\N	dJkUoi0N	7Mlnq9pG	Илья	Юхимец	0	1	981
57	2032071	t	\N	XbpFIwmK	FrAbFR1V	Кристина	Журавлева	0	1	896
58	2032162	t	\N	4xFwQiPA	HtRugANL	Никита	Мустаев	0	1	998
59	2032170	t	\N	NvuhP4mW	B5Y58Mpc	Динислам	Сафиуллин	0	1	993
60	2032168	t	\N	F6hh6bzF	pkfCH64b	Григорий	Рудниченко	0	1	955
61	2032135	t	\N	mKgbUKDd	kIaRVY8G	Данил	Газизуллин	0	1	985
62	2032165	t	\N	JJ3nPlQ8	DZV2uEiO	Ильдар	Нуршаяхов	0	1	1003
63	2032139	t	\N	mxYVksIO	BUIJSLgC	Никита	Григорьев	0	1	969
64	2032024	t	\N	uANcGZj2	K6N6Y7fj	Сергей	Ажимов	0	1	909
65	2032108	t	\N	AMKKiwsp	h7JQkiuF	Алина	Егорова	0	1	902
66	932101	t	\N	RPq8Bt6T	9HTTveFI	Артур	Файзуллин	0	1	861
67	2032150	t	\N	MpRJCI1c	qGbLnkBN	Илья	Захаров	0	1	993
68	41368	t	\N	wCQcWBAA	GqT1CVkV	Анатолий	Клочко	0	1	745
69	2032118	t	\N	riohdLf7	DMMG6cSK	Андрей	Перемечев	0	1	960
70	2032201	t	\N	dcvrf2el	Us9AEIkp	Тимофей	Путинцев	0	1	790
71	2032205	t	\N	nCckmchd	VO1rjI9J	Иван	Камчатов	0	1	955
72	2032192	t	\N	YmwxdAup	Fuo8O8HO	Гузель	Салимзянова	0	1	964
73	232028	t	\N	iIeZQVJ3	xa2EHVQ5	Салохиддин	Абдуллоев	0	1	815
74	232209	t	\N	7F6EJUi1	zvolNb4g	Ильмир	Шарапов	0	1	792
75	232007	t	\N	RgRlvsHm	k7wzns3S	Асгат	Гараев	0	1	787
76	232014	t	\N	8ksVNkGe	qAigUuTw	Самат	Нурмухаметов	0	1	1016
77	232019	t	\N	tDEPl5Og	C2M3v2lq	Максим	Зыкин	0	1	881
78	232017	t	\N	2CIKsJri	9KHePpPD	Максим	Степанов	0	1	860
79	232025	t	\N	InVFvV5y	uc9rCIzZ	Владислав	Адельшин	0	1	881
80	232035	t	\N	i1wbqk71	SXVWZk7L	Максим	Петров	0	1	879
81	232016	t	\N	p33IA9LL	8kfTBvty	Рашид	Закиров	0	1	953
82	232020	t	\N	qce4HIcP	QvpGY1bD	Марат	Салимов	0	1	878
83	232043	t	\N	0FZJv1LJ	WZc4bAsZ	Дамир	Байгубиков	0	1	787
84	232047	t	\N	i0pd7c6m	t0jieUM7	Роман	Тепляков	0	1	944
85	232083	t	\N	HCye7oW4	oC4A5STl	Данил	Трапезников	0	1	860
86	232040	t	\N	LH1s6eO7	tBbohupD	Дмитрий	Завалин	0	1	809
87	232051	t	\N	EbI0h3k8	53YcRr74	Егор	Вахрушев	0	1	953
88	232046	t	\N	CetS1Fsy	ULY9krvM	Александр	Алексеев	0	1	883
89	232011	t	\N	OH17U32p	ss8yFPiA	Иван	Рыбаков	0	1	982
90	232031	t	\N	c2qTt9Zd	fg0qgibY	Егор	Тесленко	0	1	1016
91	232044	t	\N	O2HqpNsb	SRlWSP2M	Кирилл	Рупасов	0	1	1016
92	232005	t	\N	UedGgumP	1D0JDM7S	Владислав	Тотчик	0	1	1000
93	232174	t	\N	cHta3SQK	eUEUr961	Дарья	Савельева	0	1	1006
94	232163	t	\N	Sfh72Z95	OLGxpAMq	Софья	Пигарева	0	1	948
95	232112	t	\N	bQtO7V7y	HNUZaXed	Надежда	Ламанова	0	1	914
96	232129	t	\N	9npEhTfN	OiwE1jiz	Виктория	Денисенко	0	1	1021
97	232130	t	\N	m8DIFgdy	bj7BgXMX	Ирина	Шилкина	0	1	1021
98	232109	t	\N	kfBmwZ8s	Ixx23LjM	Диляра	Иматдинова	0	1	989
99	232212	t	\N	Y8Q8pih3	vi4w5Lpj	Карина	Вахрушева	0	1	995
100	232125	t	\N	kHhUlZ4Q	QYtX51Cm	Риваз	Земдиханов	0	1	791
101	232203	t	\N	MRdvMQpl	4b59nUNQ	Андрей	Попов	0	1	878
102	232124	t	\N	eD70MB9T	T8eM4ZIu	Азалия	Гилязова	0	1	979
103	232190	t	\N	zjEU3EkA	pQAo2d0u	Константин	Константинов	0	1	862
104	232055	t	\N	3D8EOW4d	FFcIII4J	Наиль	Набиев	0	1	915
105	232202	t	\N	rT9NkECj	SKQY7fvV	Анастасия	Астафьева	0	1	1006
106	232217	t	\N	kLCUu0SM	v6wLPlvi	Елизавета	Таймнирова	0	1	947
107	232218	t	\N	48pDr6YJ	VFEHmR00	Ангелина	Тимина	0	1	947
108	232207	t	\N	mTMPOmeC	iyy3RDQ4	Илья	Константинов	0	1	792
109	232135	t	\N	ztobH7Zn	Y4NEDyDm	Алсу	Харисова	0	1	914
110	232206	t	\N	WcnHfx8T	I6bo5Fak	Тимур	Филимонов	0	1	792
111	232048	t	\N	SvObKK9c	wv0V6IiW	Айнур	Гаптуллин	0	1	945
112	232188	t	\N	opFzrsf8	ofMgmBYj	Айнур	Гарипов	0	1	862
113	232096	t	\N	tdmK1Jd5	1QG95aL1	Егор	Алешин	0	1	1024
114	232224	t	\N	a3IlluJL	RVwBfvzN	Кирилл	Данилов	0	1	857
115	232086	t	\N	SD3Rwh6f	nwJGbxRT	Никита	Тимофеев	0	1	1000
116	232205	t	\N	Fubc8q2K	1RlnnwyO	Тимур	Салахов	0	1	997
117	232097	t	\N	rqISXgzz	XMUJBASy	Радмир	Басыров	0	1	997
118	232095	t	\N	CFzQodob	snWbvF0G	Ильфар	Мингазутдинов	0	1	809
119	232063	t	\N	5XF65k3a	fc9mHO4h	Анна	Калинина	0	1	949
120	232183	t	\N	Jn0T6AuW	5tkK96fb	Иркэн	Самиков	0	1	864
121	232216	t	\N	7Ht0BewR	arpvsEDY	Ксения	Копейкина	0	1	966
122	232191	t	\N	bMswYOgW	XvOu7rsC	Кирилл	Мясников	0	1	943
123	232181	t	\N	y5XDX1xE	wvc0rCq4	Алексей	Пайбулатов	0	1	863
124	232062	t	\N	PnxcYkQo	BoacIqxB	Михаил	Нарсудинов	0	1	880
125	232201	t	\N	d9vYKHDr	MqVzQLmU	Александра	Минина	0	1	949
126	232087	t	\N	OANbCWcX	2SQBhVlJ	Алексей	Викторов	0	1	883
127	232076	t	\N	f84klEde	CDroIK7w	Рустам	Хамидуллин	0	1	970
128	232099	t	\N	jPsQYIMF	1XWyPtWu	Артур	Сафиуллин	0	1	1024
129	232082	t	\N	P5qvI5bE	eMGXPo6v	Даниил	Пискунов	0	1	1024
130	232092	t	\N	iwUtN4wU	svF2Zoua	Камиль	Шарафутдинов	0	1	916
131	232068	t	\N	UhwHvqGv	e7E0CmiJ	Яна	Дубовцева	0	1	951
132	232094	t	\N	eqistnHN	UOOiAySU	Камилла	Кайданова	0	1	951
133	232057	t	\N	1Aliyu7f	P3YOqxou	Саидахмад	Набиев	0	1	912
134	232023	t	\N	bGj0Iyyd	nw8vgNyT	Рауфджон	Примкулов	0	1	815
135	232136	t	\N	tfZNCCBr	tGLwWZ9f	Карина	Петрова	0	1	876
136	232131	t	\N	CdxSZBZ3	x2iar3Sf	Екатерина	Юреня	0	1	966
137	232056	t	\N	KlwfrWNv	FOAkTkmM	Даниил	Жуков	0	1	857
138	232184	t	\N	TnpEQK1X	7wbeifpy	Салават	Сафин	0	1	864
139	232160	t	\N	FJwjCTIV	WORTpHpA	Рената	Иванова	0	1	1006
140	232003	t	\N	vHbTPXM6	H1OZ8hVp	Марк	Стульгинский	0	1	945
141	251065	t	\N	fCxNjjWF	YwQwUMNU	Полина	Стамикова	0	1	966
142	232022	t	\N	tErgF8Bu	1fqpM9cv	Снежана	Антощенко	0	1	875
143	232142	t	\N	whtrOo1w	lWE5IYH3	Пётр	Минюшкин	0	1	944
144	232128	t	\N	oVmW2eya	C838lZ4D	Ксения	Ройтман	0	1	913
145	232006	t	\N	hr4iSEg0	KzDEfRm3	Тимур	Шилов	0	1	970
146	232071	t	\N	QBEKhIq1	foe2nf88	Ильнар	Гарафутдинов	0	1	860
147	232070	t	\N	6RQWVhqM	ri4cQg7h	Данил	Вебер	0	1	877
148	232065	t	\N	qF1pTAo9	zDq7Ctpd	Валерия	Кармакова	0	1	966
149	232018	t	\N	9BprxUch	CydRGO9o	Ернур	Ерсайынов	0	1	879
150	232120	t	\N	kf4KZ9z3	C6g0N5qT	Софья	Ткаченко	0	1	936
151	232013	t	\N	MaKdOuoO	BYKLrKIf	Анастасия	Шимарова	0	1	876
152	232219	t	\N	3PutREXt	OZrCs56U	Илья	Матвеев	0	1	880
153	232108	t	\N	FboJq5N1	LBO99eXg	Елизавета	Гизитдинова	0	1	875
154	232026	t	\N	wtWkjY4A	Rk7d451v	Дарья	Чередниченко	0	1	827
155	232081	t	\N	I5xRF6RC	NY1aJKSl	Михаил	Шатров	0	1	877
156	232080	t	\N	5sSXL2xO	bjXX7dUk	Ярослав	Шутов	0	1	982
157	232008	t	\N	IXj8MjgT	XGeXdGPL	Владислав	Бузынник	0	1	858
158	232111	t	\N	em1qrOvZ	GMfXKiJy	Никита	Менделуц	0	1	878
159	232090	t	\N	sJKpzsku	OiOYkxUm	Максим	Волков	0	1	982
160	232182	t	\N	lXJy3oMq	1gTHnGTQ	Денис	Козырев	0	1	1000
161	232170	t	\N	iHqu03y6	6K3bytIQ	Гиляна	Уразалиева	0	1	948
162	232213	t	\N	HIAYeTi9	cepPytXT	Тамерлан	Аблаев	0	1	858
163	232107	t	\N	OpQoGATG	qt1vbHD4	Елена	Степанищева	0	1	948
164	232165	t	\N	vNGnDkGX	IRrawckS	Саидкаримхон	Саиданваров	0	1	864
165	232103	t	\N	OPBllXGl	wT0Rk2Fl	Реналь	Юмангулов	0	1	858
166	232208	t	\N	E1qrmTd7	YKMmPZMy	Тимур	Забиров	0	1	791
167	232119	t	\N	ndYs04yw	Xj9fRpnW	Азизжон	Рауфов	0	1	917
168	231010	t	\N	YMHnwjGj	NG5RrrCi	Егор	Бурылов	0	1	1011
169	231008	t	\N	a0lnSPuh	W7msL9dN	Альмир	Ханнанов	0	1	868
170	231051	t	\N	F3hIdXkd	mVr37BgF	Артур	Аминов	0	1	745
171	231058	t	\N	wUuMbNHZ	FKzsznEO	Нияз	Сафин	0	1	867
172	231016	t	\N	0pnKgswA	YD8DDqpB	Гульназ	Халфина	0	1	885
173	231061	t	\N	cs1Bk4lP	raYjgKT4	Расим	Хамитов	0	1	867
174	231082	t	\N	h2g34JnV	BaGlSxq8	Максим	Елисеев	0	1	868
175	231079	t	\N	iiksyk7D	eIvQGb5z	Марсель	Гафиуллин	0	1	868
176	232078	t	\N	W2hl3LYI	dpWYCuB9	Байрам	Бахадуров	0	1	862
177	231097	t	\N	SWGyUR2K	TQ4CaZI8	Дана	Асанова	0	1	913
178	231001	t	\N	KC0FRPPs	4wHpWDQq	Валерия	Ватраскина	0	1	965
179	132151	t	\N	KBEVrrVx	3sMgEoSO	Милана	Халилова	0	1	793
180	231086	t	\N	3RCoIryM	C5wNSfKZ	Мохамед	Мулуд	0	1	897
181	232121	t	\N	VfnARvn4	z94Qgp6t	Ширинжемал	Алтыбаева	0	1	987
182	232172	t	\N	Y9qevnfO	Pm5G7obL	Шасолтан	Джумадурдыева	0	1	987
183	2032126	t	\N	eenjk3Nd	l0YBFaoB	Ринель	Халитов	0	1	789
184	132095	t	\N	3B2I5zJs	FupmUceO	Фаниль	Шамсуров	0	1	932
185	232147	t	\N	dtthpLjL	4xiU1O1F	Сейитмырат	Баллыев	0	1	841
186	132050	t	\N	Qj1g51MW	OXoNMnLj	Денис	Прохоров	0	1	925
187	132079	t	\N	xqxpGPLD	2k3XnqOk	Аделя	Мухамадеева	0	1	744
188	232154	t	\N	WJySm1CA	l42zxTTA	Лиана	Бикбулатова	0	1	930
189	132171	t	\N	maSN1yHh	M8hk4tVD	Анастасия	Самойлова	0	1	876
190	232157	t	\N	2NPv2Qmi	xYg0yUCa	Айгуль	Хисматуллина	0	1	930
191	132039	t	\N	83MUlAi0	oqq87bAo	Дмитрий	Туганов	0	1	926
192	232155	t	\N	AUTKSo32	XZPaHz8l	Илина	Баимова	0	1	936
193	232148	t	\N	LgWHvjgW	WpBFKQSG	Анастасия	Пьянова	0	1	936
194	132128	t	\N	3l4K0C8E	8MQyK9sF	Лилия	Абузярова	0	1	801
195	132092	t	\N	QnL1Kdty	sMqf6hyy	Екатерина	Борисова	0	1	801
196	232153	t	\N	XAmgcpb3	AqOqacZR	Алина	Солодянкина	0	1	929
197	232159	t	\N	mF8FymaH	vO1Sfwok	Амина	Темирова	0	1	930
198	232149	t	\N	rlYBa0an	3MC63Bui	Нурайым	Жыргалбекова	0	1	929
199	132044	t	\N	3Ulc0kEb	0LNdncA2	Алексей	Мухамедшин	0	1	927
200	132232	t	\N	ZMz3aLza	vWV4H1LX	Антонию	Капила	0	1	932
201	132186	t	\N	e33hPhq3	hn8HrfZE	Аяз	Шамсутдинов	0	1	932
202	132233	t	\N	7wX4zLEl	YyAQpxQE	Зинфира	Ишбердина	0	1	869
203	132090	t	\N	GbvJ9VSN	SlVRtcZL	Рушана	Идрисова	0	1	869
204	132045	t	\N	Cq5URbMY	S2apzdGn	Ян	Числов	0	1	926
205	132098	t	\N	qagUF4Q4	uKgajdd4	Максим	Хоров	0	1	931
206	132131	t	\N	Iz1WnpK2	lB2G3ufe	Константин	Чайников	0	1	928
207	132032	t	\N	OEXfVLnc	9P55qGcz	Всеволод	Зязев	0	1	928
208	132004	t	\N	QPcgBNQN	HMRMfP7e	Михаил	Разинов	0	1	928
209	132008	t	\N	qHdNCVhG	xoOZex8Y	Михаил	Свидетелев	0	1	926
210	132043	t	\N	hYibXVHD	k7Dp1nPm	Никита	Копеечкин	0	1	927
211	132116	t	\N	4evtRVZ2	7bR496Bu	Гульзана	Низамутдинова	0	1	799
212	132013	t	\N	1CqRS0TM	EIa0K6Iz	Махамбат	Алпысбай	0	1	819
213	231059	t	\N	DgsVn7Q3	MkVXnpP8	Данил	Смирнов	0	1	898
214	132027	t	\N	U2pzrLLx	zsJPkPCM	Мухаммадали	Нуров	0	1	808
215	132028	t	\N	YW42X1bF	xZzjgzbw	Егор	Федоров	0	1	808
216	132055	t	\N	uV9uvwQX	sivx1CXg	Ильнур	Карамасов	0	1	807
217	132065	t	\N	atKbRQWe	ltHSRxpP	Антон	Васильев	0	1	810
218	132213	t	\N	JPv81r3T	Pck0Ypfd	Динар	Гилязиев	0	1	810
219	132145	t	\N	czkICYMp	71x3ea6K	Кирилл	Сергеев	0	1	814
220	132069	t	\N	r2Yb3DDm	C1XUKmBo	Андрей	Тюрин	0	1	818
221	132147	t	\N	6YG7vxOl	moHXc2Fs	Владислав	Швыдко	0	1	818
222	132156	t	\N	6fuNg1Uj	sEd4CWld	Александр	Ищейкин	0	1	814
223	132078	t	\N	HJxCX89H	61ozk7ej	Никита	Николаев	0	1	818
224	132132	t	\N	NFs6q8aD	g3URWpC5	Денис	Матвиенко	0	1	817
225	132178	t	\N	NXzesaNf	bXfHMPro	Ярослав	Каров	0	6	820
226	132189	t	\N	s1vYHPZV	DCXTKIzj	Нияз	Хайруллов	0	1	820
227	132161	t	\N	n7fDxAif	NDHauSgs	Иван	Микрюков	0	1	817
228	132107	t	\N	PgY6TnFD	UcNxzFs8	Руслан	Хазбуранов	0	1	813
229	132109	t	\N	qwMc8kkl	xtWNRK9C	Никита	Розинов	0	1	813
230	132059	t	\N	fllCJEIY	LG08s7tR	Матвей	Живаев	0	1	807
231	132124	t	\N	2S4Kyo3x	tEqYc5w3	Анастасия	Слюсарева	0	1	811
232	132106	t	\N	gmZnvFoL	lwDzC0Na	Олеся	Поплавская	0	1	811
233	232678	t	\N	FgSgzJcX	P7L4rJOn	Никита	Севрюков	0	1	863
234	132058	t	\N	ywUeW5IL	XAucWYKi	Азат	Мухаметзянов	0	1	985
235	241120	t	\N	NNfIfi48	2bYf2xL3	Лиана	Фаткуллина	0	1	965
236	132007	t	\N	MsPlDKdx	U8jyIXZX	Алия	Каламова	0	1	793
237	2032172	t	\N	NJcmMjhG	32Erj8W8	Валерий	Сиразиев	0	1	887
238	132021	t	\N	lDdT72Pw	9gxExFHo	Лилия	Гилязева	0	1	886
239	2032174	t	\N	aJaM7adn	2eJuKibx	Эвелина	Стрельникова	0	1	886
240	2032155	t	\N	hERIoZxV	vIWo3Jht	Виталий	Кирушин	0	1	887
241	132070	t	\N	8L6fTU0N	bGv2q0XI	Ландыш	Шайхутдинова	0	1	794
242	132211	t	\N	KW0Rh0Yu	0imEoN0P	Гульфия	Давлетова	0	1	794
243	132205	t	\N	iT2KopNa	MJF3iaQw	Малика	Мынжасарова	0	1	794
244	932006	t	\N	Amr9Mukm	2u7i3yX6	Сино	Иброхимов	0	1	880
245	232151	t	\N	vemXGhyY	DSmpPldV	Гозел	Нурмухаммедова	0	1	935
246	132089	t	\N	ZoINcfWY	PckCSzE1	Регина	Гафарова	0	1	800
247	132196	t	\N	FE7a6Szj	Jief5Z2e	Юлия	Александрова	0	1	744
248	132163	t	\N	taPqRliI	jz6WWCrG	Альфия	Хабибулина	0	1	800
249	132144	t	\N	Iryug626	ngPPQFRK	Анна	Куприянова	0	1	744
250	132143	t	\N	92tRAO65	6YqdHmRU	Камилла	Естерекова	0	1	743
251	132142	t	\N	Hv9NlNZh	8i3XUrgN	Карина	Естерекова	0	1	743
252	132174	t	\N	vvONsCCA	i4QRchik	Акерке	Абдулова	0	1	800
253	2032207	t	\N	zGKPmtdE	XTRFSwWK	Денис	Латыпов	0	1	789
254	232237	t	\N	RBTYvlvV	HxWpiFxK	Сердар	Розыбаев	0	1	944
255	332095	t	\N	LBt5db3f	S5bp8wSa	Адель	Шайдуллин	0	1	823
256	332250	t	\N	ESsJWzxg	s8DI1Zps	Эмилия	Резенова	0	1	904
257	332026	t	\N	Al5qwcOi	uDxTSkvu	Даниил	Яндубаев	0	1	781
258	332051	t	\N	Sj08GTYo	UVXrnThM	Татьяна	Андреева	0	1	828
259	332030	t	\N	o7z9SmxC	1UeObLxH	Амирхан	Батталов	0	1	761
260	332019	t	\N	Z6UJ6h9E	lBkya4rt	Илья	Рыков	0	1	847
261	332257	t	\N	yaNPAvpc	NTacOCt8	Райля	Салимянова	0	1	922
262	332023	t	\N	Y0AqBfpr	FYe7DnkL	Илья	Акимов	0	1	925
263	332018	t	\N	39DudJX3	hAArGgUr	Александр	Никитин	0	1	842
264	332041	t	\N	Km6J3t8J	l685oLt5	Данил	Новоселов	0	1	752
265	332032	t	\N	NkskdHUe	6hhEQZbt	Артемий	Юрлов	0	1	954
266	332048	t	\N	MNvJEqa1	LZ2HUGLC	Никита	Константинов	0	1	842
267	332008	t	\N	VgWL6XTt	cAlOyk4K	Руслан	Ермолаев	0	1	829
268	332036	t	\N	G8wq3pAP	wXGvWoUp	Павел	Кричевский	0	1	757
269	332016	t	\N	S71w5UU7	UCTUifOq	Александр	Иванов	0	1	757
270	332034	t	\N	NPpcRXEN	rjliCrIB	Ильназ	Шаяхметов	0	1	915
271	332046	t	\N	Fs7rVzQY	12pLy8Bg	Владислав	Борисов	0	1	846
272	332010	t	\N	940TKLjA	QdcqAIUa	Анастасия	Гарина	0	1	922
273	332025	t	\N	wbPaWJ8D	I2H8eoYR	Матвей	Детин	0	1	795
274	332035	t	\N	RkYVYSmZ	Rd2NP7Rr	Владимир	Шишкин	0	1	775
275	332259	t	\N	hQyi712z	wLuD6WPB	Семён	Шамшурин	0	1	796
276	332078	t	\N	5zCeRd22	Mr6pl32w	Матвей	Лукиных	0	1	852
277	332052	t	\N	1s7rUGsf	PVKfrx13	Рустем	Хасанов	0	1	843
278	332090	t	\N	DAXuQxcC	tI5FqyaS	Екатерина	Спирина	0	1	802
279	332071	t	\N	5Vo6zRix	imaeqbAy	Артур	Иркабаев	0	1	746
280	332053	t	\N	im346t4G	AaFRWKrM	Артем	Патраков	0	1	795
281	332072	t	\N	3eOp3oCz	9yOCam8I	Сает	Хаммадиев	0	1	755
282	332045	t	\N	1P6uqY0L	cRJEW0Dr	Андрей	Дряхлых	0	1	826
283	332070	t	\N	tFnK5QTb	IXdmP0xv	Нурсиль	Набиуллин	0	1	844
284	332254	t	\N	yaV4OOM5	TJTklu8W	Родион	Казаков	0	1	796
285	332092	t	\N	4aFjGuCo	rCKRiMtm	Дмитрий	Брусов	0	1	882
286	332037	t	\N	N6c05CLZ	ZEXtTz9u	Дмитрий	Петров	0	1	882
287	332020	t	\N	qst7ydTy	eqNf8C5O	Матвей	Владимиров	0	1	978
288	332028	t	\N	wQQxsNme	mP4IX4RG	Тагир	Ахметов	0	1	758
289	332226	t	\N	bw2eR6TS	UnHBsdvm	Рушана	Султанова	0	1	828
290	332232	t	\N	Kea5rI3G	02pQEqvD	Денис	Долгов	0	1	765
291	332120	t	\N	sS2FtIyl	WeRctdHK	Ксения	Петрова	0	1	802
292	332183	t	\N	qiw0D1Dd	UgiinVP7	Софья	Ипполитова	0	1	812
293	332221	t	\N	84NaFhsw	9xEWceOj	Эмиль	Маликов	0	1	910
294	332246	t	\N	Sh36pflI	APai1Phy	Ксения	Алпеева	0	1	812
295	332234	t	\N	orR6uuWv	aWpbKIs7	Камила	Шайгараева	0	1	828
296	332220	t	\N	7uW1GkNL	M3fhCQWs	Тимур	Галиуллин	0	1	767
297	332240	t	\N	tk2LdG83	jMyHKNNI	Алена	Рысина	0	1	870
298	332235	t	\N	ygCMIVcm	yb4fWqVT	Муса	Муртазин	0	1	755
299	332228	t	\N	gw7ktiIw	bpuFMFls	Максим	Петров	0	1	752
300	332123	t	\N	0So4fHeR	YcAsWkh4	Ильяр	Уракаев	0	1	937
301	332111	t	\N	GnjJmM9c	mEPG05dT	Татьяна	Рябова	0	1	750
302	332129	t	\N	Olnxgzsx	yXGSfCGU	Зарина	Яваева	0	1	750
303	332154	t	\N	Aa7JmqAq	7gfjzk5i	Матвей	Фирсанов	0	1	779
304	332128	t	\N	PH8CXCOn	BTXXnYJX	Тимур	Маснабиев	0	1	779
305	332155	t	\N	OwXVmxTU	YuxMORlz	Максим	Цапаев	0	1	829
306	332124	t	\N	98RkSVi0	bn2t21rd	Карим	Хазиев	0	1	892
307	332149	t	\N	TNIxGdtd	bLerUX0q	Лиана	Фасахова	0	1	904
308	332229	t	\N	9deC9uA7	xXAK2g2m	Тимур	Токарев	0	1	767
309	332125	t	\N	9XMiZplA	tisoBLKJ	Рафаэль	Галямутдинов	0	1	842
310	332132	t	\N	BbimOYcY	VpYKO246	Богдан	Байкалов	0	1	742
311	332236	t	\N	hj9iTPCF	yg7TfTqS	Роман	Маклыгин	0	1	845
312	332231	t	\N	yk91Sb2S	CCe3zYP1	Камиль	Валишин	0	1	768
313	332134	t	\N	kvBzrK9Q	6rTJjquZ	Фёдор	Кирдяшов	0	1	852
314	332122	t	\N	FPJq1ejW	KBXchpme	Анжелика	Гилязова	0	1	979
315	332131	t	\N	XBjcfIay	6AVGVnb5	Алик	Ибрагимов	0	1	742
316	332029	t	\N	V3zF8EiV	l8s808wG	Андрей	Баркунов	0	1	796
317	332211	t	\N	kDDjryYX	Kqzkeif7	Алмаз	Нигматзянов	0	1	755
318	332238	t	\N	LKmIfH3O	dVIbKkN8	Камиль	Красильников	0	1	851
319	2311025	t	\N	2T1XVOQ9	VJlItsH3	Дмитрий	Холоденин	0	1	1012
320	2311022	t	\N	Z7EPnEGC	LihYDWjO	Артём	Тарасов	0	1	782
321	332001	t	\N	Y8zq26ve	IBQL11vU	Данила	Рогожкин	0	1	847
322	332121	t	\N	X5SmIRYp	1zF8IygH	Константин	Майоров	0	1	854
323	2311015	t	\N	5fYoD7bd	NmE2pl7W	Тимофей	Моисеев	0	1	781
324	332047	t	\N	B6T0G54V	V7foiqlO	Данил	Гаврилов	0	1	823
325	332055	t	\N	gEoC0Avy	JfUjYchU	Кирилл	Бушмелев	0	1	758
326	332096	t	\N	cdob2PvI	JbCs1Jlu	Илья	Савинов	0	1	851
327	332089	t	\N	SMKIOTLa	aM4PblEg	Данис	Кулбаев	0	1	854
328	332219	t	\N	PlSxeJE8	MujUXaQ7	Дмитрий	Борисов	0	1	954
329	332256	t	\N	sHQjG3JH	XEszVsHr	Андрей	Антонов	0	1	824
330	332113	t	\N	o7FJGrPr	TbOV0dE6	Азалия	Мурзина	0	1	759
331	332024	t	\N	6jdZ53cH	2LJ1DjUn	Марат	Аскаров	0	1	824
332	332304	t	\N	AtrpZ7U3	bDXlNUPk	Камила	Гайратова	0	1	750
333	332085	t	\N	6JP4L6Ke	UE5pEDk5	Никита	Афанасьев	0	1	758
334	332057	t	\N	qcVGbU7u	zJQPYbhR	Даниил	Зубков	0	1	845
335	332093	t	\N	lgDmfHdo	sewvNQ6M	Кирилл	Кудрявцев	0	1	852
336	332088	t	\N	XxwEBMkO	Ce6ZLtW2	Михаил	Иванов	0	1	746
337	332084	t	\N	oJBLBAE1	4koTCSnV	Иван	Наумов	0	1	1011
338	332177	t	\N	U0314pmk	wpq2Iv0l	Дидар	Максадов	0	1	761
339	332064	t	\N	Q1xfRgSQ	WEoXNgAN	Икром	Исломов	0	1	826
340	332116	t	\N	aJVuOYN3	EiIlv89r	Анастасия	Горюшина	0	1	895
341	331103	t	\N	0kGpBL17	TvboTrEi	Данияр	Чугурнов	0	1	972
342	332245	t	\N	2q6wjqt9	PjoiEPgg	Мекан	Веллеков	0	1	910
343	332261	t	\N	3HnH5DJa	D6GKWMMF	Мырат	Агаев	0	1	1012
344	331110	t	\N	kggBjwPg	PdHjfVuL	Кристина	Новохатская	0	1	827
345	332087	t	\N	WvmLBpw1	LVnhKU9B	Амир	Сайранов	0	1	854
346	331087	t	\N	PuXuQGke	FBgDsme7	Диана	Багаутдинова	0	1	802
347	331086	t	\N	XETe9SP6	VF929Ice	Мария	Наборщикова	0	1	921
348	331100	t	\N	jKe8K20b	0Xiohm0i	Дарья	Власова	0	1	836
349	331038	t	\N	0SLhU6eZ	TnAnuCNl	Никита	Пыхтеев	0	1	1018
350	331040	t	\N	suHccaIm	7oE5pyMk	Артур	Сигватуллин	0	1	972
351	331032	t	\N	Z2X9lNdo	nhMciUyl	Ринат	Гуфраев	0	1	785
352	331052	t	\N	U0DyNYr4	nguhBkDr	Альберт	Музаффаров	0	1	916
353	331064	t	\N	4VTD3Qqk	I3tyXSfF	Максим	Прокопьев	0	1	765
354	331085	t	\N	hUwsCI5o	CsUnpdLE	Илюза	Гафарова	0	1	1022
355	331072	t	\N	wP5szR3S	HUqUzD2W	Эльза	Гарипова	0	1	1022
356	331050	t	\N	R8e6WAGs	okcGiy41	Динар	Ахмадуллин	0	1	859
357	331055	t	\N	wPoBT1v1	WtPjDsZL	Амир	Мулюков	0	1	962
358	331101	t	\N	XKaKdpTV	alfXbI4S	Алсу	Закирова	0	1	835
359	331115	t	\N	XikIgkH6	ZHiclnuC	Иван	Волков	0	1	853
360	331011	t	\N	YPqr0vwU	lj7az5HM	Александр	Боревич	0	1	808
361	331082	t	\N	6lmpHvzP	IVxx1yyk	Артур	Гатауллин	0	1	853
362	331059	t	\N	AiZVCsku	UWr2iDJk	Артур	Хамидуллин	0	1	961
363	331054	t	\N	gdtqgjoq	ThGZt5lP	Бехруз	Махкамов	0	1	782
364	331001	t	\N	dotFQrTb	ZC7GxvFB	Дарья	Госькова	0	1	835
365	331012	t	\N	j9yVX89g	4fgttQId	Денис	Дьяконов	0	1	786
366	331125	t	\N	586ZaWBH	C9czCAez	Никита	Шакиров	0	1	785
367	331124	t	\N	8Dzr3a9G	hCt5rANP	Салават	Набиуллин	0	1	962
368	331035	t	\N	alaMeuIh	QbT1WGu2	Тагир	Махмутов	0	1	898
369	331070	t	\N	kKuypNxD	tL0ghinx	Иван	Алабужев	0	1	960
370	2032179	t	\N	Xy3nfxnM	AjkufL1D	Шахзод	Турдиев	0	1	790
371	331102	t	\N	m7Tx7t8n	CrhvZbP7	Альбина	Хамзина	0	1	836
372	332073	t	\N	VuwkqHBP	1gzSLUo4	Мухамад	Каримов	0	1	892
373	232764	t	\N	1MSmpooa	ClYDLvGi	Филипп	Балобанов	0	1	844
374	331028	t	\N	baYfC8CK	Kf7msCXx	Дилнар	Розыева	0	1	1022
375	332145	t	\N	yk8g25RB	EON6L2Ap	Керим	Чекаев	0	1	882
376	332136	t	\N	v1brM7cE	VWK8FZmh	Гулджахан	Буграева	0	1	777
377	332143	t	\N	MDGOzdhw	UazxZNW1	Мария	Канунникова	0	1	760
378	331036	t	\N	tTrosrE1	amXzwK4X	Александр	Несмеянкин	0	1	962
379	331033	t	\N	gnO021uN	GKeyGWJI	Илья	Иванов	0	1	1015
380	332002	t	\N	DWXhAGTS	ggQmsvAp	Фардин	Давлатзай	0	1	1004
381	331014	t	\N	in1EfkwO	7dpVQO7f	Артем	Мордвинцев	0	1	786
382	331006	t	\N	XkwnzFg9	dUGW7OqK	АйзатИльсурович	Харисов	0	1	786
383	132036	t	\N	oPhaLH8d	IwYwo3Zb	Александр	Шишкин	0	1	775
384	2032114	t	\N	KJkFAkng	GBIOsKvQ	Дмитрий	Лебедев	0	1	994
385	2032183	t	\N	C5D3PwM9	VOdHYT6Y	Шамшод	Хасанов	0	1	933
386	332130	t	\N	iEIdjsMv	dhw4kyPw	Рехнет	Дурдылыев	0	1	783
387	232117	t	\N	rlLYBPNP	IFvBU4QT	Марсель	Рамазанов	0	1	937
388	332060	t	\N	LDqQEl4A	2O96hCh7	Ровшен	Дурдыбаев	0	1	776
389	332127	t	\N	1tjBsTQV	nACG1vjK	Сона	Азадова	0	1	870
390	232113	t	\N	zUmWUKSB	SY5Nxzjj	Герман	Смирнов	0	1	893
391	232238	t	\N	OW6uaFFI	tKpESkKv	Ахмед	Ахмед	0	1	897
392	332159	t	\N	OczWSU8C	gnpum1Zr	Багул	Батырова	0	1	920
393	332278	t	\N	44DDI6vm	06D7BDxn	Гул	Акыева	0	1	920
394	332138	t	\N	hjCXCJaH	mIGVixxs	Ширин	Гурдова	0	1	904
395	332286	t	\N	vOgbubWt	boGzCoTn	Эзизхан	Мовлямов	0	1	844
396	332301	t	\N	AFhXOzF5	NyFmKQn5	Новруз	Сапармырадов	0	1	780
397	332267	t	\N	tlBbSuxD	KHG9iWSN	Агамырат	Магтымов	0	1	834
398	332266	t	\N	2X1GTCjo	KSJ3YRp8	Арслан	Ишанов	0	1	834
399	332161	t	\N	6tY69MzN	ShPZAqBn	Батыр	Сапаргелдиев	0	1	762
400	332372	t	\N	njDnlK83	6NSKylf4	Бахтовар	Абдусатторй	0	1	846
401	332324	t	\N	k01eTs2R	FRES5kLE	Мухаммадшариф	Мирбобоев	0	1	846
402	332269	t	\N	cINLdkpn	E4I3J7yU	Реджепмырат	Язмырадов	0	1	834
403	232763	t	\N	QVn00HIM	6VBFXcdt	Фахруддин	Исматов	0	1	916
404	332188	t	\N	XvJlJo5N	OyxVaHbr	Кервен	Гараджаев	0	1	797
405	332313	t	\N	JErrdgsn	YIA42ntg	Керим	Аннагелдиев	0	1	762
406	332339	t	\N	eNiTkwIv	cZO5zmnV	Амангелди	Гараджаев	0	1	797
407	231140	t	\N	pSa7N9Ix	19cU8eib	Дияр	Бабамурадов	0	1	762
408	2032144	t	\N	I5bnxuy9	8emPo718	Улугбек	Жунайдуллоев	0	1	814
409	332162	t	\N	Iia6RIfZ	e8HZ9zea	Ыхласмырат	Абдуллаев	0	1	826
410	332187	t	\N	oygJEl0x	GuON37Ot	Даянчмырат	Довлетов	0	1	776
411	332164	t	\N	hE5qzSlx	9TSreTGs	Мерген	Мухамметбердиев	0	1	892
412	832175	t	\N	qIDWcmoc	VzQakObN	Махмуд	Хаммам	0	1	1001
413	832174	t	\N	WK8Slzz8	izw8jn32	Мохамед	Хаммад	0	1	1001
414	332289	t	\N	GmOT9hOS	7viPvRQV	Сапарбиби	Оразова	0	1	980
415	332284	t	\N	tO5YyCwN	wZvjC7Rf	Вепа	Бердиев	0	1	830
416	332195	t	\N	Ja0WtF9d	eX9P5dpL	Руслан	Кабишов	0	1	780
417	332377	t	\N	FW3F4R8Q	rTDnBm6F	Шахноза	Адызджанова	0	1	988
418	332336	t	\N	fIJ7J2F5	SW25nPJq	Маликгулы	Байраммырадов	0	1	742
419	332327	t	\N	zQYGkEp4	GAneRLOk	Сабурджан	Сабуров	0	1	790
420	332375	t	\N	DklQxWMf	YkUk5mBX	Захитджан	Бердыев	0	1	1013
421	236840	t	\N	kdTQQEiY	KVK0oEeT	Сохбет	Овезов	0	1	946
422	332350	t	\N	RSmCKQiz	koEFAbSW	Серви	Мусдапаева	0	1	920
423	236812	t	\N	xB4mLKrC	eenXKSof	Арвуз	Аннаева	0	1	988
424	332194	t	\N	q5Ts6cHP	fgAOkNBa	Айшат	Атамедова	0	1	988
425	236579	t	\N	YYQczvOl	QzkjHAIF	Арслан	Нурмаммедов	0	1	776
426	332163	t	\N	YleForli	j0ZeW1pm	Айнур	Какагелдиева	0	1	759
427	236784	t	\N	Hl0TxA8g	c0SGKKz6	Галкан	Якубов	0	1	998
428	236915	t	\N	sHaevS2G	mSIqiuib	Мейлис	Мухаммедов	0	1	984
429	236437	t	\N	JyHV0Czt	TytKQl8s	Айнабат	Овезова	0	1	935
430	236396	t	\N	8XQdnKHB	dAjZrs66	Рашит	Аширкулиев	0	1	998
431	236744	t	\N	DNJRqhrK	270JHqSx	Эркин	Аллабердиев	0	1	984
432	236447	t	\N	w5XnnPB1	p1By4T9k	Хакберди	Джанназаров	0	1	984
433	231141	t	\N	Jxi45p3A	vDRrHx78	Язмырат	Гелдиев	0	1	1004
434	232233	t	\N	rzlDx58V	UL5S1DxH	Кахрамон	Аширов	0	1	933
435	236472	t	\N	47RLlKWI	jEgIBolp	Нагым	Багыев	0	1	946
436	332262	t	\N	zE9ocSZD	Q5Pp5jAl	Байрамдурды	Мелаев	0	1	994
437	332312	t	\N	66znMsiM	fEEGSgiV	Гурбан	Пащыев	0	1	763
438	332310	t	\N	R2ZdnWnT	Z58FYRGj	Тахыр	Гылычдурдыев	0	1	783
439	236803	t	\N	3iHgsrAm	Ush1koJr	Багтыяр	Таллыев	0	1	994
440	332353	t	\N	5gUWSZnH	2G46pdaX	Гапур	Оразгелдиев	0	1	763
441	236844	t	\N	4hmTtBCl	mLXUtrzx	Максат	Сапармаммедов	0	1	766
442	332191	t	\N	N4DZaV6d	0hjX94R2	Мекан	Чарыев	0	1	766
443	236678	t	\N	kSYi7tps	t3XtfZwp	Огулнияз	Ходжамбердиева	0	1	996
444	332326	t	\N	ytBPgqxZ	PrzPDZn5	Селби	Гарлыева	0	1	914
445	332300	t	\N	Wjv8pdeX	drTuXewY	Огулджан	Алланепесова	0	1	950
446	236599	t	\N	ZR9wBnd9	mlrfBOF9	Арслан	Назаров	0	1	824
447	332346	t	\N	JuUtaUib	zSGl3cpD	Назар	Курбанов	0	1	848
448	332334	t	\N	M8h33g64	2WqdgAsO	Анварбек	Бабагулыев	0	1	848
449	332338	t	\N	pJCzAs93	OJuNC69l	Тахырджан	Гапурджанов	0	1	848
450	332268	t	\N	dsb24h0t	43IGvG0i	Рахым	Нурмухаммедов	0	1	960
451	236272	t	\N	hqL37MGJ	qALmIyvL	Мамед	Исламов	0	1	833
452	236452	t	\N	50BBDmN2	bb8469RQ	Аманмырат	Мередов	0	1	841
453	332294	t	\N	izETkkjV	IOZz1Ujc	Айна	Ашыраманова	0	1	996
454	332282	t	\N	8gcLn8mA	DSUkhJ1V	Бегенчмырат	Агаев	0	1	931
455	332302	t	\N	Wl1r4IQA	SLeRhf8d	Багдат	Халаев	0	1	810
456	332285	t	\N	0UfwtwE4	OFMMtP0v	Айджан	Гелдыева	0	1	963
457	332292	t	\N	zqBfP1xQ	y1RdSTup	Гулджан	Гелдыева	0	1	963
458	332318	t	\N	pClQgy5Y	6RpUoTLj	Бегенч	Меджиков	0	1	938
459	332160	t	\N	uZEIvS8n	UFE6nJq6	Сердар	Сапаргелдиев	0	1	752
460	236499	t	\N	ZhVog132	VWRMLoO9	Мухамметгелди	Шаларов	0	1	833
461	332273	t	\N	2cThKBSV	yVDxthZr	Атаджан	Маммедов	0	1	1014
462	332299	t	\N	vzvkU0VY	VoK24GAE	Огулдженнет	Оразсахедова	0	1	799
463	332349	t	\N	KDvI1Dv7	20o3Covj	Гапбар	Метиев	0	1	1014
464	332359	t	\N	FOioXDYU	PDbRuJvK	Мекан	Хайдаров	0	1	946
465	332351	t	\N	CAXCtU2M	1aHFSth3	Мердан	Нурсахатов	0	1	1014
466	236573	t	\N	QfBSZQ25	GSY1zdkX	Огулджан	Кулбаева	0	1	886
467	332189	t	\N	ZCmczaj5	StY9RKvJ	Дженнет	Бабаназарова	0	1	778
468	236448	t	\N	GjZssBXN	WEHV1sfl	Арслан	Джумагулыев	0	1	1013
469	236809	t	\N	N8NPFHRU	jgVXIS8q	Дженнет	Хемраева	0	1	778
470	236814	t	\N	7seIGZtE	pvpNN07X	Нодира	Мирзакулова	0	1	778
471	332361	t	\N	4ZBNkBhD	9WHl3Ibs	Ходжагулы	Ходжагулыев	0	1	972
472	332277	t	\N	3GeQBbod	1ECTwtqS	Исгендер	Байрамгелдиев	0	1	967
473	332283	t	\N	bLmwK3fL	WAzMX52t	Энегул	Байрамгелдиева	0	1	967
474	236964	t	\N	tB5K7QAQ	1oPt3g6e	Гундогды	Гурбанов	0	1	849
475	236374	t	\N	6dRCLKow	TDcWO0XK	Аллаберди	Башимов	0	1	788
476	236557	t	\N	cZnrabP0	7OTmrb5T	Ковус	Байрамов	0	1	788
477	332332	t	\N	7BiYepN2	aVfOgTww	Амир	Анваров	0	1	788
478	236539	t	\N	KlSBUzwa	JfRdXs0l	Якуп	Палванов	0	1	849
479	332190	t	\N	hzK07oul	8P9iByxi	Джемал	Торекулыева	0	1	777
480	332307	t	\N	iJoLwaBq	uDY5psOm	Алтын	Довлетова	0	1	950
481	332343	t	\N	gJQhMkBR	ZMv8OvKn	Боссан	Джумаева	0	1	950
482	332200	t	\N	tSPkKPbK	xuw3yQNb	Сулгун	Джейхунова	0	1	760
483	323199	t	\N	21PycRtj	SwNOzroh	Махмут	Шемсиддинов	0	1	956
484	332365	t	\N	LseorG1W	RjyE6ns9	Непес	Язмырадов	0	1	741
485	332264	t	\N	enpPs3LP	mahaSpOR	Одилджон	Одинаев	0	1	938
486	332062	t	\N	0VxutQl0	estjXmL1	Фазлиддин	Салимов	0	1	766
487	332027	t	\N	zt7O4fUn	uP0oGvYw	Озодбек	Норматов	0	1	768
488	332014	t	\N	E6I7mIOZ	nzv2QY04	Мейрамбек	Актамаков	0	1	843
489	332171	t	\N	KAkymjK8	TG9VaoBh	Ангелина	Ярославцева	0	1	749
490	332172	t	\N	Gkvs73YW	4IYikFJG	Александра	Гаврилова	0	1	749
491	332244	t	\N	KGmkKXxw	Yk8pzKkh	Мирас	Куанбай	0	1	768
492	332173	t	\N	7zsZkr5h	5k9kYocb	Ксения	Старикова	0	1	812
493	332176	t	\N	iaXFeS45	1s18n1gG	Мария	Анастасьева	0	1	980
494	332225	t	\N	y9kEtkNT	L8yX57vA	Дарья	Латушкина	0	1	870
495	332017	t	\N	FwJTWVtK	YgKl2qke	Худоёр	Пулотов	0	1	938
496	232998	t	\N	7mPNVjhf	rRXErNFk	Михаил	Евсягин	0	1	782
497	2311016	t	\N	G596St5G	2ZsodW5e	Шукрулло	Нуралиев	0	1	830
498	332076	t	\N	w7VuZedf	DZ0ZyGQz	Альмир	Хамидулин	0	1	746
499	332178	t	\N	v3Mvwqo2	oCovToii	Виолетта	Басюк	0	1	980
500	331120	t	\N	tHf9vePj	lHBrIU64	Дмитрий	Шилин	0	1	961
501	2311020	t	\N	CDFBjUQm	Upo1yglx	Виктор	Рыжиков	0	1	830
502	2311004	t	\N	PH6jmvVY	7nrVP1h1	Алия	Вахитова	0	1	895
503	2311194	t	\N	naYGQRvh	SR5z5n9O	Нияз	Аввясов	0	1	825
504	2311195	t	\N	ysar2oP3	Z44hI2YL	Айдар	Арсланов	0	1	825
505	2311005	t	\N	U0rW2ihl	4bYfVcaB	Азат	Гайнетдинов	0	1	911
\.


--
-- Data for Name: worktickettable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.worktickettable (id, creator, deadline, kpd_rollback, ticket_hash, text_task, performer_id) FROM stdin;
\.


--
-- Name: eventlogtable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.eventlogtable_id_seq', 1, false);


--
-- Name: eventtypetable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.eventtypetable_id_seq', 5, true);


--
-- Name: feedbacktable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.feedbacktable_id_seq', 1, false);


--
-- Name: imagetable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.imagetable_id_seq', 1, false);


--
-- Name: notificationtable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notificationtable_id_seq', 1, false);


--
-- Name: roletable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roletable_id_seq', 6, true);


--
-- Name: roomtable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roomtable_id_seq', 1026, true);


--
-- Name: sankomtable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sankomtable_id_seq', 1, false);


--
-- Name: usertable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usertable_id_seq', 505, true);


--
-- Name: worktickettable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.worktickettable_id_seq', 1, false);


--
-- Name: eventlogtable eventlogtable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventlogtable
    ADD CONSTRAINT eventlogtable_pkey PRIMARY KEY (id);


--
-- Name: eventtypetable eventtypetable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventtypetable
    ADD CONSTRAINT eventtypetable_pkey PRIMARY KEY (id);


--
-- Name: feedbacktable feedbacktable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedbacktable
    ADD CONSTRAINT feedbacktable_pkey PRIMARY KEY (id);


--
-- Name: imagetable imagetable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagetable
    ADD CONSTRAINT imagetable_pkey PRIMARY KEY (id);


--
-- Name: notificationtable notificationtable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificationtable
    ADD CONSTRAINT notificationtable_pkey PRIMARY KEY (id);


--
-- Name: roletable roletable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roletable
    ADD CONSTRAINT roletable_pkey PRIMARY KEY (id);


--
-- Name: roomtable roomtable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomtable
    ADD CONSTRAINT roomtable_pkey PRIMARY KEY (id);


--
-- Name: sankomtable sankomtable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sankomtable
    ADD CONSTRAINT sankomtable_pkey PRIMARY KEY (id);


--
-- Name: usertable usertable_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable
    ADD CONSTRAINT usertable_login_key UNIQUE (login);


--
-- Name: usertable usertable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable
    ADD CONSTRAINT usertable_pkey PRIMARY KEY (id);


--
-- Name: usertable usertable_student_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable
    ADD CONSTRAINT usertable_student_id_key UNIQUE (student_id);


--
-- Name: usertable usertable_tg_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable
    ADD CONSTRAINT usertable_tg_id_key UNIQUE (tg_id);


--
-- Name: worktickettable worktickettable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worktickettable
    ADD CONSTRAINT worktickettable_pkey PRIMARY KEY (id);


--
-- Name: eventlogtable eventlogtable_event_initiator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventlogtable
    ADD CONSTRAINT eventlogtable_event_initiator_id_fkey FOREIGN KEY (event_initiator_id) REFERENCES public.usertable(id);


--
-- Name: eventlogtable eventlogtable_event_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventlogtable
    ADD CONSTRAINT eventlogtable_event_type_id_fkey FOREIGN KEY (event_type_id) REFERENCES public.eventtypetable(id);


--
-- Name: feedbacktable feedbacktable_initiator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedbacktable
    ADD CONSTRAINT feedbacktable_initiator_id_fkey FOREIGN KEY (initiator_id) REFERENCES public.usertable(id);


--
-- Name: imagetable imagetable_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagetable
    ADD CONSTRAINT imagetable_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.eventlogtable(id);


--
-- Name: notificationtable notificationtable_initiator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificationtable
    ADD CONSTRAINT notificationtable_initiator_id_fkey FOREIGN KEY (initiator_id) REFERENCES public.usertable(id);


--
-- Name: sankomtable sankomtable_initiator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sankomtable
    ADD CONSTRAINT sankomtable_initiator_id_fkey FOREIGN KEY (initiator_id) REFERENCES public.usertable(id);


--
-- Name: sankomtable sankomtable_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sankomtable
    ADD CONSTRAINT sankomtable_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.roomtable(id);


--
-- Name: usertable usertable_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable
    ADD CONSTRAINT usertable_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roletable(id);


--
-- Name: usertable usertable_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertable
    ADD CONSTRAINT usertable_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.roomtable(id);


--
-- Name: worktickettable worktickettable_performer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worktickettable
    ADD CONSTRAINT worktickettable_performer_id_fkey FOREIGN KEY (performer_id) REFERENCES public.usertable(id);


--
-- PostgreSQL database dump complete
--

