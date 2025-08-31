# PinVibe API Documentation - User Registration

## Overview
This document describes the user registration system with email verification, unique validation, and password rules.

## Features
- ✅ Unique username and email validation
- ✅ Email verification with secure tokens
- ✅ Strong password validation rules
- ✅ Persian error messages
- ✅ Resend verification email functionality

## API Endpoints

### 1. User Registration
**POST** `/api/users/register/`

**Request Body:**
```json
{
    "username": "user123",
    "email": "user@example.com",
    "password": "StrongPass123!",
    "password_confirm": "StrongPass123!",
    "bio": "Optional bio text"
}
```

**Response (Success - 201):**
```json
{
    "message": "ثبت نام با موفقیت انجام شد. لطفاً ایمیل خود را برای تایید بررسی کنید.",
    "user_id": 1,
    "email": "user@example.com"
}
```

**Validation Rules:**
- **Username**: Only letters, numbers, and underscores. Must be unique.
- **Email**: Must be valid email format and unique.
- **Password**: Must meet all security requirements (see below).

### 2. User Login
**POST** `/api/users/login/`

**Request Body:**
```json
{
    "username": "user123",
    "password": "StrongPass123!"
}
```

**Response (Success - 200):**
```json
{
    "token": "your-auth-token",
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "bio": "Optional bio text",
        "avatar": null,
        "is_email_verified": true,
        "date_joined": "2024-01-01T00:00:00Z"
    }
}
```

**Response (Email not verified - 400):**
```json
{
    "error": "ایمیل شما تایید نشده است. لطفاً ایمیل خود را تایید کنید.",
    "needs_verification": true,
    "email": "user@example.com"
}
```

### 3. Email Verification
**GET** `/api/users/verify-email/{token}/`

**Response (Success - 200):**
```json
{
    "message": "ایمیل شما با موفقیت تایید شد.",
    "verified": true
}
```

**Response (Error - 400):**
```json
{
    "error": "کد تایید نامعتبر است.",
    "verified": false
}
```

### 4. Resend Verification Email
**POST** `/api/users/resend-verification/`

**Request Body:**
```json
{
    "email": "user@example.com"
}
```

**Response (Success - 200):**
```json
{
    "message": "ایمیل تایید دوباره ارسال شد."
}
```

### 5. User Profile
**GET** `/api/users/profile/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response (Success - 200):**
```json
{
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "bio": "Optional bio text",
    "avatar": null,
    "is_email_verified": true,
    "date_joined": "2024-01-01T00:00:00Z"
}
```

## Password Requirements

The password must meet the following criteria:

1. **Minimum Length**: At least 8 characters
2. **Uppercase Letters**: At least one uppercase letter (A-Z)
3. **Lowercase Letters**: At least one lowercase letter (a-z)
4. **Numbers**: At least one digit (0-9)
5. **Special Characters**: At least one special character (!@#$%^&*(),.?":{}|<>)
6. **No Consecutive Repeats**: No more than 2 consecutive identical characters
7. **No Common Patterns**: No common patterns like "123", "abc", "qwe", etc.

**Example Valid Passwords:**
- `TestPass123!`
- `MySecure@2024`
- `Complex#Password1`

**Example Invalid Passwords:**
- `password` (no uppercase, no numbers, no special chars)
- `Password1` (no special characters)
- `Test123` (too short)
- `aaa123!` (consecutive repeats)

## Email Verification Process

1. **Registration**: User registers with valid data
2. **Email Sent**: Verification email is automatically sent
3. **Token Generation**: Unique UUID token is generated
4. **Token Expiry**: Token expires after 1 hour
5. **Verification**: User clicks link or uses API endpoint
6. **Account Activation**: User account becomes active and verified

## Error Messages (Persian)

All error messages are provided in Persian:

- `این نام کاربری قبلاً استفاده شده است.` - Username already exists
- `این ایمیل قبلاً استفاده شده است.` - Email already exists
- `رمزهای عبور مطابقت ندارند.` - Passwords don't match
- `رمز عبور باید حداقل ۸ کاراکتر باشد.` - Password too short
- `ایمیل شما تایید نشده است.` - Email not verified
- `کد تایید منقضی شده است.` - Verification token expired

## Security Features

- **Token Security**: UUID tokens with 1-hour expiry
- **Password Hashing**: Passwords are securely hashed using Django's built-in hashing
- **Account Locking**: Unverified accounts cannot login
- **Rate Limiting**: Resend verification has 5-minute cooldown
- **Input Validation**: Comprehensive validation on all inputs

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install django-cors-headers django-email-verification
   ```

2. **Configure Email Settings:**
   ```python
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   ```

3. **Run Migrations:**
   ```bash
   python manage.py makemigrations users
   python manage.py migrate
   ```

4. **Test the API:**
   ```bash
   python manage.py test users.test_registration
   ```

## Example Usage with curl

```bash
# Register a new user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!"
  }'

# Login
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'

# Verify email (replace TOKEN with actual token)
curl -X GET http://localhost:8000/api/users/verify-email/TOKEN/

# Resend verification email
curl -X POST http://localhost:8000/api/users/resend-verification/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
``` 