--
-- PostgreSQL database dump
--

\restrict yBFkTOYVL8JI5kmdm6NzYe6Plyox5HcZbb2PH3OBlJ2iBcjoi0hA0p1wc9DBeRZ

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 16.15 (Debian 16.15-1.pgdg13+2)

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
-- Name: dealer; Type: TABLE; Schema: public; Owner: pavana
--

CREATE TABLE public.dealer (
    dealer_id integer NOT NULL,
    name character varying(30),
    location character varying(30),
    phone_no character varying(12)
);


ALTER TABLE public.dealer OWNER TO pavana;

--
-- Name: dealer_dealer_id_seq; Type: SEQUENCE; Schema: public; Owner: pavana
--

CREATE SEQUENCE public.dealer_dealer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dealer_dealer_id_seq OWNER TO pavana;

--
-- Name: dealer_dealer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pavana
--

ALTER SEQUENCE public.dealer_dealer_id_seq OWNED BY public.dealer.dealer_id;


--
-- Name: product; Type: TABLE; Schema: public; Owner: pavana
--

CREATE TABLE public.product (
    product_id integer NOT NULL,
    name character varying(30),
    category character varying(30),
    unit character varying(10),
    manufacturer character varying(40),
    selling_price numeric(10,2)
);


ALTER TABLE public.product OWNER TO pavana;

--
-- Name: product_product_id_seq; Type: SEQUENCE; Schema: public; Owner: pavana
--

CREATE SEQUENCE public.product_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_product_id_seq OWNER TO pavana;

--
-- Name: product_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pavana
--

ALTER SEQUENCE public.product_product_id_seq OWNED BY public.product.product_id;


--
-- Name: restock; Type: TABLE; Schema: public; Owner: pavana
--

CREATE TABLE public.restock (
    restock_id integer NOT NULL,
    product_id integer,
    dealer_id integer,
    shop_id integer,
    batch_no character varying(30),
    quantity integer,
    cost_price numeric(10,2),
    manufacture_date date,
    expiry_date date,
    order_date date,
    delivery_date date
);


ALTER TABLE public.restock OWNER TO pavana;

--
-- Name: restock_restock_id_seq; Type: SEQUENCE; Schema: public; Owner: pavana
--

CREATE SEQUENCE public.restock_restock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.restock_restock_id_seq OWNER TO pavana;

--
-- Name: restock_restock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pavana
--

ALTER SEQUENCE public.restock_restock_id_seq OWNED BY public.restock.restock_id;


--
-- Name: sale; Type: TABLE; Schema: public; Owner: pavana
--

CREATE TABLE public.sale (
    sale_id integer NOT NULL,
    shop_id integer,
    sale_date date,
    total_amount numeric(10,2)
);


ALTER TABLE public.sale OWNER TO pavana;

--
-- Name: sale_sale_id_seq; Type: SEQUENCE; Schema: public; Owner: pavana
--

CREATE SEQUENCE public.sale_sale_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sale_sale_id_seq OWNER TO pavana;

--
-- Name: sale_sale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pavana
--

ALTER SEQUENCE public.sale_sale_id_seq OWNED BY public.sale.sale_id;


--
-- Name: saleitem; Type: TABLE; Schema: public; Owner: pavana
--

CREATE TABLE public.saleitem (
    sale_item_id integer NOT NULL,
    sale_id integer,
    product_id integer,
    quantity_sold integer,
    price_at_sale numeric(10,2)
);


ALTER TABLE public.saleitem OWNER TO pavana;

--
-- Name: saleitem_sale_item_id_seq; Type: SEQUENCE; Schema: public; Owner: pavana
--

CREATE SEQUENCE public.saleitem_sale_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saleitem_sale_item_id_seq OWNER TO pavana;

--
-- Name: saleitem_sale_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pavana
--

ALTER SEQUENCE public.saleitem_sale_item_id_seq OWNED BY public.saleitem.sale_item_id;


--
-- Name: shop; Type: TABLE; Schema: public; Owner: pavana
--

CREATE TABLE public.shop (
    shop_id integer NOT NULL,
    name character varying(30),
    location character varying(30)
);


ALTER TABLE public.shop OWNER TO pavana;

--
-- Name: shop_shop_id_seq; Type: SEQUENCE; Schema: public; Owner: pavana
--

CREATE SEQUENCE public.shop_shop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shop_shop_id_seq OWNER TO pavana;

--
-- Name: shop_shop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pavana
--

ALTER SEQUENCE public.shop_shop_id_seq OWNED BY public.shop.shop_id;


--
-- Name: dealer dealer_id; Type: DEFAULT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.dealer ALTER COLUMN dealer_id SET DEFAULT nextval('public.dealer_dealer_id_seq'::regclass);


--
-- Name: product product_id; Type: DEFAULT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.product ALTER COLUMN product_id SET DEFAULT nextval('public.product_product_id_seq'::regclass);


--
-- Name: restock restock_id; Type: DEFAULT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.restock ALTER COLUMN restock_id SET DEFAULT nextval('public.restock_restock_id_seq'::regclass);


--
-- Name: sale sale_id; Type: DEFAULT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.sale ALTER COLUMN sale_id SET DEFAULT nextval('public.sale_sale_id_seq'::regclass);


--
-- Name: saleitem sale_item_id; Type: DEFAULT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.saleitem ALTER COLUMN sale_item_id SET DEFAULT nextval('public.saleitem_sale_item_id_seq'::regclass);


--
-- Name: shop shop_id; Type: DEFAULT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.shop ALTER COLUMN shop_id SET DEFAULT nextval('public.shop_shop_id_seq'::regclass);


--
-- Name: dealer dealer_pkey; Type: CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.dealer
    ADD CONSTRAINT dealer_pkey PRIMARY KEY (dealer_id);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (product_id);


--
-- Name: restock restock_pkey; Type: CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.restock
    ADD CONSTRAINT restock_pkey PRIMARY KEY (restock_id);


--
-- Name: sale sale_pkey; Type: CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.sale
    ADD CONSTRAINT sale_pkey PRIMARY KEY (sale_id);


--
-- Name: saleitem saleitem_pkey; Type: CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.saleitem
    ADD CONSTRAINT saleitem_pkey PRIMARY KEY (sale_item_id);


--
-- Name: shop shop_pkey; Type: CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.shop
    ADD CONSTRAINT shop_pkey PRIMARY KEY (shop_id);


--
-- Name: restock restock_dealer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.restock
    ADD CONSTRAINT restock_dealer_id_fkey FOREIGN KEY (dealer_id) REFERENCES public.dealer(dealer_id);


--
-- Name: restock restock_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.restock
    ADD CONSTRAINT restock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(product_id);


--
-- Name: restock restock_shop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.restock
    ADD CONSTRAINT restock_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES public.shop(shop_id);


--
-- Name: sale sale_shop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.sale
    ADD CONSTRAINT sale_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES public.shop(shop_id);


--
-- Name: saleitem saleitem_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.saleitem
    ADD CONSTRAINT saleitem_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(product_id);


--
-- Name: saleitem saleitem_sale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pavana
--

ALTER TABLE ONLY public.saleitem
    ADD CONSTRAINT saleitem_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES public.sale(sale_id);


--
-- PostgreSQL database dump complete
--

\unrestrict yBFkTOYVL8JI5kmdm6NzYe6Plyox5HcZbb2PH3OBlJ2iBcjoi0hA0p1wc9DBeRZ

