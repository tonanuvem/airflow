#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TYPE "products_status" AS ENUM (
    'out_of_stock',
    'in_stock',
    'running_low'
  );
  CREATE TABLE "products" (
    "id" SERIAL PRIMARY KEY,
    "name_description" varchar,
    "price" int,
    "quantity" int,
    "status" products_status,
    "created_at" TIMESTAMPTZ DEFAULT Now()
  );
  CREATE INDEX "product_status" ON "products" ("status");
  CREATE UNIQUE INDEX ON "products" ("id");
  
  INSERT INTO products (name_description,price,quantity,status) VALUES ('Camisa branca tipo polo', 69, 5, 'in_stock');
  INSERT INTO products (name_description,price,quantity,status) VALUES ('Bermuda preta sem bolso', 29, 5, 'in_stock');
  INSERT INTO products (name_description,price,quantity,status) VALUES ('Meia preta do tipo social', 19, 5, 'in_stock');  
EOSQL
