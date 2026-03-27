-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.app_user (
  user_id integer NOT NULL DEFAULT nextval('app_user_user_id_seq'::regclass),
  email character varying NOT NULL UNIQUE,
  username character varying NOT NULL UNIQUE,
  location_lat double precision,
  location_lng double precision,
  postcode character,
  created_at timestamp without time zone DEFAULT now(),
  role character varying NOT NULL CHECK (role::bpchar = ANY (ARRAY['customer'::bpchar, 'barber'::bpchar, 'guest'::bpchar])),
  auth_user_id uuid UNIQUE,
  CONSTRAINT app_user_pkey PRIMARY KEY (user_id)
);
CREATE TABLE public.barber (
  barber_id integer NOT NULL DEFAULT nextval('barber_barber_id_seq'::regclass),
  user_id integer NOT NULL UNIQUE,
  barbershop_id integer NOT NULL,
  bio text,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT barber_pkey PRIMARY KEY (barber_id),
  CONSTRAINT barber_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(user_id),
  CONSTRAINT barber_barbershop_id_fkey FOREIGN KEY (barbershop_id) REFERENCES public.barbershop(barbershop_id)
);
CREATE TABLE public.barber_tag (
  barber_id integer NOT NULL,
  tag_id integer NOT NULL,
  CONSTRAINT barber_tag_pkey PRIMARY KEY (barber_id, tag_id),
  CONSTRAINT barber_tag_barber_id_fkey FOREIGN KEY (barber_id) REFERENCES public.barber(barber_id),
  CONSTRAINT barber_tag_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(tag_id)
);
CREATE TABLE public.barbershop (
  barbershop_id integer NOT NULL DEFAULT nextval('barbershop_barbershop_id_seq'::regclass),
  name character varying NOT NULL,
  postcode character NOT NULL,
  location_lat double precision NOT NULL,
  location_lng double precision NOT NULL,
  phone character varying,
  website character varying,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT barbershop_pkey PRIMARY KEY (barbershop_id)
);
CREATE TABLE public.follow (
  follow_id integer NOT NULL DEFAULT nextval('follow_follow_id_seq'::regclass),
  user_id integer NOT NULL,
  barber_id integer NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT follow_pkey PRIMARY KEY (follow_id),
  CONSTRAINT follow_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(user_id),
  CONSTRAINT follow_barber_id_fkey FOREIGN KEY (barber_id) REFERENCES public.barber(barber_id)
);
CREATE TABLE public.haircutphoto (
  photo_id integer NOT NULL DEFAULT nextval('haircutphoto_photo_id_seq'::regclass),
  barber_id integer NOT NULL,
  image_url character varying NOT NULL,
  width_px integer NOT NULL,
  height_px integer NOT NULL,
  status character DEFAULT 'show'::bpchar CHECK (status = ANY (ARRAY['show'::bpchar, 'hide'::bpchar])),
  main_tag integer,
  is_post boolean DEFAULT false,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT haircutphoto_pkey PRIMARY KEY (photo_id),
  CONSTRAINT haircutphoto_barber_id_fkey FOREIGN KEY (barber_id) REFERENCES public.barber(barber_id),
  CONSTRAINT haircutphoto_main_tag_fkey FOREIGN KEY (main_tag) REFERENCES public.tag(tag_id)
);
CREATE TABLE public.haircutphoto_tag (
  photo_id integer NOT NULL,
  tag_id integer NOT NULL,
  CONSTRAINT haircutphoto_tag_pkey PRIMARY KEY (photo_id, tag_id),
  CONSTRAINT haircutphoto_tag_photo_id_fkey FOREIGN KEY (photo_id) REFERENCES public.haircutphoto(photo_id),
  CONSTRAINT haircutphoto_tag_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(tag_id)
);
CREATE TABLE public.profilephoto (
  photo_id integer NOT NULL DEFAULT nextval('profilephoto_photo_id_seq'::regclass),
  user_id integer NOT NULL UNIQUE,
  image_url character varying NOT NULL,
  width_px integer NOT NULL,
  height_px integer NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT profilephoto_pkey PRIMARY KEY (photo_id),
  CONSTRAINT profilephoto_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(user_id)
);
CREATE TABLE public.review (
  review_id integer NOT NULL DEFAULT nextval('review_review_id_seq'::regclass),
  parent_review_id integer,
  target_barber_id integer,
  target_barbershop_id integer,
  user_id integer NOT NULL,
  status character DEFAULT 'show'::bpchar CHECK (status = ANY (ARRAY['show'::bpchar, 'hide'::bpchar])),
  text text NOT NULL,
  rating integer CHECK (rating >= 1 AND rating <= 5),
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT review_pkey PRIMARY KEY (review_id),
  CONSTRAINT review_parent_review_id_fkey FOREIGN KEY (parent_review_id) REFERENCES public.review(review_id),
  CONSTRAINT review_target_barber_id_fkey FOREIGN KEY (target_barber_id) REFERENCES public.barber(barber_id),
  CONSTRAINT review_target_barbershop_id_fkey FOREIGN KEY (target_barbershop_id) REFERENCES public.barbershop(barbershop_id),
  CONSTRAINT review_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(user_id)
);
CREATE TABLE public.review_helpful_vote (
  review_id integer NOT NULL,
  user_id integer NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT review_helpful_vote_pkey PRIMARY KEY (review_id, user_id),
  CONSTRAINT review_helpful_vote_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.review(review_id),
  CONSTRAINT review_helpful_vote_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(user_id)
);
CREATE TABLE public.shift (
  shift_id integer NOT NULL DEFAULT nextval('shift_shift_id_seq'::regclass),
  barber_id integer NOT NULL,
  day_of_week integer NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
  start_time time without time zone NOT NULL,
  end_time time without time zone NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT shift_pkey PRIMARY KEY (shift_id),
  CONSTRAINT shift_barber_id_fkey FOREIGN KEY (barber_id) REFERENCES public.barber(barber_id)
);
CREATE TABLE public.tag (
  tag_id integer NOT NULL DEFAULT nextval('tag_tag_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT tag_pkey PRIMARY KEY (tag_id)
);