USE CompanySITS;

-- Show the First and last name  and the average grade of the students that made attempts
SELECT Users.Fname, Users.Lname, AVG(Attempts.Marks_Earned) AS Avg_Marks
FROM Users
INNER JOIN Student ON Users.UserID = Student.StudentID
INNER JOIN Attempts ON Student.StudentID = Attempts.StudentID
GROUP BY Users.Fname, Users.Lname;

-- Show the data of the teachers that had created a quiz
SELECT Users.*, Teacher.Department
FROM Users
JOIN Teacher ON  Users.UserID = Teacher.TeacherID
WHERE UserID IN (SELECT Created_By FROM Quiz);

-- Update or modify the grade of the student attempt in a quiz
UPDATE Attempts
SET Marks_Earned = 85
WHERE AttemptID = 1 AND QuizID = 1 AND StudentID = 1;
  
-- Delete a specific attempt of a student
DELETE FROM Attempts
WHERE AttemptID = 1 AND QuizID = 1 AND StudentID = 1;

-- Show the attempts info on a specific date
SELECT *
FROM Attempts
WHERE DATE(Attempt_Date) = '2026-03-29';

-- Show max attempts done by a certain student
SELECT StudentID, COUNT(*) AS Total_Attempts
FROM Attempts
WHERE StudentID = 1
GROUP BY StudentID;

-- Right option in the question
SELECT QuestionID, OptionID, Content
FROM Question_Options
WHERE QuestionID = 5 AND isCorrect = 1;

-- Update the isCorrect option
UPDATE Question_Options -- First set all options as 0
SET isCorrect = 0
WHERE QuestionID = 5;

UPDATE Question_Options -- then set the specific option to 1
SET isCorrect = 1
WHERE QuestionID = 5 AND OptionID = 2;
  
-- Questions in a quiz
SELECT Question.QuestionID, Question.Content
FROM Quiz_Contains_Question
INNER JOIN Question ON Quiz_Contains_Question.QuestionID = Question.QuestionID
WHERE Quiz_Contains_Question.QuizID = 1;

-- Options in a question
SELECT QuestionID, OptionID, Content, isCorrect
FROM Question_Options
WHERE QuestionID = 5;

-- Delete a question from a quiz
DELETE FROM Quiz_Contains_Question
WHERE QuizID = 1 AND QuestionID = 5;

-- creating a view for student results in the attempts for quices and the using it
CREATE VIEW Student_Results AS
SELECT Users.Fname, Users.Lname, Quiz.Title, Attempts.Marks_Earned
FROM Users
INNER JOIN Student ON Users.UserID = Student.StudentID
INNER JOIN Attempts ON Student.StudentID = Attempts.StudentID
INNER JOIN Quiz ON Attempts.QuizID = Quiz.QuizID;

SELECT * 
FROM Student_Results;

-- COUNT of all question in a quiz
SELECT QuizID, COUNT(QuestionID) AS Total_Questions
FROM Quiz_Contains_Question
WHERE QuizID = 1
GROUP BY QuizID;

-- Average of all the attempts made by students
SELECT AVG(Marks_Earned) AS Average_Marks
FROM Attempts;

-- Get all students who have attempted a certain quiz
SELECT Users.Fname, Users.Lname, Student.StudentID
FROM Attempts
INNER JOIN Student ON Attempts.StudentID = Student.StudentID
INNER JOIN Users ON Student.StudentID = Users.UserID
WHERE Attempts.QuizID = 1;

-- DISTINCT/COUNT of all quizzes made by a student
SELECT StudentID, COUNT(DISTINCT QuizID) AS Total_Quizzes_Attempted
FROM Attempts
WHERE StudentID = 1
GROUP BY StudentID;

-- Student with more/less than specific grade
SELECT Users.Fname, Users.Lname, Attempts.Marks_Earned
FROM Attempts
INNER JOIN Student ON Attempts.StudentID = Student.StudentID
INNER JOIN Users ON Student.StudentID = Users.UserID
WHERE Attempts.Marks_Earned > 80;

-- Student with max grade
SELECT Users.Fname, Users.Lname, Attempts.Marks_Earned
FROM Attempts
INNER JOIN Student ON Attempts.StudentID = Student.StudentID
INNER JOIN Users ON Student.StudentID = Users.UserID
WHERE Attempts.Marks_Earned = (SELECT MAX(Marks_Earned)FROM Attempts);

-- Quizzes by attempted by student
SELECT Users.Fname, Users.Lname, Quiz.Title
FROM Attempts
INNER JOIN Student ON Attempts.StudentID = Student.StudentID
INNER JOIN Users ON Student.StudentID = Users.UserID
INNER JOIN Quiz ON Attempts.QuizID = Quiz.QuizID
WHERE Attempts.StudentID = 1;

-- Number of questions created by a teacher
SELECT TeacherID, COUNT(DISTINCT Question.QuestionID) AS Total_Questions
FROM Quiz
INNER JOIN Teacher ON Teacher.TeacherID = Quiz.Created_By
INNER JOIN Quiz_Contains_Question ON Quiz.QuizID = Quiz_Contains_Question.QuizID
INNER JOIN Question ON Quiz_Contains_Question.QuestionID = Question.QuestionID
WHERE Quiz.Created_By = 31
GROUP BY TeacherID;

-- Quizzes by created by teacher
SELECT Users.Fname, Users.Lname, Quiz.Title
FROM Quiz
INNER JOIN Teacher ON Quiz.Created_By = Teacher.TeacherID
INNER JOIN Users ON Teacher.TeacherID = Users.UserID
WHERE Teacher.TeacherID = 33;

