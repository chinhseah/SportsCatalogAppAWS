CREATE TABLE catalog_user (
   id serial PRIMARY KEY,
   name VARCHAR (80) NOT NULL,
   email VARCHAR (120) NOT NULL,
   picture VARCHAR(250)
);

CREATE TABLE category (
   id serial PRIMARY KEY,
   name VARCHAR (80) NOT NULL
);

CREATE TABLE category_item (
   id serial PRIMARY KEY,
   name VARCHAR (80) NOT NULL,
   description VARCHAR (250),
   user_id integer NOT NULL, 
   category_id integer NOT NULL,
   create_date timestamp without time zone,
   CONSTRAINT category_item_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES catalog_user (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
   CONSTRAINT category_item_category_id_fkey FOREIGN KEY (category_id)
      REFERENCES category (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);



