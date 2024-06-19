-- Command to drop tables
DROP TABLE languages;
DROP TABLE meta;
DROP TABLE payment_gateways;
DROP TABLE social_media;
DROP TABLE tech_stack;
DROP TABLE websites;




-- Creatign tables
CREATE TABLE websites (
    website_id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(255) NOT NULL
);
CREATE TABLE social_media (
    social_media_id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT NOT NULL,
    platform VARCHAR(50) NOT NULL,
    link VARCHAR(255) NOT NULL
);
CREATE TABLE tech_stack (
    tech_stack_id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT NOT NULL,
    technology VARCHAR(50) NOT NULL
);
CREATE TABLE meta (
    meta_id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT
);
CREATE TABLE payment_gateways (
    payment_gateways_id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT NOT NULL,
    gateway VARCHAR(50) NOT NULL
);
CREATE TABLE languages (
    language_id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT NOT NULL,
    language VARCHAR(50) NOT NULL
);

-- Adding Foreign Constraints
-- Add foreign key constraint to social_media table
ALTER TABLE social_media
ADD CONSTRAINT FK_social_media_website_id
FOREIGN KEY (website_id) REFERENCES websites(website_id);

-- Add foreign key constraint to tech_stack table
ALTER TABLE tech_stack
ADD CONSTRAINT FK_tech_stack_website_id
FOREIGN KEY (website_id) REFERENCES websites(website_id);

-- Add foreign key constraint to meta table
ALTER TABLE meta
ADD CONSTRAINT FK_meta_website_id
FOREIGN KEY (website_id) REFERENCES websites(website_id);

-- Add foreign key constraint to payment_gateways table
ALTER TABLE payment_gateways
ADD CONSTRAINT FK_payment_gateways_website_id
FOREIGN KEY (website_id) REFERENCES websites(website_id);

-- Add foreign key constraint to languages table
ALTER TABLE languages
ADD CONSTRAINT FK_languages_website_id
FOREIGN KEY (website_id) REFERENCES websites(website_id);


-- Retrieve Final Data
SELECT 
    w.website_id,
    w.url,
    w.category,
    l.language,
    m.title,
    m.description,
    ts.technology,
    pg.gateway,
    sm.platform,
    sm.link
FROM 
    websites w
LEFT JOIN social_media sm ON w.website_id = sm.website_id
LEFT JOIN tech_stack ts ON w.website_id = ts.website_id
LEFT JOIN meta m ON w.website_id = m.website_id
LEFT JOIN payment_gateways pg ON w.website_id = pg.website_id
LEFT JOIN languages l ON w.website_id = l.website_id;