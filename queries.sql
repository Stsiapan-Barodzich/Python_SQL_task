-- This file is just for show which queries was used 
USE python_json_schema;

CREATE TABLE rooms(
id INT PRIMARY KEY,
name VARCHAR(255) NOT NULL );

CREATE TABLE students(
id INT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
sex CHAR(1) NOT NULL,
birthday DATE NOT NULL,
room_id INT NOT NULL,
FOREIGN KEY(room_id) REFERENCES rooms(id));


CREATE INDEX idx_room_id ON students(room_id);
CREATE INDEX idx_birthday ON students(birthday);
CREATE INDEX idx_sex ON students(sex);

--  List of rooms and the number of students in each.
SELECT r.name, COUNT(s.id) as students_count
FROM rooms r
LEFT JOIN students s ON r.id = s.room_id
GROUP BY r.id;

-- Top 5 rooms with the smallest average student age
SELECT r.name,  AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) as average_age
FROM rooms r
LEFT JOIN students s ON r.id = s.room_id
GROUP BY r.id
ORDER BY average_age ASC
LIMIT 5;

-- Top 5 rooms with the largest age difference among students
SELECT r.name,  MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) as age_diff
FROM rooms r
LEFT JOIN students s ON r.id = s.room_id
GROUP BY r.id
ORDER BY age_diff ASC
LIMIT 5;

--  List of rooms where students of different sexes live together
SELECT r.name
FROM rooms r
JOIN students s ON r.id = s.room_id
GROUP BY r.id
HAVING COUNT(DISTINCT s.sex) > 1;
