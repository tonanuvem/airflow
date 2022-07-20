USE usuarios;

CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255),
  `created_at` timestamp,
  `address` varchar(255)
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

INSERT INTO users (full_name,created_at, address) VALUES("Indiana Jones",NOW(),"Adventures Avenue");
INSERT INTO users (full_name,created_at, address) VALUES("Jack Sparrow",NOW(),"Master Ship Square");
INSERT INTO users (full_name,created_at, address) VALUES("John Snow",NOW(),"Kinds Landing Westeros");
