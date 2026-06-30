-- USE CompanySITS;

-- Department(Number, Name)
INSERT INTO Users (UserID,Fname,Lname,EmailID) VALUES
(1,'Liam','Anderson','liam.anderson@test.com'),  -- students
(2,'Noah','Martinez','noah.martinez@test.com'),
(3,'Oliver','Garcia','oliver.garcia@test.com'),
(4,'Elijah','Rodriguez','elijah.rodriguez@test.com'),
(5,'James','Hernandez','james.hernandez@test.com'),
(6,'William','Lopez','william.lopez@test.com'),
(7,'Benjamin','Gonzalez','benjamin.gonzalez@test.com'),
(8,'Lucas','Wilson','lucas.wilson@test.com'),
(9,'Henry','Anderson','henry.anderson@test.com'),
(10,'Alexander','Thomas','alexander.thomas@test.com'),
(11,'Mason','Taylor','mason.taylor@test.com'),
(12,'Michael','Moore','michael.moore@test.com'),
(13,'Ethan','Jackson','ethan.jackson@test.com'),
(14,'Daniel','Martin','daniel.martin@test.com'),
(15,'Jacob','Lee','jacob.lee@test.com'),
(16,'Logan','Perez','logan.perez@test.com'),
(17,'Jackson','Thompson','jackson.thompson@test.com'),
(18,'Levi','White','levi.white@test.com'),
(19,'Sebastian','Harris','sebastian.harris@test.com'),
(20,'Mateo','Sanchez','mateo.sanchez@test.com'),
(21,'Jack','Clark','jack.clark@test.com'),
(22,'Owen','Ramirez','owen.ramirez@test.com'),
(23,'Theodore','Lewis','theodore.lewis@test.com'),
(24,'Aiden','Robinson','aiden.robinson@test.com'),
(25,'Samuel','Walker','samuel.walker@test.com'),
(26,'Joseph','Young','joseph.young@test.com'),
(27,'John','Allen','john.allen@test.com'),
(28,'David','King','david.king@test.com'),
(29,'Wyatt','Wright','wyatt.wright@test.com'),
(30,'Matthew','Scott','matthew.scott@test.com'),
-- tecahers
(31,'Sophia','Green','sophia.green@test.com'),
(32,'Isabella','Adams','isabella.adams@test.com'),
(33,'Mia','Baker','mia.baker@test.com'),
(34,'Charlotte','Nelson','charlotte.nelson@test.com'),
(35,'Amelia','Carter','amelia.carter@test.com'),
(36,'Harper','Mitchell','harper.mitchell@test.com'),
(37,'Evelyn','Perez','evelyn.perez@test.com'),
(38,'Abigail','Roberts','abigail.roberts@test.com'),
(39,'Emily','Turner','emily.turner@test.com'),
(40,'Elizabeth','Phillips','elizabeth.phillips@test.com');


INSERT INTO Student(StudentID,Program) VALUES
(1,'Computer Science'),
(2,'Computer Science'),
(3,'Software Engineering'),
(4,'Software Engineering'),
(5,'Information Technology'),
(6,'Data Science'),
(7,'Computer Science'),
(8,'Computer Science'),
(9,'Software Engineering'),
(10,'Statistics'),
(11,'Information Technology'),
(12,'Advanced Mathematics'),
(13,'Computer Science'),
(14,'Computer Science'),
(15,'Software Engineering'),
(16,'Software Engineering'),
(17,'Information Technology'),
(18,'Information Technology'),
(19,'Computer Science'),
(20,'Computer Science'),
(21,'Software Engineering'),
(22,'Software Engineering'),
(23,'Information Technology'),
(24,'Data Analitycs'),
(25,'Computer Science'),
(26,'Computer Science'),
(27,'Software Engineering'),
(28,'Software Engineering'),
(29,'Information Technology'),
(30,'Advanced Mathematics');

INSERT INTO Teacher(TeacherID,Department) VALUES
(31,'Engineering'),
(32,'Engineering'),
(33,'Mathematics'),
(34,'Physics'),
(35,'Engineering'),
(36,'Computer Science'),
(37,'Mathematics'),
(38,'Software Engineering'),
(39,'Mathematics'),
(40,'Cybersecurity');

INSERT INTO  Teacher_Subjects(TeacherID,Subject_Name) VALUES
-- 31
(31,'Fundamentals of Engineering'),
(31,'Databases'),
(31,'Programming'),
-- 32
(32,'Programming'),
(32,'Software Development'),
-- 33
(33,'Algebra'),
(33,'Advanced Mathematics'),
-- 34
(34,'Physics'),
(34,'Mechanics'),
-- 35
(35,'Networks'),
(35,'Cybersecurity'),
(35,'Fundamentals of Engineering'),
-- 36
(36,'Artificial Intelligence'),
(36,'Machine Learning'),
-- 37
(37,'Statistics'),
(37,'Data Analytics'),
(37,'Data Science'),
-- 38
(38,'Software Design'),
(38,'Software Engineering'),
-- 39
(39,'Calculus'),
(39,'Advanced Mathematics'),
-- 40
(40,'Cybersecurity'),
(40,'Network Security');

INSERT INTO Course(CourseID,Course_Name) VALUES
(1,'Fundamentals of Engineering'),
(2,'Databases'),
(3,'Programming'),
(4,'Software Development'),
(5,'Algebra'),
(6,'Advanced Mathematics'),
(7,'Physics'),
(8,'Mechanics'),
(9,'Networks'),
(10,'Cybersecurity'),
(11,'Artificial Intelligence'),
(12,'Machine Learning'),
(13,'Statistics'),
(14,'Data Analytics'),
(15,'Data Science'),
(16,'Software Design'),
(17,'Software Engineering'),
(18,'Calculus'),
(19,'Network Security');

INSERT INTO Quiz(QuizID,Created_By,Title,Descp,Total_Marks,Created_Date) VALUES
-- Profesor 31
(1,31,'Databases Quiz 1','Intro to databases',100,NOW()),-- NOW() works here but in MS SQL the equivalent is GETDATE()
(2,31,'Databases Quiz 2','Advanced databases',100,NOW()),
-- Profesor 32
(3,32,'Programming Quiz 1','Intro programming',100,NOW()),
(4,32,'Programming Quiz 2','Programming concepts',100,NOW()),
-- Profesor 33
(5,33,'Algebra Quiz 1','Basic algebra',100,NOW()),
(6,33,'Algebra Quiz 2','Advanced algebra',100,NOW()),
-- Profesor 34
(7,34,'Physics Quiz 1','Mechanics basics',100,NOW()),
(8,34,'Physics Quiz 2','Dynamics',100,NOW()),
-- Profesor 35
(9,35,'Networking Quiz 1','Networking concepts',100,NOW()),
(10,35,'Networking Quiz 2','Network security',100,NOW()),
-- Profesor 36
(11,36,'AI Quiz 1','Intro AI',100,NOW()),
(12,36,'AI Quiz 2','Machine learning',100,NOW()),
-- Profesor 37
(13,37,'Statistics Quiz 1','Descriptive statistics',100,NOW()),
(14,37,'Statistics Quiz 2','Inferential statistics',100,NOW()),
-- Profesor 38
(15,38,'Software Design Quiz 1','Design patterns',100,NOW()),
(16,38,'Software Design Quiz 2','Software architecture',100,NOW()),
-- Profesor 39
(17,39,'Calculus Quiz 1','Limits & derivatives',100,NOW()),
(18,39,'Calculus Quiz 2','Integrals',100,NOW()),
-- Profesor 40
(19,40,'Cybersecurity Quiz 1','Intro to security',100,NOW()),
(20,40,'Cybersecurity Quiz 2','Network attacks',100,NOW());

INSERT INTO Question(QuestionID,CourseID,Content,Feedback) VALUES
-- Quiz 1 → Curso 2 (Databases)
(1,2,'What is a database?','A system to store structured data'),
(2,2,'What is SQL used for?','Querying and managing data'),
(3,2,'Primary key uniquely identifies what?','A record in a table'),
(4,2,'Which is a type of database?','Relational, NoSQL, etc.'),
-- Quiz 2 → Curso 2 (Databases advanced)
(5,2,'What is a foreign key?','It links tables together'),
(6,2,'What is normalization?','Organizing data efficiently'),
(7,2,'Which SQL command deletes data?','DELETE'),
(8,2,'What is indexing?','Speeds up queries'),
-- Quiz 3 → Curso 3 (Programming basics)
(9,3,'What is a variable?','Stores data'),
(10,3,'Which is a loop structure?','for, while, do-while'),
(11,3,'What is a function?','Reusable code block'),
(12,3,'What is a conditional?','if/else statement'),
-- Quiz 4 → Curso 3 (Programming concepts)
(13,3,'What is OOP?','Object Oriented Programming'),
(14,3,'What is inheritance?','A class derives from another'),
(15,3,'What is encapsulation?','Restrict access to internals'),
(16,3,'What is polymorphism?','Same interface, different behavior');

INSERT INTO Question_Options(QuestionID,OptionID,Content,isCorrect)VALUES
-- Q1
(1,1,'A system to store structured data',1),
(1,2,'A programming language',0),
(1,3,'A network protocol',0),
(1,4,'A hardware device',0),
-- Q2
(2,1,'Querying and managing data',1),
(2,2,'Drawing diagrams',0),
(2,3,'Sending emails',0),
(2,4,'Operating system commands',0),
-- Q3
(3,1,'A record in a table',1),
(3,2,'A database itself',0),
(3,3,'A column',0),
(3,4,'A server',0),
-- Q4
(4,1,'Relational, NoSQL, etc.',1),
(4,2,'Photoshop',0),
(4,3,'Word processor',0),
(4,4,'Network cable',0),
-- Q5
(5,1,'It links tables together',1),
(5,2,'Deletes files',0),
(5,3,'Stores images',0),
(5,4,'Formats text',0);

INSERT INTO Quiz_Contains_Question(QuestionID,QuizID) VALUES
(1,1),(2,1),(3,1),(4,1),
(5,2),(6,2),(7,2),(8,2),
(9,3),(10,3),(11,3),(12,3),
(13,4),(14,4),(15,4),(16,4);

INSERT INTO Attempts(AttemptID,QuizID,StudentID,Attempt_Date,Marks_Earned) VALUES
(1,1,1,NOW(),85), -- NOW() works here but in MS SQL the equivalent is GETDATE()
(2,1,2,NOW(),90),
(3,2,1,NOW(),80);

-- Attempt 1 (StudentID 1, QuizID 1)
INSERT INTO Attempt_Answer(AttemptID,QuizID,StudentID,QuestionID,OptionID) VALUES
(1, 1, 1, 1, 1), -- Q1 correct
(1, 1, 1, 2, 1), -- Q2 correct
(1, 1, 1, 3, 1), -- Q3 correct
(1, 1, 1, 4, 1); -- Q4 correct
-- Attempt 2 (StudentID 2, QuizID 1)
INSERT INTO Attempt_Answer (AttemptID, QuizID, StudentID, QuestionID, OptionID) VALUES
(2, 1, 2, 1, 1),
(2, 1, 2, 2, 1),
(2, 1, 2, 3, 1),
(2, 1, 2, 4, 1);

-- Attempt 3 (StudentID 1, QuizID 2)
INSERT INTO Attempt_Answer (AttemptID, QuizID, StudentID, QuestionID, OptionID) VALUES
(3, 2, 1, 1, 1),
(3, 2, 1, 2, 1),
(3, 2, 1, 3, 1),
(3, 2, 1, 4, 1);

-- Topics
INSERT INTO Topic(CourseID,TopicID,Topic_Name) VALUES
-- Databases (CourseID 2)
(2,1,'Database Basics'),
(2,2,'SQL Queries'),
(2,3,'Normalization'),
-- Programming (CourseID 3)
(3,1,'Variables and Data Types'),
(3,2,'Loops and Conditionals'),
(3,3,'Functions and OOP'),
-- Algebra (CourseID 5)
(5,1,'Equations'),
(5,2,'Polynomials'),
(5,3,'Factorization'),
-- Advanced Mathematics (CourseID 6)
(6,1,'Matrices'),
(6,2,'Vectors'),
-- Physics (CourseID 7)
(7,1,'Mechanics'),
(7,2,'Dynamics'),
-- Networking (CourseID 9)
(9,1,'Network Basics'),
(9,2,'Network Security'),
-- Artificial Intelligence (CourseID 11)
(11,1,'AI Concepts'),
(11,2,'Machine Learning'),
-- Statistics (CourseID 13)
(13,1,'Descriptive Statistics'),
(13,2,'Inferential Statistics'),
-- Software Design (CourseID 16)
(16,1,'Design Patterns'),
(16,2,'Architecture Principles'),
-- Cybersecurity (CourseID 10)
(10,1,'Security Basics'),
(10,2,'Network Threats');

-- Subtopics (topics relations)
INSERT INTO Topic_Contains_Subtopic(CourseID,TopicID,Sub_TopicID) VALUES
-- Databases
(2,1,2), -- Database Basics → SQL Queries
(2,1,3), -- Database Basics → Normalization
-- Programming
(3,1,2), -- Variables and Data Types → Loops and Conditionals
(3,1,3), -- Variables and Data Types → Functions and OOP
-- Algebra
(5,1,2), -- Equations → Polynomials
(5,2,3), -- Polynomials → Factorization
-- Advanced Mathematics
(6,1,2), -- Matrices → Vectors
-- Physics
(7,1,2), -- Mechanics → Dynamics
-- Networking
(9,1,2), -- Network Basics → Network Security
-- AI
(11,1,2), -- AI Concepts → Machine Learning
-- Statistics
(13,1,2), -- Descriptive → Inferential
-- Software Design
(16,1,2), -- Design Patterns → Architecture Principles
-- Cybersecurity
(10,1,2); -- Security Basics → Network Threats














