--- A dump of notes-related tables as of 21-Oct-2013.

CREATE TABLE notes (
    id integer NOT NULL,
    latitude integer NOT NULL,
    longitude integer NOT NULL,
    tile bigint NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    status note_status_enum NOT NULL,
    closed_at timestamp without time zone
);

CREATE TABLE note_comments (
    id integer NOT NULL,
    note_id bigint NOT NULL,
    visible boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    author_ip inet,
    author_id bigint,
    body text,
    event note_event_enum
);

--- Enums:
-- note_status_enum = { open, closed, hidden }
-- note_event_enum = { opened, closed, reopened, commented, hidden }
