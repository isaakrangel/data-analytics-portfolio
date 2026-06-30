-- CREATE DATABASE CompanySITS;
-- USE CompanySITS;

-- STRONG ENTITIES
CREATE TABLE Users (
	UserID INT,
	Fname VARCHAR(50) NOT NULL,
	Lname VARCHAR(50) NOT NULL,
	EmailID VARCHAR(100) NOT NULL UNIQUE,
    
    PRIMARY KEY (UserID)
);

CREATE TABLE Student(
	StudentID INT,
	Program VARCHAR(100) NOT NULL,
     
	PRIMARY KEY (StudentID),
	FOREIGN KEY (StudentID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE Teacher (
	TeacherID INT,
	Department VARCHAR(100) NOT NULL,
    
	PRIMARY KEY (TeacherID),
	FOREIGN KEY (TeacherID) REFERENCES Users(UserID)
);
-- Multi-valued attribute from Teacher
CREATE TABLE Teacher_Subjects(
	TeacherID INT,
	Subject_Name VARCHAR(100) NOT NULL,
    
    
	PRIMARY KEY (TeacherID,Subject_Name),
	FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID) ON DELETE CASCADE
);

CREATE TABLE Quiz (
	QuizID INT,
    Created_By INT NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Descp VARCHAR(200),
    Total_Marks FLOAT NOT NULL,
    Created_Date DATETIME,
    
    
    PRIMARY KEY (QuizID),
    FOREIGN KEY (Created_By) REFERENCES Teacher(TeacherID) ON DELETE CASCADE 
);

CREATE TABLE Course(
	CourseID INT,
    Course_Name VARCHAR(250) NOT NULL,
	    
	PRIMARY KEY (CourseID)
);

CREATE TABLE Question(
	QuestionID INT,
    CourseID INT NOT NULL,
    Content VARCHAR(250) NOT NULL,
    Feedback VARCHAR(250),
    
	PRIMARY KEY (QuestionID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
);

-- WEAK ENTITIES
CREATE TABLE Topic(
	CourseID INT,
    TopicID INT,
    Topic_Name VARCHAR(100),
        
	PRIMARY KEY (TopicID,CourseID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
);

CREATE TABLE Question_Options
(
    QuestionID INT,
    OptionID INT,
    Content VARCHAR(250) NOT NULL,
    isCorrect TINYINT NOT NULL,

    PRIMARY KEY (QuestionID,OptionID),
    FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID) ON DELETE CASCADE
);

CREATE TABLE Attempts (
	AttemptID INT,
    QuizID INT,
    StudentID INT,
    Attempt_Date DATETIME NOT NULL,
    Marks_Earned FLOAT NOT NULL,   
    
	PRIMARY KEY (AttemptID,QuizID,StudentID),
    FOREIGN KEY (QuizID) REFERENCES Quiz(QuizID) ON DELETE CASCADE,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE -- or Users(UserID)
);
CREATE TABLE Attempt_Answer
(
    AttemptID INT,
    QuizID INT,
    StudentID INT,
    OptionID INT,
    QuestionID INT,

    PRIMARY KEY (AttemptID,QuizID,StudentID,QuestionID,OptionID),
    FOREIGN KEY (AttemptID,QuizID,StudentID) REFERENCES Attempts(AttemptID,QuizID,StudentID) ON DELETE CASCADE,
    -- FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE,
    -- or Users(UserID)
    -- FOREIGN KEY (QuizID) REFERENCES Quiz(QuizID) ON DELETE CASCADE,
    FOREIGN KEY (QuestionID,OptionID) REFERENCES Question_Options(QuestionID,OptionID) ON DELETE CASCADE
    -- FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID) ON DELETE CASCADE
);

-- Relationship Relations
CREATE TABLE Quiz_Contains_Question (
	QuestionID INT,
    QuizID INT,
    
    PRIMARY KEY (QuestionID,QuizID),
    FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID) ON DELETE CASCADE,
    FOREIGN KEY (QuizID) REFERENCES Quiz(QuizID) ON DELETE CASCADE
);

CREATE TABLE Topic_Contains_Subtopic
(
    CourseID INT,
    TopicID INT,
    Sub_TopicID INT,

    PRIMARY KEY (Sub_TopicID,CourseID),
    FOREIGN KEY (Sub_TopicID,CourseID) REFERENCES Topic(TopicID,CourseID),
    FOREIGN KEY (TopicID,CourseID) REFERENCES Topic(TopicID,CourseID) ON DELETE CASCADE
);