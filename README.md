# Skyloov Assignment Documentation

## How to run

### Docker
- Run `docker-compose up --build --no-deps` for launching the project with Docker.
- In a different terminal, run `docker exec -it skyloov-web-1 /bin/bash`. Please use the correct container name.
    - Run `cd /code` to change into the code directory.
    - Execute `python manage.py makemigrations` for creating migration files.
    - Execute `python manage.py migrate` for running the database migrations.
    - Execute `python manage.py createsuperuser` and fill up the details of the superuser.
    - Execute `python manage.py populate_real_products` to populate the Products with sample data for testing.

### Notes
- For quick and easy project setup, I have included the .env file in the Git repository.
- To learn more about the configuration, please refer to the docker-compose.yml file.
- You can populate the database with sample products by using the provided command and verifying in Django Admin.
- Authenticated users can upload product images, which are automatically converted into different sizes, such as 150 x 150 (thumbnail), 300 x 300 (small), and 1200 x 1200 (large), using multiprocessing.
- The welcome email notification is scheduled to be sent after 86400 seconds, which can be changed from the settings.
- You can also customize the page size in a paginated response from the settings.


### Important Links
- [Django Admin](localhost:8000/admin/)
- [Swagger](localhost:8000/docs/)

# API Documentation

Endpoints
1. [User Account Creation API](#1)
2. [Authentication JWT Generation API](#2)
3. [Authentication JWT Refresh API](#3)
4. [Product Search API](#4)
5. [Product Image Upload API](#5)
6. [View Cart Items API](#6)
7. [API Endpoint: Add to Cart](#7)
8. [UpdateCartItemQuantityView](#8)
9. [Remove Cart Item API](#9) 

## User Account Creation API <a id="1"></a>

### Description
This API creates a new user account in the database with the provided `username`, `email`, and `password`. It returns the newly created user instance if the operation is successful. It also sends a welcome email to the user after 24 hours.

### URL
```
POST /api/register/
```

### Request
- Content-Type: application/json
- Body:

    | Field | Type | Required | Description |
    |-------|------|----------|-------------|
    | username | string | yes | The username of the new user |
    | email | string | yes | The email of the new user |
    | password | string | yes | The password of the new user |
    | confirm_password | string | yes | Confirmation of the password of the new user |

### Response
- Status Code: 201 Created
- Body:

    | Field | Type | Description |
    |-------|------|-------------|
    | username | string | The username of the new user |
    | email | string | The email of the new user |

- Error Response:
  - Status Code: 400 Bad Request
  - Body:
  
    | Field | Type | Description |
    |-------|------|-------------|
    | error | string | A brief error message |
    | detail | string | A detailed error message |

### Email Sending Functionality
- A signal is triggered after a new user is created.
- It sends a welcome email to the newly registered user after `WELCOME_EMAIL_DELAY_SECONDS` seconds (24 hours for our use case).
![Email Example](https://github.com/thakurfurqaan/skyloov/blob/master/Skyloov%20Welcome%20Email%20Example.jpg)

## Authentication JWT Generation API <a id="2"></a>

### URL

POST `/api/token/`

**Description:** This endpoint is used to obtain an access token and a refresh token for a user using their username and password. 

### Request Body Parameters

| Parameter | Type   | Required | Description                                            |
|-----------|--------|----------|--------------------------------------------------------|
| username  | string | Yes      | The username of the user to authenticate.              |
| password  | string | Yes      | The password of the user to authenticate.              |


### Response Body Parameters

| Parameter    | Type   | Required | Description                                                                           |
|--------------|--------|----------|---------------------------------------------------------------------------------------|
| access_token | string | Yes      | The access token to use for subsequent API requests.                                   |

### Successful Response

**HTTP Status Code:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJ...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

### Error Responses

**HTTP Status Code:** `400 BAD REQUEST`

```json
{
  "detail": "No active account found with the given credentials"
}
```

**HTTP Status Code:** `401 UNAUTHORIZED`

```json
{
  "detail": "Invalid username/password."
}
```

## Authentication JWT Refresh API <a id="3"></a>

### URL

```
POST /api/token/refresh/
```

### Authentication

- This endpoint requires valid access token in the authorization header to access.

### Parameters

| Parameter  | Required | Type   | Description                    |
| ---------- | -------- | ------ | ------------------------------ |
| `refresh` | Yes      | String | A valid refresh token issued for the user |

### Response

**Response Body**

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
}
```

- `access`: A new JWT access token that can be used to authenticate subsequent requests.

### Sample Request

**Request**

```http
POST /api/token/refresh/ HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer <refresh_token>

{
    "refresh": "<refresh_token>"
}
```

**Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
}
```


## Product Search API <a id="4"></a>

This API allows authenticated users to search for products using various filters and sorting and get a paginated response back.

### URL

GET `/api/products/search/`

### Authentication Required

Yes

### Request Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| category | Integer | No | The category to filter by |
| brand | Integer | No | The brand to filter by |
| price | Integer | No | The price range to filter by. Format: `gte:lte` |
| quantity | Integer | No | The quantity range to filter by. Format: `gte:lte` |
| created_at | String | No | The date range to filter by. Format: `yyyy-mm-dd:yyyy-mm-dd` |
| ordering | String | No | The field to order by. Allowed values: `price`, `rating`, `created_at`, `quantity`. Prefix with `-` to sort in descending order. |

### Response Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| id | Integer | The unique identifier of the product |
| name | String | The name of the product |
| description | String | The description of the product |
| price | Decimal | The price of the product |
| quantity | Integer | The quantity of the product |
| category | Integer | The category of the product |
| brand | Integer | The brand of the product |
| created_at | Datetime | The date and time when the product was created |
| updated_at | Datetime | The date and time when the product was last updated |
| rating | Decimal | The rating of the product |
| images | List | The list of images associated with the product |

### Example Request

```
GET /api/products/search?ordering=quantity&quantity__gte=5&quantity__lte=10
```

### Example Response

```
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 12,
            "name": "Damac Hills Villa",
            "description": "Luxurious 4-bedroom villa in Damac Hills with private pool and golf course view",
            "price": "3500000.00",
            "quantity": 5,
            "category": "Villa",
            "brand": "Damac Properties",
            "created_at": "2023-05-07T07:39:44.527709Z",
            "updated_at": "2023-05-07T07:39:44.527743Z",
            "rating": 4.9,
            "images": []
        },
        {
            "id": 19,
            "name": "Jumeirah Village Circle Townhouse",
            "description": "Lovely 3-bedroom townhouse in Jumeirah Village Circle with private garden",
            "price": "2500000.00",
            "quantity": 6,
            "category": "Townhouse",
            "brand": "Nakheel",
            "created_at": "2023-05-07T07:39:44.558762Z",
            "updated_at": "2023-05-07T07:39:44.558787Z",
            "rating": 4.8,
            "images": []
        },
        {
            "id": 14,
            "name": "Jumeirah Lake Towers Office",
            "description": "Spacious office space in Jumeirah Lake Towers with beautiful lake view",
            "price": "2000000.00",
            "quantity": 8,
            "category": "Office",
            "brand": "DMCC",
            "created_at": "2023-05-07T07:39:44.539162Z",
            "updated_at": "2023-05-07T07:39:44.539194Z",
            "rating": 4.5,
            "images": []
        },
        {
            "id": 11,
            "name": "Emaar Beachfront Apartment",
            "description": "Beautiful 2-bedroom apartment in Emaar Beachfront with sea view",
            "price": "1200000.00",
            "quantity": 10,
            "category": "Apartment",
            "brand": "Emaar Properties",
            "created_at": "2023-05-07T07:39:44.480552Z",
            "updated_at": "2023-05-07T14:00:20.321926Z",
            "rating": 4.8,
            "images": [
                {
                    "id": 43,
                    "image": "http://localhost:8000/media/products/images/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg",
                    "thumbnail": "http://localhost:8000/media/products/thumbnails/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg-thumbnail.jpg",
                    "small": "http://localhost:8000/media/products/small/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg-small.jpg",
                    "large": "http://localhost:8000/media/products/large/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg-large.jpg"
                },
                {
                    "id": 44,
                    "image": "http://localhost:8000/media/products/images/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg",
                    "thumbnail": "http://localhost:8000/media/products/thumbnails/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg-thumbnail.jpg",
                    "small": "http://localhost:8000/media/products/small/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg-small.jpg",
                    "large": "http://localhost:8000/media/products/large/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg-large.jpg"
                }
            ]
        }
    ]
}
```

## Product Image Upload API <a id="5"></a>

This endpoint allows authenticated users to upload one or more images for a specific product. The images are processed in different sizes (thumbnail, small, and large) and saved as separate fields in the database.

### URL
```
POST /api/products/<int:pk>/upload-image/
```

### Authentication
This endpoint requires authentication. The user must include a valid JWT token in the `Authorization` header of the request.

### Request Parameters
- `pk`: The ID of the product to which the images are being uploaded. It must be an integer.

### Request Body
- `images`: A list of image files to be uploaded. The files must be in JPEG or PNG format and must not exceed 2 MB in size.

### Response
If the request is successful, the API will respond with an HTTP status code `201 Created`.

If there is an error with the request, the API will respond with an HTTP status code `400 Bad Request` and include an error message in the response body.

### Example Request
```
POST /api/products/11/upload-image/
```

### Example Response

```json
HTTP/1.1 201 Created
```

### Processing Images
When an image is uploaded, the server processes it in the following way:
- The original image is opened using the PIL library.
- Three versions of the image are generated in different sizes (thumbnail, small, and large).
- Each version is saved as a separate field in the `ProductImage` model in the database.

The image processing is performed asynchronously using Python's `multiprocessing` library to improve the performance of the endpoint. The `process_product_image` function is called in a separate process for each image that is uploaded.





## View Cart Items API <a id="6"></a>

This API endpoint is used to get a list of items in the cart of the authenticated user.

### URL

```
GET /api/cart/items/
```

### Request Parameters

No request parameters are required for this endpoint.

### Request Headers

This endpoint requires a `Authorization` header with the JWT token received from the authentication endpoint.


### Response Body

The response body will contain a list of all items in the authenticated user's cart.

Each item will have the following attributes:

- `id`: The ID of the cart item
- `product`: An object containing the following details of the product in the cart:
- `id`: The ID of the product
- `name`: The name of the product
- `description`: The description of the product
- `price`: The price of the product
- `quantity`: The quantity of the product
- `category`: The category of the product
- `brand`: The brand of the product
- `created_at`: The date and time at which the product was created
- `updated_at`: The date and time at which the product was last updated
- `rating`: The rating of the product
- `images`: A list of objects containing the details of all the images associated with the product
- `quantity`: The quantity of the product in the cart

### Example Response

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "product": {
                "id": 11,
                "name": "Emaar Beachfront Apartment",
                "description": "Beautiful 2-bedroom apartment in Emaar Beachfront with sea view",
                "price": "1200000.00",
                "quantity": 10,
                "category": "Apartment",
                "brand": "Emaar Properties",
                "created_at": "2023-05-07T07:39:44.480552Z",
                "updated_at": "2023-05-07T14:00:20.321926Z",
                "rating": 4.8,
                "images": [
                    {
                        "id": 43,
                        "image": "http://localhost:8000/media/products/images/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg",
                        "thumbnail": "http://localhost:8000/media/products/thumbnails/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg-thumbnail.jpg",
                        "small": "http://localhost:8000/media/products/small/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg-small.jpg",
                        "large": "http://localhost:8000/media/products/large/WhatsApp_Image_2023-04-30_at_11.51.31.jpeg-large.jpg"
                    },
                    {
                        "id": 44,
                        "image": "http://localhost:8000/media/products/images/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg",
                        "thumbnail": "http://localhost:8000/media/products/thumbnails/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg-thumbnail.jpg",
                        "small": "http://localhost:8000/media/products/small/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg-small.jpg",
                        "large": "http://localhost:8000/media/products/large/WhatsApp_Image_2023-04-30_at_11.44.56.jpeg-large.jpg"
                    }
                ]
            },
            "quantity": 3
        }
    ]
}
```

### Error Response

- `401 Unauthorized`: If the user is not authenticated

## API Endpoint: Add to Cart <a id="7"></a>

The Add to Cart endpoint allows authenticated users to add products to their cart.

### URL

`POST /api/cart/items/add/`

### Request Parameters

The request should include a JSON body containing the following parameters:

| Parameter | Required | Type   | Description                                                  |
| --------- | -------- | ------ | ------------------------------------------------------------ |
| `product` | Yes      | Number | The ID of the product to add to the cart.                     |
| `quantity`| Yes      | Number | The quantity of the product to add to the cart.               |

### Response

If the request is successful, the endpoint will return a JSON response containing the added product information, including its quantity in the cart.

### Example Request

```http
POST /api/cart/items/add/
Content-Type: application/json
Authorization: Bearer <token>

{
    "product": 1,
    "quantity": 2
}
```

### Example Response

```json
HTTP 201 Created
Content-Type: application/json

{
    "product": 12,
    "quantity": 1
}
```

## Update Cart Item Quantity API <a id="8"></a>

Endpoint to update the quantity of a product in the user's cart.

### URL

PUT `/api/cart/items/<int:pk>/quantity/`

### URL Params

- `pk`: the primary key of the `CartItem` instance to be updated.

### Body Params

- `quantity`: (required) the new quantity of the product in the cart.

### Success Response

- Code: `200 OK`

### Example Request

```
PUT /api/cart/items/3/quantity/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <access_token>

{
    "quantity": 3
}
```

### Example Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "product": 12,
    "quantity": 3
}
```

## Remove Cart Item API <a id="9"></a>

This endpoint removes an item from the user's cart.

### Request

`DELETE /api/cart/items/<int:pk>/remove/`

### Parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| pk | integer | Yes | The ID of the cart item to remove. |

### Response

The response will have a status code of 204 (No Content) if the cart item was successfully removed.

### Example

```
DELETE /api/cart/items/42/remove/
```
