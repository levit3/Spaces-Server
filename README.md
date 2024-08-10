# Spaces

# Spaces Server

Spaces Server is a backend server for managing spaces, users, bookings, reviews, and payments. It is built using Flask and Flask-RESTful, with integrations for Cloudinary, PayPal, and M-Pesa.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [API Endpoints](#api-endpoints)
4. [Authentication](#authentication)
5. [Payment Integration](#payment-integration)
6. [Email Integration](#email-integration)
7. [Logging](#logging)
8. [Usage](#usage)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd spaces-server
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Configuration

Configure the following settings in the `config.py` file:

- **M-Pesa Configuration**:

  ```python
  CONSUMER_KEY = "your_consumer_key"
  CONSUMER_SECRET = "your_consumer_secret"
  SHORTCODE = "your_shortcode"
  PASSKEY = "your_passkey"
  CALLBACK_URL = "https://yourdomain.com/path"
  ```

- **PayPal Configuration**:

  ```python
  PAYPAL_MODE = "live"
  PAYPAL_CLIENT_ID = "your_client_id"
  PAYPAL_CLIENT_SECRET = "your_client_secret"
  ```

- **Cloudinary Configuration**:

  ```python
  CLOUDINARY_CLOUD_NAME = "your_cloud_name"
  CLOUDINARY_API_KEY = "your_api_key"
  CLOUDINARY_API_SECRET = "your_api_secret"
  ```

- **Mailjet Configuration**:
  ```python
  MAILJET_API_KEY = "your_mailjet_api_key"
  MAILJET_SECRET_KEY = "your_mailjet_secret_key"
  ```

## API Endpoints

### User Management

- **Get All Users**: `GET /api/users`
- **Get User by ID**: `GET /api/users/<int:user_id>`
- **Update User by ID**: `PUT /api/users/<int:user_id>`
- **Delete User by ID**: `DELETE /api/users/<int:user_id>`
- **Patch User by ID**: `PATCH /api/users/<int:user_id>`

### Space Management

- **Get All Spaces**: `GET /api/spaces`
- **Get Space by ID**: `GET /api/spaces/<int:space_id>`
- **Create Space**: `POST /api/spaces`
- **Update Space by ID**: `PUT /api/spaces/<int:space_id>`
- **Delete Space by ID**: `DELETE /api/spaces/<int:space_id>`
- **Patch Space by ID**: `PATCH /api/spaces/<int:space_id>`

### Booking Management

- **Get All Bookings**: `GET /api/bookings`
- **Get Booking by ID**: `GET /api/bookings/<int:booking_id>`
- **Create Booking**: `POST /api/bookings`
- **Update Booking by ID**: `PUT /api/bookings/<int:booking_id>`
- **Delete Booking by ID**: `DELETE /api/bookings/<int:booking_id>`
- **Patch Booking by ID**: `PATCH /api/bookings/<int:booking_id>`

### Review Management

- **Get All Reviews**: `GET /api/reviews`
- **Get Review by ID**: `GET /api/reviews/<int:review_id>`
- **Create Review**: `POST /api/reviews`
- **Update Review by ID**: `PUT /api/reviews/<int:review_id>`

### Payment Management

- **Get All Payments**: `GET /api/payments`
- **Get Payment by ID**: `GET /api/payments/<int:payment_id>`
- **Create Payment**: `POST /api/payments`
- **Update Payment by ID**: `PUT /api/payments/<int:payment_id>`
- **Delete Payment by ID**: `DELETE /api/payments/<int:payment_id>`
- **Patch Payment by ID**: `PATCH /api/payments/<int:payment_id>`
- **Process Payment**: `POST /api/payments/<int:payment_id>`

### Event Management

- **Get All Events**: `GET /api/events`
- **Get Event by ID**: `GET /api/events/<int:event_id>`
- **Create Event**: `POST /api/events`
- **Update Event by ID**: `PATCH /api/events/<int:event_id>`
- **Delete Event by ID**: `DELETE /api/events/<int:event_id>`

### Authentication

- **Login**: `POST /api/login`
- **Logout**: `DELETE /api/logout`
- **Check Session**: `GET /api/check_session`

### Other Endpoints

- **Send Email**: `POST /api/send-email`
- **M-Pesa Callback**: `POST /api/callback/<int:payment_id>/`
- **PayPal Payment Success**: `GET /api/payment_success/<int:payment_id>`
- **PayPal Payment Cancel**: `GET /api/payment_cancel/<int:payment_id>`

## Authentication

Authentication is managed using JSON Web Tokens (JWT). The `token_required` decorator is used to protect endpoints that require authentication.

## Payment Integration

### M-Pesa

M-Pesa payments are initiated using the `POST /api/payments/<int:payment_id>` endpoint with `payment_method` set to `mpesa`.

### PayPal

PayPal payments are initiated using the `POST /api/payments/<int:payment_id>` endpoint with `payment_method` set to `paypal`.

## Email Integration

Emails are sent using Mailjet. Configure your Mailjet credentials in the configuration file.

## Logging

Logging is configured to display debug information. Adjust the logging level as needed:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
