-- ============================================
-- SNIPSNAP DATABASE - CORE QUERIES FILE
-- Author: Database Team
-- Project: SnipSnap - Barber Discovery App
-- University of Portsmouth - Group 7E
-- ============================================


-- ============================================
-- 1. AUTHENTICATION QUERIES
-- ============================================

-- Login: Fetch user by email (back-end compares password hash)
SELECT user_id, username, role, password_hash
FROM Users
WHERE email = 'user@email.com';

-- Signup: Insert new customer
INSERT INTO Users (email, username, password_hash, role, location_lat, location_lng)
VALUES ('user@email.com', 'username123', 'hashed_password_here', 'customer', 51.7949, -1.2542);

-- Signup: Insert new barber
INSERT INTO Users (email, username, password_hash, role)
VALUES ('barber@email.com', 'barber_username', 'hashed_password_here', 'barber');

-- Check if email already exists (prevent duplicate accounts)
SELECT COUNT(*) FROM Users
WHERE email = 'user@email.com';

-- Check if username already taken
SELECT COUNT(*) FROM Users
WHERE username = 'username123';

-- Fetch user by ID (for session token validation)
SELECT user_id, username, email, role
FROM Users
WHERE user_id = 1;


-- ============================================
-- 2. BARBER PROFILE QUERIES
-- ============================================

-- Create barber profile after barber signs up
INSERT INTO BarberProfiles (user_id, barbershop_id, bio, specialties)
VALUES (1, 1, 'Expert in fades and modern cuts.', ARRAY['Fades', 'Beard Trim', 'Design']);

-- Fetch full barber profile by barber_profile_id
SELECT 
    bp.barber_profile_id,
    u.username,
    u.email,
    bp.bio,
    bp.specialties,
    bp.average_rating,
    bp.total_reviews,
    bp.profile_image_url,
    bs.name AS barbershop_name,
    bs.address AS barbershop_address,
    bs.location_lat,
    bs.location_lng,
    bs.website
FROM BarberProfiles bp
JOIN Users u ON bp.user_id = u.user_id
LEFT JOIN Barbershops bs ON bp.barbershop_id = bs.barbershop_id
WHERE bp.barber_profile_id = 1;

-- Fetch barber profile by user_id (for dashboard)
SELECT 
    bp.barber_profile_id,
    bp.bio,
    bp.specialties,
    bp.average_rating,
    bp.total_reviews,
    bp.profile_image_url
FROM BarberProfiles bp
WHERE bp.user_id = 1;

-- Update barber profile info (from dashboard)
UPDATE BarberProfiles
SET bio = 'Updated bio here', 
    specialties = ARRAY['Fades', 'Curly Hair', 'Hot Towel Shave'],
    profile_image_url = 'https://image-url.com/pic.jpg'
WHERE user_id = 1;

-- Update barber's linked barbershop
UPDATE BarberProfiles
SET barbershop_id = 2
WHERE user_id = 1;


-- ============================================
-- 3. BARBERSHOP QUERIES
-- ============================================

-- Create a new barbershop
INSERT INTO Barbershops (name, address, location_lat, location_lng, phone, website)
VALUES ('Cuts & Glory', '12 High Street, Portsmouth', 50.7989, -1.0912, '02392123456', 'https://cutsandglory.com');

-- Fetch barbershop by ID
SELECT * FROM Barbershops
WHERE barbershop_id = 1;

-- Fetch all barbers in a specific barbershop
SELECT 
    bp.barber_profile_id,
    u.username,
    bp.specialties,
    bp.average_rating,
    bp.profile_image_url
FROM BarberProfiles bp
JOIN Users u ON bp.user_id = u.user_id
WHERE bp.barbershop_id = 1;

-- Fetch all barbershops (for interactive map pins)
SELECT 
    barbershop_id,
    name,
    address,
    location_lat,
    location_lng
FROM Barbershops;


-- ============================================
-- 4. POSTS / DISCOVER FEED QUERIES
-- ============================================

-- Create a new post (barber uploading to discover page)
INSERT INTO Posts (barber_profile_id, image_url, description, tags)
VALUES (1, 'https://image-url.com/haircut.jpg', 'Fresh fade done today!', ARRAY['fade', 'short hair', 'design']);

-- Basic discover feed: Fetch 10 most recent posts
SELECT 
    p.post_id,
    p.image_url,
    p.description,
    p.tags,
    p.created_at,
    bp.barber_profile_id,
    u.username AS barber_name,
    bp.average_rating,
    bp.profile_image_url,
    bs.location_lat,
    bs.location_lng
FROM Posts p
JOIN BarberProfiles bp ON p.barber_profile_id = bp.barber_profile_id
JOIN Users u ON bp.user_id = u.user_id
LEFT JOIN Barbershops bs ON bp.barbershop_id = bs.barbershop_id
ORDER BY p.created_at DESC
LIMIT 10 OFFSET 0;  -- Change OFFSET for pagination (0, 10, 20...)

-- Discover feed: Filter by tag (e.g., "fade")
SELECT 
    p.post_id,
    p.image_url,
    p.description,
    p.tags,
    p.created_at,
    u.username AS barber_name,
    bp.average_rating
FROM Posts p
JOIN BarberProfiles bp ON p.barber_profile_id = bp.barber_profile_id
JOIN Users u ON bp.user_id = u.user_id
WHERE 'fade' = ANY(p.tags)
ORDER BY p.created_at DESC
LIMIT 10 OFFSET 0;

-- Discover feed: Filter by followed barbers only
SELECT 
    p.post_id,
    p.image_url,
    p.description,
    p.created_at,
    u.username AS barber_name,
    bp.average_rating
FROM Posts p
JOIN BarberProfiles bp ON p.barber_profile_id = bp.barber_profile_id
JOIN Users u ON bp.user_id = u.user_id
JOIN Follows f ON f.barber_profile_id = bp.barber_profile_id
WHERE f.customer_user_id = 1  -- Replace with logged in user's ID
ORDER BY p.created_at DESC
LIMIT 10 OFFSET 0;

-- Discover feed: Filter by highest rated barbers
SELECT 
    p.post_id,
    p.image_url,
    p.description,
    u.username AS barber_name,
    bp.average_rating
FROM Posts p
JOIN BarberProfiles bp ON p.barber_profile_id = bp.barber_profile_id
JOIN Users u ON bp.user_id = u.user_id
ORDER BY bp.average_rating DESC
LIMIT 10 OFFSET 0;

-- Delete a post (barber removes their own post)
DELETE FROM Posts
WHERE post_id = 1 AND barber_profile_id = 1;

-- Fetch all posts by a specific barber (for barber profile page gallery)
SELECT 
    post_id,
    image_url,
    description,
    tags,
    created_at
FROM Posts
WHERE barber_profile_id = 1
ORDER BY created_at DESC;


-- ============================================
-- 5. REVIEW QUERIES
-- ============================================

-- Submit a new review
INSERT INTO Reviews (barber_profile_id, customer_user_id, rating, comment)
VALUES (1, 2, 5, 'Best fade I have ever had, highly recommend!');

-- Fetch all reviews for a barber
SELECT 
    r.review_id,
    r.rating,
    r.comment,
    r.created_at,
    u.username AS customer_name,
    u.user_id AS customer_id
FROM Reviews r
JOIN Users u ON r.customer_user_id = u.user_id
WHERE r.barber_profile_id = 1
ORDER BY r.created_at DESC;

-- Fetch total review count and average rating for a barber
SELECT 
    COUNT(*) AS total_reviews,
    ROUND(AVG(rating), 1) AS average_rating
FROM Reviews
WHERE barber_profile_id = 1
  AND created_at >= NOW() - INTERVAL '1 year';  -- Only last year's reviews

-- Update a review (customer edits their review)
UPDATE Reviews
SET rating = 4, comment = 'Updated my review - still great!'
WHERE review_id = 1 AND customer_user_id = 2;  -- Must be the review owner

-- Delete a review (customer removes their review)
DELETE FROM Reviews
WHERE review_id = 1 AND customer_user_id = 2;  -- Must be the review owner

-- Update barber average rating after a review is added/edited/deleted
UPDATE BarberProfiles
SET 
    average_rating = (
        SELECT ROUND(AVG(rating), 1)
        FROM Reviews
        WHERE barber_profile_id = 1
          AND created_at >= NOW() - INTERVAL '1 year'
    ),
    total_reviews = (
        SELECT COUNT(*)
        FROM Reviews
        WHERE barber_profile_id = 1
    )
WHERE barber_profile_id = 1;


-- ============================================
-- 6. FOLLOW QUERIES
-- ============================================

-- Follow a barber
INSERT INTO Follows (customer_user_id, barber_profile_id)
VALUES (2, 1);

-- Unfollow a barber
DELETE FROM Follows
WHERE customer_user_id = 2 AND barber_profile_id = 1;

-- Check if customer already follows a barber (to toggle follow/unfollow button)
SELECT COUNT(*) FROM Follows
WHERE customer_user_id = 2 AND barber_profile_id = 1;

-- Fetch all barbers a customer follows
SELECT 
    bp.barber_profile_id,
    u.username AS barber_name,
    bp.profile_image_url,
    bp.average_rating
FROM Follows f
JOIN BarberProfiles bp ON f.barber_profile_id = bp.barber_profile_id
JOIN Users u ON bp.user_id = u.user_id
WHERE f.customer_user_id = 2;

-- Count how many followers a barber has
SELECT COUNT(*) AS total_followers
FROM Follows
WHERE barber_profile_id = 1;


-- ============================================
-- 7. USEFUL ADMIN / DEBUG QUERIES
-- ============================================

-- See all tables in the database
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Count rows in each table (health check)
SELECT 'Users' AS table_name, COUNT(*) FROM Users
UNION ALL
SELECT 'BarberProfiles', COUNT(*) FROM BarberProfiles
UNION ALL
SELECT 'Barbershops', COUNT(*) FROM Barbershops
UNION ALL
SELECT 'Posts', COUNT(*) FROM Posts
UNION ALL
SELECT 'Reviews', COUNT(*) FROM Reviews
UNION ALL
SELECT 'Follows', COUNT(*) FROM Follows;

-- Fetch everything about a specific user (debugging)
SELECT 
    u.user_id, u.username, u.email, u.role,
    bp.barber_profile_id, bp.bio, bp.average_rating
FROM Users u
LEFT JOIN BarberProfiles bp ON u.user_id = bp.user_id
WHERE u.user_id = 1;