DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE url_checks (
    id serial PRIMARY KEY,
    url_id int NOT NULL REFERENCES urls(id) ON DELETE CASCADE,
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);