-- SCHEMA :

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('customer', 'barber', 'guest')),
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Barbershops (
    barbershop_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lng DECIMAL(11, 8) NOT NULL,
    phone VARCHAR(20),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE BarberProfiles (
    barber_profile_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    barbershop_id INT REFERENCES Barbershops(barbershop_id),
    bio TEXT,
    specialties TEXT[],
    average_rating DECIMAL(2,1) DEFAULT 0.0,
    total_reviews INT DEFAULT 0,
    profile_image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Posts (
    post_id SERIAL PRIMARY KEY,
    barber_profile_id INT NOT NULL REFERENCES BarberProfiles(barber_profile_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    description TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    barber_profile_id INT NOT NULL REFERENCES BarberProfiles(barber_profile_id) ON DELETE CASCADE,
    customer_user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(barber_profile_id, customer_user_id)
);

CREATE TABLE Follows (
    follow_id SERIAL PRIMARY KEY,
    customer_user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    barber_profile_id INT NOT NULL REFERENCES BarberProfiles(barber_profile_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(customer_user_id, barber_profile_id)
);

-- Indexes for performance (as per your requirements)
CREATE INDEX idx_posts_created_at ON Posts(created_at DESC);
CREATE INDEX idx_barber_rating ON BarberProfiles(average_rating DESC);
CREATE INDEX idx_posts_barber ON Posts(barber_profile_id);
CREATE INDEX idx_reviews_barber ON Reviews(barber_profile_id);




---- INSERTION -----

-- =========================
-- 5 fake customers
-- =========================
INSERT INTO Users (email, username, password_hash, role, location_lat, location_lng)
VALUES
('john.customer@snipsnap.test',   'john_customer',   'hash_john_123',   'customer', 50.79890000, -1.09170000),
('emma.customer@snipsnap.test',   'emma_customer',   'hash_emma_123',   'customer', 50.79920000, -1.08990000),
('liam.customer@snipsnap.test',   'liam_customer',   'hash_liam_123',   'customer', 50.79760000, -1.09430000),
('olivia.customer@snipsnap.test', 'olivia_customer', 'hash_olivia_123', 'customer', 50.80010000, -1.08750000),
('noah.customer@snipsnap.test',   'noah_customer',   'hash_noah_123',   'customer', 50.79690000, -1.09610000)
ON CONFLICT DO NOTHING;


-- ======================
-- 3 fake barbers
-- ======================
INSERT INTO Users (email, username, password_hash, role, location_lat, location_lng)
VALUES
('alex.barber@snipsnap.test',  'alex_barber',  'hash_alex_123',  'barber', 50.79980000, -1.09020000),
('marco.barber@snipsnap.test', 'marco_barber', 'hash_marco_123', 'barber', 50.79830000, -1.09290000),
('sam.barber@snipsnap.test',   'sam_barber',   'hash_sam_123',   'barber', 50.79790000, -1.08880000)
ON CONFLICT DO NOTHING;


-- =========================
-- 2 fake barbershops
-- =========================
INSERT INTO Barbershops (name, address, location_lat, location_lng, phone, website)
VALUES
('Portsmouth Fade House', '12 Queen St, Portsmouth, PO1', 50.79895000, -1.09110000, '+44 7700 900111', 'https://fadehouse.example'),
('Southsea Clippers',     '7 Elm Grove, Southsea, PO5',   50.78580000, -1.07690000, '+44 7700 900222', 'https://southseeclippers.example');


-- ============================
--  3 fake barber profiles
--  (links Users -> Barbershops)
-- ============================
INSERT INTO BarberProfiles (user_id, barbershop_id, bio, specialties, average_rating, total_reviews, profile_image_url)
VALUES
(
  (SELECT user_id FROM Users WHERE username='alex_barber'),
  (SELECT barbershop_id FROM Barbershops WHERE name='Portsmouth Fade House'),
  'Precision fades, clean lineups, and modern styles.',
  ARRAY['fade','lineup','textured crop'],
  4.8, 120,
  'https://pics.example/alex.jpg'
),
(
  (SELECT user_id FROM Users WHERE username='marco_barber'),
  (SELECT barbershop_id FROM Barbershops WHERE name='Southsea Clippers'),
  'Classic cuts with sharp beard work. Fast, clean, consistent.',
  ARRAY['beard trim','taper','classic cut'],
  4.6, 85,
  'https://pics.example/marco.jpg'
),
(
  (SELECT user_id FROM Users WHERE username='sam_barber'),
  (SELECT barbershop_id FROM Barbershops WHERE name='Portsmouth Fade House'),
  'Premium styling, scissor work, and wedding-ready grooming.',
  ARRAY['scissor cut','styling','grooming'],
  4.7, 102,
  'https://pics.example/sam.jpg'
)
ON CONFLICT (user_id) DO NOTHING;


-- ======================
--  10 fake posts
-- ======================
INSERT INTO Posts (barber_profile_id, image_url, description, tags)
VALUES
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='alex_barber'),
 'https://pics.example/posts/alex_01.jpg', 'Fresh skin fade with a crisp finish.', ARRAY['fade','skin-fade','clean']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='alex_barber'),
 'https://pics.example/posts/alex_02.jpg', 'Low fade + textured top for everyday style.', ARRAY['low-fade','texture']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='alex_barber'),
 'https://pics.example/posts/alex_03.jpg', 'Sharp lineup for a bold look.', ARRAY['lineup','sharp']),

((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='marco_barber'),
 'https://pics.example/posts/marco_01.jpg', 'Beard shaping with smooth blend.', ARRAY['beard','shape-up']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='marco_barber'),
 'https://pics.example/posts/marco_02.jpg', 'Classic gentleman cut with tidy sides.', ARRAY['classic','smart']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='marco_barber'),
 'https://pics.example/posts/marco_03.jpg', 'Buzz cut, clean and simple.', ARRAY['buzzcut','minimal']),

((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='sam_barber'),
 'https://pics.example/posts/sam_01.jpg', 'Scissor cut with natural flow.', ARRAY['scissor','natural']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='sam_barber'),
 'https://pics.example/posts/sam_02.jpg', 'Wedding-ready grooming package.', ARRAY['wedding','grooming']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='sam_barber'),
 'https://pics.example/posts/sam_03.jpg', 'Modern taper with clean edges.', ARRAY['taper','modern']),
((SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='alex_barber'),
 'https://pics.example/posts/alex_04.jpg', 'Before/after transformation — major upgrade.', ARRAY['before-after','transformation']);


-- =======================
--  5 fake reviews
-- (unique per barber+customer)
-- =======================
INSERT INTO Reviews (barber_profile_id, customer_user_id, rating, comment)
VALUES
(
  (SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='alex_barber'),
  (SELECT user_id FROM Users WHERE username='john_customer'),
  5, 'Top-tier fade. Super clean finish.'
),
(
  (SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='marco_barber'),
  (SELECT user_id FROM Users WHERE username='emma_customer'),
  4, 'Great beard work and friendly service.'
),
(
  (SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='sam_barber'),
  (SELECT user_id FROM Users WHERE username='liam_customer'),
  5, 'Best haircut I’ve had in a long time.'
),
(
  (SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='alex_barber'),
  (SELECT user_id FROM Users WHERE username='olivia_customer'),
  5, 'Perfect edges and exactly what I asked for.'
),
(
  (SELECT bp.barber_profile_id FROM BarberProfiles bp JOIN Users u ON u.user_id=bp.user_id WHERE u.username='marco_barber'),
  (SELECT user_id FROM Users WHERE username='noah_customer'),
  4, 'Quick, clean, and consistent.'
)
ON CONFLICT (barber_profile_id, customer_user_id) DO NOTHING;
