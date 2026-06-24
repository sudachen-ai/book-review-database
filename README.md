# Book Review Database Management System

## Overview

This project is a Python and MySQL command-line database application for managing books, authors, genres, reading statuses, and book reviews.

The goal of this project was to practice relational database design, SQL operations, stored procedures, triggers, and Python database connectivity using PyMySQL.

## Tech Stack

- Python
- MySQL
- PyMySQL
- SQL
- Stored Procedures
- Triggers
- Git / GitHub

## Features

- List all books
- View book details
- Search books by keyword
- Search books by author
- List all reviews
- View reviews for a specific book
- Add a new book
- Add a book using genre and status names
- Add a review
- Update a book's reading status
- Delete a book
- View reference lists for genres, statuses, and authors

## Database Design

The database stores information about:

- Books
- Authors
- Genres
- Reading statuses
- Reviews

The design uses relational database concepts including:

- Primary keys
- Foreign keys
- Many-to-many relationships between books and authors
- Stored procedures for reusable database operations
- Triggers for data integrity and automated database behavior

## Application Workflow

The application provides a command-line menu that allows users to perform CRUD operations:

- Create: add books and reviews
- Read: search and view books, authors, genres, statuses, and reviews
- Update: update reading status
- Delete: delete a book record

The Python program connects to the MySQL database using PyMySQL and calls stored procedures to perform database operations.

## Error Handling and Validation

The application includes basic input validation and error handling, including:

- Checking whether required fields are empty
- Validating numeric input for IDs and ratings
- Restricting ratings to a valid range
- Using commits and rollbacks for database transactions
- Handling database errors from MySQL operations

## Support / QA Relevance

This project is relevant to application support, technical support, QA, and database support roles because it demonstrates:

- Working with a database-backed application
- Understanding CRUD workflows
- Querying and validating relational data
- Handling user input and database errors
- Troubleshooting database-related issues
- Documenting application behavior clearly

## What I Learned

Through this project, I practiced:

- Designing relational database tables
- Writing SQL queries and stored procedures
- Connecting Python applications to MySQL
- Managing database transactions
- Building command-line application workflows
- Thinking about data validation and application reliability# book-review-database
Python and MySQL command-line application for managing books, authors, genres, reading status, and reviews.
