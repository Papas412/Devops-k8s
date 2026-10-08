-- Apply once to the Desk database (local Postgres or RDS).

CREATE TABLE tickets (
    id               SERIAL PRIMARY KEY,
    title            TEXT NOT NULL,
    body             TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'new',  -- new | open
    acknowledgement  TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE jobs (
    id          SERIAL PRIMARY KEY,
    ticket_id   INTEGER NOT NULL REFERENCES tickets (id),
    type        TEXT NOT NULL,                     -- ack
    status      TEXT NOT NULL DEFAULT 'pending',   -- pending | done
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
