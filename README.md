# InsuranceWebApp project for ITNetwork

This project a Flask-based web application that allows users to create user accounts and admin account which can manage user information, and handle insurance-related tasks. The system differentiates between normal users and admin users, granting admin users additional capabilities. It automatically creates a database (if it's not already created) with User and Insurance tables and their relational database.

# Prerequisities

Python 3.11
and see the requirements.txt for additional libraries

# Getting started
- after installing all needed packages, just run main.py
- it automatically creates database
- than it's needed to first creat Admin user

# Usage
- Create a user account or log in if you're already registered.
- Admin users can manage user accounts, as well as create and manage insurance policies and assign them to users.
Normal users can view their account information and insurance details.

# Features
- User account management (registration, login)
- Role-based access control (admin vs. normal user)
- Admin user management (create, modify, delete)
- Insurance policy management (create, modify, delete)
- Data validation and security measures(hashed passwords)
- User-friendly web interface

# Future enhancements

While the current version of the project is functional, it's still under develop and there are several features and improvements I plan to implement in the future. 

These include:

- User Profile Customization: Allow users to customize their profiles with avatars, personal information, and more.
- Enhanced Admin and User dashboard -> Improve the admin dashboard with advanced analytics and user management features.
- More web responsive features, make app much more user friendly with nicer web environment


