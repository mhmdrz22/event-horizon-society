-- Sample Data for University Scientific Association System

BEGIN;

-- Users
-- Passwords are placeholders, actual passwords should be hashed by the application
-- For testing, if using raw SQL, you might insert known test hashes.
-- Hashed password for 'password123' (example bcrypt hash, generate properly in app)
-- UserRole enum values: 'regular', 'member', 'admin'
-- UserRole enum values: 'دانشجو', 'عضو انجمن', 'مدیر انجمن'
INSERT INTO users (id, full_name, email, password_hash, student_id, phone_number, role, created_at, updated_at) VALUES
(1, 'مدیر سیستم', 'admin@example.com', '$2b$12$DUMMYHASHADMINLMNOPQRSTU.Vabcdefghijklmnopqrstuv.abcdefghijkl', 'admin001', '+989120000001', 'مدیر انجمن', NOW(), NOW()),
(2, 'عضو نمونه', 'member@example.com', '$2b$12$DUMMYHASHMEMBERLMNOPQRS.Tabcdefghijklmnopqrstuv.abcdefghijkl', 'member001', '+989120000002', 'عضو انجمن', NOW(), NOW()),
(3, 'دانشجوی نمونه', 'student@example.com', '$2b$12$DUMMYHASHREGULARLMNOPQR.Sabcdefghijklmnopqrstuv.abcdefghijkl', 'user001', '+989120000003', 'دانشجو', NOW(), NOW());

-- News
-- NewsStatus enum values: 'draft', 'published'
-- Assuming admin user (id=1) and member user (id=2) are authors
INSERT INTO news (id, title, content, author_id, status, created_at, updated_at) VALUES
(1, 'First News Post by Admin', 'This is the content of the first news post, created by an admin.', 1, 'published', NOW(), NOW()),
(2, 'Draft News by Member', 'This is a draft news post by a member.', 2, 'draft', NOW(), NOW());

-- Events
-- Assuming admin user (id=1) is the organizer
INSERT INTO events (id, title, description, event_datetime, location, capacity, registered_count, organizer_id, created_at, updated_at) VALUES
(1, 'Tech Workshop', 'A workshop on new technologies.', (NOW() + INTERVAL '7 day'), 'Room 101', 50, 0, 1, NOW(), NOW()),
(2, 'Annual Meetup', 'The annual general meeting for association members.', (NOW() + INTERVAL '30 day'), 'Main Hall', 200, 0, 1, NOW(), NOW());

-- Event Registrations
-- Assuming regular user (id=3) registers for the Tech Workshop (event_id=1)
INSERT INTO event_registrations (user_id, event_id, registered_at) VALUES
(3, 1, NOW());
-- Update registered_count for event 1
UPDATE events SET registered_count = registered_count + 1 WHERE id = 1;

-- Articles
-- ArticleStatus enum values: 'pending', 'approved', 'rejected'
-- Assuming member user (id=2) and regular user (id=3) submit articles
INSERT INTO articles (id, title, content, author_id, status, review_comments, submitted_at, reviewed_at) VALUES
(1, 'My Research Idea', 'Content of the research idea by a member.', 2, 'pending', NULL, NOW(), NULL),
(2, 'Review of Quantum Computing', 'A detailed review article by a regular user.', 3, 'approved', 'Well written article.', NOW(), NOW());

-- Comments
-- User 3 (id=3) comments on News 1 (id=1)
INSERT INTO comments (user_id, news_id, event_id, content, created_at) VALUES
(3, 1, NULL, 'Great news post!', NOW());
-- User 2 (id=2) comments on Event 1 (id=1)
INSERT INTO comments (user_id, news_id, event_id, content, created_at) VALUES
(2, NULL, 1, 'Looking forward to this workshop!', NOW());

-- Membership Requests
-- MembershipRequestStatus enum values: 'pending', 'approved', 'rejected'
-- Regular user (id=3) requests membership
INSERT INTO membership_requests (user_id, status, requested_at, reviewed_at) VALUES
(3, 'pending', NOW(), NULL);

COMMIT;
