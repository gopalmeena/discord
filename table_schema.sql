CREATE TABLE user_queries (
	id serial PRIMARY KEY, 
	user_id varchar(25) NOT NULL,
	query varchar(250) NOT NULL,
	searched_at timestamp NOT NULL
)