CREATE TABLE music (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    artist VARCHAR(100),
    genre VARCHAR(50),
    spotify_id VARCHAR(255)
);
drop table music