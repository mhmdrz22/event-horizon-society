BEGIN;

CREATE TABLE users (
	full_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	student_id VARCHAR(50),
	phone_number VARCHAR(20),
	role userrole NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	id SERIAL NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE articles (
	title VARCHAR(255) NOT NULL,
	content TEXT NOT NULL,
	status articlestatus NOT NULL,
	review_comments TEXT,
	submitted_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	reviewed_at TIMESTAMP WITH TIME ZONE,
	author_id INTEGER NOT NULL,
	id SERIAL NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(author_id) REFERENCES users (id)
);
CREATE TABLE events (
	title VARCHAR(255) NOT NULL,
	description TEXT,
	event_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
	location VARCHAR(255) NOT NULL,
	capacity INTEGER NOT NULL,
	registered_count INTEGER NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	organizer_id INTEGER NOT NULL,
	id SERIAL NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT cc_registered_count_less_than_equal_capacity CHECK (registered_count <= capacity),
	CONSTRAINT cc_capacity_positive CHECK (capacity > 0),
	CONSTRAINT cc_registered_count_non_negative CHECK (registered_count >= 0),
	FOREIGN KEY(organizer_id) REFERENCES users (id)
);
CREATE TABLE membership_requests (
	user_id INTEGER NOT NULL,
	status membershiprequeststatus NOT NULL,
	requested_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	reviewed_at TIMESTAMP WITH TIME ZONE,
	id SERIAL NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE news (
	title VARCHAR(255) NOT NULL,
	content TEXT NOT NULL,
	status newsstatus NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	author_id INTEGER NOT NULL,
	id SERIAL NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(author_id) REFERENCES users (id)
);
CREATE TABLE comments (
	content TEXT NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	user_id INTEGER NOT NULL,
	news_id INTEGER,
	event_id INTEGER,
	id SERIAL NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT cc_comment_target_xor CHECK ((news_id IS NOT NULL AND event_id IS NULL) OR (news_id IS NULL AND event_id IS NOT NULL)),
	FOREIGN KEY(user_id) REFERENCES users (id),
	FOREIGN KEY(news_id) REFERENCES news (id),
	FOREIGN KEY(event_id) REFERENCES events (id)
);
CREATE TABLE event_registrations (
	user_id INTEGER NOT NULL,
	event_id INTEGER NOT NULL,
	registered_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	id SERIAL NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT uq_user_event_registration UNIQUE (user_id, event_id),
	FOREIGN KEY(user_id) REFERENCES users (id),
	FOREIGN KEY(event_id) REFERENCES events (id)
);

COMMIT;
