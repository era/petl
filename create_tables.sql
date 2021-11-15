CREATE TABLE IF NOT EXISTS twitter_followers (user_id INTEGER, updated TEXT);

-- for text based tables use FTS5
CREATE VIRTUAL TABLE twitter_likes USING fts5(id, text);

CREATE VIRTUAL TABLE twitter_tweets USING fts5(id, text);
