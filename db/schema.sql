-- drop table if re-running the script during testing
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

-- Inserting the initial records
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('Nouri', 'Dawalibi', 'john.doe@example.com', '2023-09-01'),
('Jack', 'Daniels', 'jackdaniel@example.com', '2024-03-01'),
('Hooman', 'smth', 'hooman.smth@example.com', '2020-01-01');

