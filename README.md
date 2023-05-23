# Async Python Wrapper for KeepinCRM API

This is an async Python wrapper for the KeepinCRM API that allows you to interact with the API using simple and convenient methods. The wrapper provides a `KeepinClient` class with async methods for making HTTP requests and retrieving data from the API.

## Installation

You can install the library using pip:

```shell
pip install aiokeepin
```

## Usage

To use the KeepinCRM async Python wrapper, import the `KeepinClient` class from the library:

```python
from aiokeepin import KeepinClient
```

### Initializing the Client

Create an instance of the `KeepinClient` class by providing your API key:

```python
client = KeepinClient(api_key='YOUR_API_KEY')
```

### Making API Requests

The `KeepinClient` instance provides async methods that correspond to the different HTTP request methods (`GET`, `POST`, `PATCH`, `PUT`, `DELETE`). Each method returns a dictionary containing the response from the API.

#### GET Request Example

```python
response = await client.get('/clients')
print(response)
```

#### POST Request Example

```python
data = {
  "email": "pib@example.com",
  "company": "Назва чи ПІБ",
  "lead": True,
  "source_id": 5,
  "status_id": 1,
  "phones": [
    "+380000000001"
  ],
  "tag_names": [
    "VIP"
  ],
  "contacts_attributes": [
    {
      "fullname": "Прізвище Імʼя По батькові",
      "phones": [
        "+380000000002"
      ],
      "custom_fields": [
        {
          "name": "Посада",
          "value": "Директор"
        }
      ]
    }
  ]
}

response = await client.post('/clients', data=data)
print(response)
```

#### PATCH Request Example

```python
data = {
  "email": "new_email@example.com"
}

response = await client.patch('/clients/{client_id}', data=data)
print(response)
```

#### PUT Request Example

```python
data = {
  "email": "updated_email@example.com"
}

response = await client.put('/clients/{client_id}', data=data)
print(response)
```

#### DELETE Request Example

```python
response = await client.delete('/clients/{client_id}')
print(response)
```

#### GET Paginated Items Example

```python
response = await client.get_paginated_items('/clients')
```

## Error Handling

In case of an error response from the KeepinCRM API, an exception will be raised. The exceptions provided by the aiokeepin library inherit from the base `KeepinException` class. There are several specific exceptions available for different types of errors:

- `KeepinStatusError`: This exception is raised for non-2xx status codes. It contains the `status_code` and `response` attributes, providing information about the error.

- `InvalidAPIKeyError`: This exception is raised specifically for an invalid API key.

- `ValidationError`: This exception is raised for invalid data.

- `NotFoundError`: This exception is raised when the requested resource is not found.

- `InternalServerError`: This exception is raised for internal server errors.

When making API requests, you can handle exceptions using try-except blocks to capture and handle specific types of errors. Here's an example:

```python
from aiokeepin.exceptions import KeepinStatusError, InvalidAPIKeyError

try:
    response = await client.get('/nonexistent_endpoint')
except InvalidAPIKeyError:
    print("Invalid API key provided.")
except KeepinStatusError as e:
    print(f"Error: {e.status_code} - {e.response}")
```

You can customize the exception handling based on your specific needs. By catching the appropriate exceptions, you can handle different error scenarios and provide appropriate error messages or take specific actions. Make sure to refer to the documentation for the KeepinCRM API for more details on the possible error responses and their corresponding status codes.

## Documentation

For detailed information on the KeepinCRM API, refer to the official API documentation: [KeepinCRM API Documentation](https://app.swaggerhub.com/apis/KeepInCRM/keepincrm-api/0.12.3)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.