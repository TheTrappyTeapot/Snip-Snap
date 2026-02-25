-- SCHEMA :

/*
App_User: Stores all users (customers, barbers, guests). Role field distinguishes types.
*/
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

/*
Barbershop: Stores barbershop details. Location stored as lat/lng for distance calculations.
Each Barber will reference a Barbershop.
*/
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

/*
Barber: Stores barber details. Each barber is linked to one App_User and one Barbershop.
Bio, average rating, and profile image URL are stored here for easy access when displaying barber profiles
*/
CREATE TABLE IF NOT EXISTS Barber (
    barber_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    barbershop_id INT NOT NULL REFERENCES Barbershop(barbershop_id),
    bio TEXT,
    created_at TIMESTAMP DEFAULT now()
);


/* 
Barber timetable data. 
A barber may have less than 7 shifts per week. 
If a barber has no shift for a given day, they simply won't have a record for that day.
*/
CREATE TABLE IF NOT EXISTS Shift (
    shift_id SERIAL PRIMARY KEY,
    barber_id INT NOT NULL REFERENCES Barber(barber_id) ON DELETE CASCADE,
    day_of_week INT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    CHECK (end_time > start_time)
);

/*
Tag: Stores tags that can be associated with haircut photos and barbers. This allows for flexible categorization and searching of haircuts and barbers based on styles, techniques, or other attributes represented by tags.
*/
CREATE TABLE IF NOT EXISTS Tag (
    tag_id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);


/*
HaircutPhoto: Stores photos of haircuts done by barbers. Each photo is linked to one barber.
is_post indicates whether the photo is a to be used in a post (true) or just a regular gallery photo (false). 
This allows barbers to have photos that are not currently being promoted in posts, but can be used later without 
needing to re-upload. The main_tag field allows one tag to be designated as the primary tag for the photo, 
which can be used for sorting and display purposes.
*/
CREATE TABLE IF NOT EXISTS HaircutPhoto (
    photo_id SERIAL PRIMARY KEY,
    barber_id INT NOT NULL REFERENCES Barber(barber_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    width_px INT NOT NULL,
    height_px INT NOT NULL,
    status CHAR(4) CHECK (status IN ('show', 'hide')) DEFAULT 'show',
    main_tag INT REFERENCES Tag(tag_id),
    is_post BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now()
);

/*
Each user can have one profile photo. This is stored separately from haircut photos to allow for different handling and display.
*/
CREATE TABLE IF NOT EXISTS ProfilePhoto (
    photo_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    width_px INT NOT NULL,
    height_px INT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

/*
Review: Stores reviews for both barbers and barbershops.
To handle the polymorphic relationship (a review can target either a barber or a barbershop), we have two nullable foreign keys: target_barber_id and target_barbershop_id. A CHECK constraint ensures that exactly one of these is set for each review.
parent_review_id allows for nested reviews (replies to reviews). A CHECK constraint ensures that only top-level reviews can have a rating, while replies cannot have a rating. This maintains the integrity of the review system and allows for threaded discussions in the review section.
*/
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

/*
To allow users to mark reviews as helpful, we have a join table Review_Helpful_Vote that links users to the reviews they've voted on. This allows us to easily count the number of helpful votes for each review and also prevents users from voting multiple times on the same review.
*/
CREATE TABLE IF NOT EXISTS Review_Helpful_Vote (
    review_id INT NOT NULL REFERENCES Review(review_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (review_id, user_id)
);


/*
Allows barbers or customers to follow barbers. This creates a many-to-many relationship between App_User (customers) and Barber. The UNIQUE constraint on (user_id, barber_id) ensures that either a customer or a barber can only follow a specific barber once.
This meets our system requirement that customers can follow barbers to see their latest posts, and also allows barbers to follow other barbers if they choose to.
*/
CREATE TABLE IF NOT EXISTS Follow (
    follow_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES App_User(user_id) ON DELETE CASCADE,
    barber_id INT NOT NULL REFERENCES Barber(barber_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE(user_id, barber_id)
);


/*
Intersection tables to link HaircutPhoto and Barber to Tag, allowing for many-to-many relationships. A haircut photo can have multiple tags (e.g., "fade", "short", "modern"), and a barber can also have multiple tags representing their specialties or styles they offer. The ON DELETE CASCADE ensures that if a photo or barber is deleted, the associated tag links are also removed, maintaining referential integrity.
*/
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


INSERT INTO Shift (barber_id, day_of_week, start_time, end_time)
VALUES
-- Barber 1 (Mon-Fri 9am-5pm)
(1, 0, '09:00', '17:00'),
(1, 1, '09:00', '17:00'),
(1, 2, '09:00', '17:00'),
(1, 3, '09:00', '17:00'),
(1, 4, '09:00', '17:00'),
-- Barber 2 (Tue-Sat 10am-6pm)
(2, 1, '10:00', '18:00'),
(2, 2, '10:00', '18:00'),
(2, 3, '10:00', '18:00'),
(2, 4, '10:00', '18:00'),
(2, 5, '10:00', '18:00'),
-- Barber 3 (Wed-Sun 11am-7pm)
(3, 2, '11:00', '19:00'),
(3, 3, '11:00', '19:00'),
(3, 4, '11:00', '19:00'),
(3, 5, '11:00', '19:00'),
(3, 6, '11:00', '19:00'),
-- Barber 4 (Mon-Fri 8am-4pm)
(4, 0, '08:00', '16:00'),
(4, 1, '08:00', '16:00'),
(4, 2, '08:00', '16:00'),
(4, 3, '08:00', '16:00'),
(4, 4, '08:00', '16:00'),
-- Barber 5 (Tue-Sat 12pm-8pm)
(5, 1, '12:00', '20:00'),
(5, 2, '12:00', '20:00'),
(5, 3, '12:00', '20:00'),
(5, 4, '12:00', '20:00'),
(5, 5, '12:00', '20:00'),
-- Barber 6 (Wed-Sun 9am-5pm)
(6, 2, '09:00', '17:00'),
(6, 3, '09:00', '17:00'),
(6, 4, '09:00', '17:00'),
(6, 5, '09:00', '17:00'),
(6, 6, '09:00', '17:00');


INSERT INTO ProfilePhoto (user_id, image_url, width_px, height_px)
VALUES 
(4, '/static/uploads/profiles/profile1.png', 1024, 1024),
(5, '/static/uploads/profiles/profile2.png', 1024, 1024),
(6, '/static/uploads/profiles/profile3.png', 1024, 1024),
(7, '/static/uploads/profiles/profile4.png', 1024, 1536),
(8, '/static/uploads/profiles/profile5.png', 1024, 1536),
(9, '/static/uploads/profiles/profile6.png', 1024, 1024);

Insert into tag (name)
VALUES
('fade'),
('skin fade'),
('taper'),
('clean shave'),
('quiff'),
('pompadour'),
('slick back'),
('beard'),
('beard trim'),
('line up'),
('buzz cut'),
('short'),
('edgy'),
('textured crop'),
('fringe'),
('modern'),
('classic'),
('undercut'),
('crop'),
('medium');


INSERT INTO HaircutPhoto (barber_id, image_url, width_px, height_px, is_post)
VALUES
(1, '/static/uploads/haircut_photos/image.png', 183, 275, TRUE),
(2, '/static/uploads/haircut_photos/image1.png', 225, 225, TRUE),
(3, '/static/uploads/haircut_photos/image2.png', 205, 246, TRUE),
(4, '/static/uploads/haircut_photos/image3.png', 225, 225, TRUE),
(5, '/static/uploads/haircut_photos/image4.png', 214, 235, FALSE),
(6, '/static/uploads/haircut_photos/image5.png', 201, 250, TRUE),
(1, '/static/uploads/haircut_photos/image6.png', 194, 259, TRUE),
(2, '/static/uploads/haircut_photos/image7.png', 168, 299, FALSE),
(3, '/static/uploads/haircut_photos/image8.png', 183, 275, TRUE),
(4, '/static/uploads/haircut_photos/image9.png', 206, 244, FALSE);


INSERT INTO HaircutPhoto_Tag (photo_id, tag_id)
VALUES
(1, 1), -- fade
(1, 2), -- skin fade
(1, 15), -- modern

(2, 3), -- taper
(2, 16), -- classic
(2, 4), -- clean shave

(3, 5), -- quiff
(3, 6), -- pompadour
(3, 7), -- slick back

(4, 8), -- beard
(4, 9), -- beard trim
(4, 10), -- line up

(5, 11), -- buzz cut
(5, 12), -- short
(5, 13), -- edgy

(6, 14), -- textured crop
(6, 15), -- fringe
(6, 16); -- modern


INSERT INTO Barber_Tag (barber_id, tag_id)
VaLUES
(1, 1), -- fade
(1, 2), -- skin fade
(1, 3), -- taper

(2, 3), -- taper
(2, 4), -- clean shave
(2, 10), -- line up

(3, 5), -- quiff
(3, 6), -- pompadour
(3, 7), -- slick back

(4, 8), -- beard
(4, 9), -- beard trim
(4, 10), -- line up

(5, 11), -- buzz cut
(5, 12), -- short
(5, 13), -- edgy

(6, 14), -- textured crop
(6, 15), -- fringe
(6, 16); -- modern


INSERT INTO Review (target_barber_id, user_id, text, rating)
VALUES
-- Reviews for Barber 1
(1, 1, 'Great fade, very clean!', 5),
(1, 2, 'Good service but the wait was long.', 4),
(1, 3, 'Not satisfied with the cut.', 2),
-- Reviews for Barber 2
(2, 1, 'Excellent taper, will come again!', 5),
(2, 2, 'Decent cut but could be better.', 3),
(2, 3, 'Loved the clean shave!', 5),
-- Reviews for Barber 3
(3, 1, 'Amazing quiff, very stylish!', 5),
(3, 2, 'Good pompadour but a bit pricey.', 4),
(3, 3, 'Slick back was perfect!', 5),
-- Reviews for Barber 4
(4, 1, 'Best beard trim Ive had!', 5),
(4, 2, 'Good line up but the fade was uneven.', 3),
(4, 3, 'Decent service but not great.', 3),
-- Reviews for Barber 5
(5, 1, 'Fantastic buzz cut, very edgy!', 5),
(5, 2, 'Short cut was good but not great.', 3),
(5, 3, 'Edgy style was perfect!', 5),
-- Reviews for Barber 6
(6, 1, 'Loved the textured crop!', 5),
(6, 2, 'Fringe was good but could be better.', 4),
(6, 3, 'Modern style was perfect!', 5);


INSERT INTO Review (target_barbershop_id, user_id, text, rating)
VALUES
-- Reviews for Barbershop 1
(1, 1, 'Great atmosphere and friendly staff!', 5),
(1, 2, 'Good service but a bit pricey.', 4),
(1, 3, 'Not satisfied with the overall experience.', 2),
-- Reviews for Barbershop 2
(2, 1, 'Excellent service and great cuts!', 5),
(2, 2, 'Decent experience but could be better.', 3),
(2, 3, 'Loved the vibe of the shop!', 5);

-- Barber replies to reviews 
INSERT INTO Review (parent_review_id, target_barber_id, user_id, text)
VALUES
-- Replies to reviews for Barber 1
(1, 1, 4, 'Thank you for your feedback!'),
(2, 1, 4, 'We apologize for the wait time. We are working on improving it.'),
(3, 1, 4, 'We are sorry to hear that. Please contact us so we can make it right.'),
-- Replies to reviews for Barber 2
(4, 2, 5, 'Thank you for your kind words!'),
(5, 2, 5, 'We appreciate your feedback and will strive to improve.'),
(6, 2, 5, 'Glad you loved the clean shave!'),
-- Replies to reviews for Barber 3
(7, 3, 6, 'Thank you for your positive feedback!'),
(8, 3, 6, 'We appreciate your honest review and will work on our pricing.'),
(9, 3, 6, 'Glad you loved the slick back!'),
-- Replies to reviews for Barber 4
(10, 4, 7, 'Thank you for your feedback!'),
(11, 4, 7, 'We apologize for the uneven fade. We will work on improving it.'),
(12, 4, 7, 'We appreciate your honest review and will strive to do better.'),
-- Replies to reviews for Barber 5
(13, 5, 8, 'Thank you for your positive feedback!'),
(14, 5, 8, 'We appreciate your honest review and will work on improving our short cuts.'),
(15, 5, 8, 'Glad you loved the edgy style!'),
-- Replies to reviews for Barber 6
(16, 6, 9, 'Thank you for your positive feedback!'),
(17, 6, 9, 'We appreciate your honest review and will work on improving our fringe styles.'),
(18, 6, 9, 'Glad you loved the modern style!');

-- Customers reply to reviews, some are usefull some are funny
INSERT INTO Review (parent_review_id, target_barber_id, user_id, text)
VALUES
(1, 1, 1, 'I agree, the fade was fantastic!'),
(2, 1, 2, 'I had a similar experience with the wait time.'),
(3, 1, 3, 'I had a great experience, maybe you just had an off day?'),
(4, 2, 1, 'The taper was amazing! I will definitely be back.'),
(5, 2, 2, 'I thought the cut was decent but not great.'),
(6, 2, 3, 'The clean shave was perfect! Highly recommend.'),
(7, 3, 1, 'The quiff was amazing! Very stylish.'),
(8, 3, 2, 'I thought the pompadour was good but a bit pricey.'),
(9, 3, 3, 'The slick back was perfect! I love it.'),
(10, 4, 1, 'The beard trim was fantastic! Best Ive had.'),
(11, 4, 2, 'I thought the line up was good but the fade was uneven.'),
(12, 4, 3, 'Decent service but not great overall.'),
(13, 5, 1, 'The buzz cut was fantastic! Very edgy and modern.'),
(14, 5, 2, 'I thought the short cut was good but not great.'),
(15, 5, 3, 'The edgy style was perfect! I love it.'),
(16, 6, 1, 'Loved the textured crop! Very modern and stylish.'),
(17, 6, 2, 'I thought the fringe was good but could be better.'),
(18, 6, 3, 'The modern style was perfect! Highly recommend!');


Insert into Follow (user_id, barber_id)
VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6);

INSERT INTO Review_Helpful_Vote (review_id, user_id)
VALUES
(1, 1),
(1, 2),
(4, 1),
(4, 3),
(7, 2),
(7, 3),
(10, 1),
(10, 2),
(13, 1),
(13, 3),
(16, 2),
(16, 3),
(2, 1),
(2, 3),
(5, 2),
(5, 3),
(8, 1),
(8, 3),
(11, 1),
(11, 3),
(14, 2),
(14, 3),
(17, 1),
(17, 3),
(3, 2),
(3, 3),
(6, 1),
(6, 2),
(9, 1),
(9, 2),
(12, 1),
(12, 2),
(15, 1),
(15, 2),
(18, 1),
(18, 2);


-- App_User
CREATE INDEX IF NOT EXISTS idx_app_user_role ON App_User(role);
CREATE INDEX IF NOT EXISTS idx_app_user_postcode ON App_User(postcode);

-- Barber
CREATE UNIQUE INDEX IF NOT EXISTS uq_barber_user_id ON Barber(user_id);
CREATE INDEX IF NOT EXISTS idx_barber_barbershop_id ON Barber(barbershop_id);

-- Barbershop
CREATE INDEX IF NOT EXISTS idx_barbershop_postcode ON Barbershop(postcode);

-- Shift
CREATE INDEX IF NOT EXISTS idx_shift_barber_id ON Shift(barber_id);
CREATE INDEX IF NOT EXISTS idx_shift_barber_day ON Shift(barber_id, day_of_week);

-- HaircutPhoto
CREATE INDEX IF NOT EXISTS idx_haircutphoto_barber_id ON HaircutPhoto(barber_id);
CREATE INDEX IF NOT EXISTS idx_haircutphoto_main_tag ON HaircutPhoto(main_tag);
CREATE INDEX IF NOT EXISTS idx_haircutphoto_is_post ON HaircutPhoto(is_post);
CREATE INDEX IF NOT EXISTS idx_haircutphoto_status ON HaircutPhoto(status);

-- ProfilePhoto
CREATE UNIQUE INDEX IF NOT EXISTS uq_profilephoto_user_id ON ProfilePhoto(user_id);

-- Review
CREATE INDEX IF NOT EXISTS idx_review_user_id ON Review(user_id);
CREATE INDEX IF NOT EXISTS idx_review_target_barber_id ON Review(target_barber_id);
CREATE INDEX IF NOT EXISTS idx_review_target_barbershop_id ON Review(target_barbershop_id);
CREATE INDEX IF NOT EXISTS idx_review_parent_review_id ON Review(parent_review_id);
CREATE INDEX IF NOT EXISTS idx_review_status ON Review(status);
CREATE INDEX IF NOT EXISTS idx_review_created_at ON Review(created_at);

-- Review_Helpful_Vote
CREATE INDEX IF NOT EXISTS idx_review_helpful_vote_user_id ON Review_Helpful_Vote(user_id);
CREATE INDEX IF NOT EXISTS idx_review_helpful_vote_review_id ON Review_Helpful_Vote(review_id);

-- Follow
CREATE INDEX IF NOT EXISTS idx_follow_user_id ON Follow(user_id);
CREATE INDEX IF NOT EXISTS idx_follow_barber_id ON Follow(barber_id);

-- Tag
CREATE UNIQUE INDEX IF NOT EXISTS uq_tag_name ON Tag(name);

-- Junction tables
CREATE INDEX IF NOT EXISTS idx_haircutphoto_tag_tag_id ON HaircutPhoto_Tag(tag_id);
CREATE INDEX IF NOT EXISTS idx_haircutphoto_tag_photo_id ON HaircutPhoto_Tag(photo_id);

CREATE INDEX IF NOT EXISTS idx_barber_tag_tag_id ON Barber_Tag(tag_id);
CREATE INDEX IF NOT EXISTS idx_barber_tag_barber_id ON Barber_Tag(barber_id);