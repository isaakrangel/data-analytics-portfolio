# Quiz Management System Database Design (SQL Project)

## Objective
Design and implement a relational database system for a Quiz Management platform that allows teachers to create quizzes and students to attempt them multiple times, while tracking performance and responses.

## Project Overview
The system is designed to support the creation, management, and evaluation of multiple-choice quizzes. It models the relationships between teachers, students, quizzes, questions, options, and course categorization.

## Key Features
- Teachers can create multiple quizzes
- Each quiz contains one or more multiple-choice questions
- Students can attempt quizzes multiple times
- Each attempt records selected answers and total score
- Questions are categorized by course, topic, and sub-topic
- Each question has one correct answer and multiple options

## Database Design Assumptions
- A teacher can create multiple quizzes (1:N)
- A student can attempt multiple quizzes multiple times (M:N)
- A quiz contains multiple questions, and questions can belong to multiple quizzes (M:N)
- Each question has one correct answer and multiple incorrect options
- Options can be shared across multiple questions
- Questions can belong to one or multiple courses (M:N)

## Entities Modeled
- Teachers
- Students
- Quizzes
- Questions
- Options
- Courses

## Relationships (Cardinality Summary)
- Teacher → Quiz (1:N)
- Student → Quiz (M:N)
- Quiz → Questions (M:N)
- Question → Options (1:M, with correct/incorrect classification)
- Question → Courses (M:N)

## Skills Demonstrated
- Relational database design (ER modeling)
- Normalization principles
- Cardinality and relationship mapping
- SQL database structuring
- Data modeling for real-world systems

## Conclusion
This project demonstrates the design of a scalable relational database system capable of managing quizzes, user interactions, and performance tracking, while maintaining proper normalization and relationship integrity.
