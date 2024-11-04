# E-Academy Backend

E-Academy is an online platform for educational purposes. This repository contains the backend implementation of the E-Academy project using Django and Django REST Framework. It also includes OAuth authentication using Google and Twitter.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [OAuth Setup](#oauth-setup)
- [Author](#author)

## Features

- User registration and authentication
- Password reset functionality
- OAuth authentication with Google and Twitter
- JWT token-based authentication
- User profile management

## Requirements

- Python 3.12
- Django 4.x
- Django REST Framework
- django-allauth
- requests
- requests-oauthlib

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/happychuks/eacademy_auth.git
   cd eacademy_auth
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies**:

    `pip3 install -r requirements.txt`

4. **Run migrations**:

    ```bash 
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

## Configuration

1. **Environmental Variables**:
    Create a `.env` file in the root directory and add the following environment variables:

    ```txt
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'example@gmail.com'
    EMAIL_HOST_PASSWORD = '<password>'

    # Oauth 
    GOOGLE_CLIENT_ID=<CLIENT_ID>
    GOOGLE_CLIENT_SECRET=<CLIENT_SECRET>
    TWITTER_API_KEY =<API_KEY>
    TWITTER_API_SECRET_KEY =<API_SECRET_KEY>
    ```


2. **Update `settings.py`**:
    Replace with your frontend URL.

    ```python
    FRONTEND_URL='http://localhost:3000'
    ```

## Running the Project

1. **Start the development server**:

    `python3 manage.py runserver`

2. **Access the application**:

    Open your web browser and navigate to http://localhost:8000.

## API Endpoints

- User Registration: POST /api/signup/
- User Login: POST /api/login/
- Token Refresh: POST /api/token/refresh/
- User Profile: GET /api/user/
- Password Reset Request: POST /api/forgot-password/
- Password Reset: POST /api/reset-password/
- Google OAuth Login: GET /accounts/google/login/
- Twitter OAuth Login: GET /accounts/twitter/login/

## OAuth Setup

1. **Google OAuth**:

- Go to the [Google Developers Console](https://console.developers.google.com/).
- Create a new project and enable the "Google+ API".
- Create OAuth 2.0 credentials and set the authorized redirect URIs to `http://localhost:8000/accounts/google/login/callback/`.

2. **Twitter OAuth**:

- Go to the [Twitter Developer Portal](https://developer.twitter.com/).
- Create a new app and set the callback URL to `http://localhost:8000/accounts/twitter/login/callback/`.

## Author

- [Happy Felix Chukwuma](https://codewithfelix.vercel.app/)

Happy Coding