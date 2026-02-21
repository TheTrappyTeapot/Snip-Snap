-- SCHEMA :

CREATE TABLE IF NOT EXISTS App_User (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    location_lat DOUBLE PRECISION,
    location_lng DOUBLE PRECISION,
    postcode CHAR(8),
    created_at TIMESTAMP DEFAULT now(),
    role CHAR(8) NOT NULL CHECK (role IN ('customer', 'barber', 'guest'))
);

CREATE TABLE IF NOT EXISTS Barbershop (
    barbershop_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    postcode CHAR(8) NOT NULL,
    location_lat DOUBLE PRECISION NOT NULL,
    location_lng DOUBLE PRECISION NOT NULL,
    phone VARCHAR(20),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS Barber (
    barber_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    barbershop_id INT REFERENCES Barbershop(barbershop_id),
    bio TEXT,
    average_rating DECIMAL(2,1) DEFAULT 0.0,
    profile_image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS HaircutPhoto (
    photo_id SERIAL PRIMARY KEY,
    barber_id INT NOT NULL REFERENCES Barber(barber_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    width_px INT NOT NULL,
    height_px INT NOT NULL,
    status CHAR(4) CHECK (status IN ('show', 'hide')) DEFAULT 'show',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS Review (
    review_id SERIAL PRIMARY KEY,
    parent_review_id INT REFERENCES Review(review_id) ON DELETE CASCADE,

    -- Split polymorphic target into two nullable FKs
    target_barber_id INT REFERENCES Barber(barber_id) ON DELETE CASCADE,
    target_barbershop_id INT REFERENCES Barbershop(barbershop_id) ON DELETE CASCADE,

    user_id INT NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    status CHAR(4) CHECK (status IN ('show', 'hide')) DEFAULT 'show',
    text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT now(),

    -- Exactly one target must be set
    CONSTRAINT review_exactly_one_target_chk CHECK (
        (target_barber_id IS NOT NULL AND target_barbershop_id IS NULL) OR
        (target_barber_id IS NULL AND target_barbershop_id IS NOT NULL)
    ),

    -- Top-level reviews must have rating; replies must not have rating
    CONSTRAINT review_rating_top_level_only_chk CHECK (
        (parent_review_id IS NULL AND rating IS NOT NULL) OR
        (parent_review_id IS NOT NULL AND rating IS NULL)
    )
);

CREATE TABLE IF NOT EXISTS Review_Helpful_Vote (
    review_id INT NOT NULL REFERENCES Review(review_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (review_id, user_id)
);

CREATE TABLE IF NOT EXISTS Follow (
    follow_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    barber_id INT NOT NULL REFERENCES Barber(barber_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE(user_id, barber_id)
);

CREATE TABLE IF NOT EXISTS Tag (
    tag_id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS HaircutPhoto_Tag (
    photo_id INT NOT NULL REFERENCES HaircutPhoto(photo_id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES Tag(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (photo_id, tag_id)
);

CREATE TABLE IF NOT EXISTS Barber_Tag (
    barber_id INT NOT NULL REFERENCES Barber(barber_id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES Tag(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (barber_id, tag_id)
);



INSERT INTO App_User (email, username, role)
VALUES
-- customers
('cust1@snipsnap.dev', 'Tony Blair', 'customer'),
('cust2@snipsnap.dev', 'Joe Biden', 'customer'),
('cust3@snipsnap.dev', 'Donald Trump', 'customer'),

-- barbers (linked later)
('barber1@snipsnap.dev', 'Queen Elizibeth', 'barber'),
('barber2@snipsnap.dev', 'Princess Diana', 'barber'),
('barber3@snipsnap.dev', 'Gordon Brown', 'barber'),
('barber4@snipsnap.dev', 'Keir Starmer', 'barber'),
('barber5@snipsnap.dev', 'Rachel Reaves', 'barber'),
('barber6@snipsnap.dev', 'Margret Thatcher', 'barber'),

-- guest
('guest@snipsnap.dev', 'guest1', 'guest');


INSERT INTO Barbershop (name, postcode, location_lat, location_lng)
VALUES
(
  'Fade Factory',
  'PO1 2SB',
  50.79536421032783,
  -1.0941994724762119
),
(
  'Sharp Cuts',
  'PO1 2DU',
  50.79808043529969,
  -1.0916402828737106
);


INSERT INTO Barber (user_id, barbershop_id, bio)
VALUES
-- Shop 1
(4, 1, 'Classic cuts and fades'),
(5, 1, 'Skin fades and tapers'),
(6, 1, 'Modern styles and trims'),

-- Shop 2
(7, 2, 'Precision cutting specialist'),
(8, 2, 'Beards and styling expert'),
(9, 2, 'Creative modern barber');


INSERT INTO HaircutPhoto (barber_id, image_url, width_px, height_px)
VALUES
(1, '/static/uploads/haircuts/image.png', 183, 275),
(2, '/static/uploads/haircuts/image1.png', 225, 225),
(3, '/static/uploads/haircuts/image2.png', 205, 246),
(4, '/static/uploads/haircuts/image3.png', 225, 225),
(5, '/static/uploads/haircuts/image4.png', 214, 235),
(6, '/static/uploads/haircuts/image5.png', 201, 250),
(1, '/static/uploads/haircuts/image6.png', 194, 259),
(2, '/static/uploads/haircuts/image7.png', 168, 299),
(3, '/static/uploads/haircuts/image8.png', 183, 275),
(4, '/static/uploads/haircuts/image9.png', 206, 244);


INSERT INTO HaircutPhoto_Tag (photo_id, tag_id)
SELECT p.photo_id, t.tag_id
FROM (
    VALUES
    (1, 'fade'),
    (1, 'short'),
    (1, 'modern'),

    (2, 'skin fade'),
    (2, 'taper'),
    (2, 'clean shave'),

    (3, 'quiff'),
    (3, 'medium'),
    (3, 'classic'),

    (4, 'pompadour'),
    (4, 'medium'),
    (4, 'slick back'),

    (5, 'buzz cut'),
    (5, 'short'),
    (5, 'edgy'),

    (6, 'textured crop'),
    (6, 'fringe'),
    (6, 'modern'),

    (7, 'undercut'),
    (7, 'slick back'),
    (7, 'classic'),

    (8, 'crop'),
    (8, 'short'),
    (8, 'modern'),

    (9, 'beard'),
    (9, 'beard trim'),
    (9, 'classic'),

    (10, 'line up'),
    (10, 'fade'),
    (10, 'edgy')
) AS m(photo_id, tag_name)
JOIN Tag t ON t.name = m.tag_name
JOIN HaircutPhoto p ON p.photo_id = m.photo_id
ON CONFLICT DO NOTHING;


INSERT INTO Barber_Tag (barber_id, tag_id)
SELECT b.barber_id, t.tag_id
FROM (
    VALUES
    (1, 'fade'),
    (1, 'skin fade'),
    (1, 'modern'),

    (2, 'taper'),
    (2, 'classic'),
    (2, 'clean shave'),

    (3, 'quiff'),
    (3, 'pompadour'),
    (3, 'slick back'),

    (4, 'beard'),
    (4, 'beard trim'),
    (4, 'line up'),

    (5, 'buzz cut'),
    (5, 'short'),
    (5, 'edgy'),

    (6, 'textured crop'),
    (6, 'fringe'),
    (6, 'modern')
) AS m(barber_id, tag_name)
JOIN Tag t ON t.name = m.tag_name
JOIN Barber b ON b.barber_id = m.barber_id
ON CONFLICT DO NOTHING;
