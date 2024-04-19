# Events app

### Description:
Events, roles, and related stuff

## /location

### Description:
List all locations or create new location

### Methods:
- `GET`: Display locations
- `POST`: Create new location

### GET method

#### Example:
```json
{
  "count": 40,
  "next": "http://0.0.0.0:8000/location?limit=25&offset=25",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "learn",
      "address_line": "0266 Anna Groves Suite 817\nWilliamsbury, WA 37085",
      "city": "Lake Gregoryhaven",
      "postal_code": "06929",
      "country": "TR"
    },
    {
      "id": 2,
      "name": "north",
      "address_line": "078 White Dam\nNew April, NV 78577",
      "city": "Port Luis",
      "postal_code": "90034",
      "country": "TH"
    },
  ...
}
```
#### Response codes:
- `200 OK` - Locations get listed
- `400 BAD REQUEST` - Invalid request parameters

### POST method

#### Parameters:
- `name`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Location name",
        "max_length": 150
      }
    ```
- `address_line`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Address line",
        "max_length": 300
      }
    ```
- `city`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "City",
        "max_length": 100
      }
    ```
- `postal_code`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Postal code",
        "max_length": 20
      }
    ```
- `country`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Country",
        "max_length": 3
      }
    ```

#### Example response
```json
{
  "id": 41,
  "name": "example",
  "address_line": "example",
  "city": "example",
  "postal_code": "example",
  "country": "XMP"
}
```

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /event

### Description:
List all events or create new events

### Methods:
- `GET`: Display events
- `POST`: Create new event

### GET method

#### Example:
```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Congress",
      "desc": "Kitchen modern Republican husband politics four force. Standard degree price art radio.",
      "picture": null,
      "start": "2023-11-12T02:21:21.891000+01:00",
      "end": "2024-05-12T13:33:52.019000+02:00",
      "location": 12
    },
    {
      "id": 2,
      "title": "their",
      "desc": "Close way camera table sell anyone tonight. Game opportunity mention across.",
      "picture": null,
      "start": "2023-11-13T18:04:56.647000+01:00",
      "end": "2024-04-20T16:47:51.425000+02:00",
      "location": 38
    },
  ...
}
```
#### Response codes:
- `200 OK` - Locations get listed
- `400 BAD REQUEST` - Invalid request parameters

### POST method

#### Parameters:
- `title`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Title",
        "max_length": 150
      }
    ```
- `desc`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Description",
        "max_length": 300
      }
    ```
- `picture`:
    ```json
      {
        "type": "image upload",
        "required": false,
        "read_only": false,
        "label": "Picture",
        "max_length": 100
      }
    ```
- `start`:
    ```json
      {
        "type": "datetime",
        "required": false,
        "read_only": false,
        "label": "Start date"
      }
    ```
- `end`:
    ```json
      {
        "type": "datetime",
        "required": false,
        "read_only": false,
        "label": "End date"
      }
    ```
- `location`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Location"
      }
    ```

#### Example response
```json
{
  "id": 41,
  "name": "example",
  "address_line": "example",
  "city": "example",
  "postal_code": "example",
  "country": "XMP"
}
```

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /event/`pk`

### Description:
Display, edit, delete event with pk id

### Methods:
- `GET`: Display event
- `PUT`: Update event information
- `DELETE`: Delete the event

### GET method

#### Example:
```json
{
  "id": 1,
  "event_contacts": [
    {
      "id": 19,
      "name": "Andrew Stanton",
      "phone": "001-405-603-5306"
    },
    {
      "id": 34,
      "name": "Emily Flowers",
      "phone": "780-544-3785x485"
    },
    {
      "id": 41,
      "name": "Troy Hall",
      "phone": "001-915-741-0328"
    },
    {
      "id": 48,
      "name": "Zachary Solomon",
      "phone": "(253)649-1082x2541"
    }
  ],
  "social_media": [
    {
      "id": 20,
      "link": "https://www.curtis.com/",
      "platform": "INSTAGRAM"
    }
  ],
  "location": {
    "id": 12,
    "name": "view",
    "address_line": "336 Simpson Prairie Apt. 656\nSouth Ellen, IL 04014",
    "postal_code": "57783",
    "country": "AD"
  },
  "title": "Congress",
  "desc": "Kitchen modern Republican husband politics four force. Standard degree price art radio.",
  "picture": null,
  "start": "2023-11-12T02:21:21.891000+01:00",
  "end": "2024-05-12T13:33:52.019000+02:00"
}
}
```
#### Response codes:
- `200 OK` - Events get listed
- `400 BAD REQUEST` - Invalid request parameters
- `404 NOT FOUND` - `pk` value doesn't match any id

### PUT method

#### Parameters:
- `title`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Title",
        "max_length": 150
      }
    ```
- `desc`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Description",
        "max_length": 300
      }
    ```
- `picture`:
    ```json
      {
        "type": "image upload",
        "required": false,
        "read_only": false,
        "label": "Picture",
        "max_length": 100
      }
    ```
- `start`:
    ```json
      {
        "type": "datetime",
        "required": false,
        "read_only": false,
        "label": "Start date"
      }
    ```
- `end`:
    ```json
      {
        "type": "datetime",
        "required": false,
        "read_only": false,
        "label": "End date"
      }
    ```
- `location`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Location"
      }
    ```


#### Example response
```json
{
  "id": 23,
  "title": "example",
  "desc": "example",
  "picture": null,
  "start": null,
  "end": null,
  "location": 1
}
```

#### Permissions
User has to have at least moderator role in given event.

#### Response codes:
- `200 OK` - Post was succesfully updated
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to update a post
- `404 NOT FOUND` - `pk` value doesn't match any id

### DELETE method

#### Permissions:
User has at least owner permission in current group

#### Response codes:
- `204 NO CONTENT` - Event was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to delete a post
- `404 NOT FOUND` - `pk` value doesn't match any id


## /role

### Description:
Create new role

### Methods:
- `POST`: Create default - user role

### POST method

#### Parameters:
- `event`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Event"
      }
    ```

#### Example response
```json
{
  "id": 68,
  "event": 3,
  "user": 25,
  "name": 0
}
```

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /role/`pk`

### Description:
Edit, delete role with pk id

### Methods:
- `PUT`: Update role information
- `DELETE`: Delete the role

### PUT method

#### Parameters:
- `event`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Event"
      }
    ```
- `user`:
    ```json
      {
        "type": "field",
        "required": false,
        "read_only": true,
        "label": "User"
      }
    ```
- `name`:
    ```json
      {
        "type": "choice",
        "required": false,
        "read_only": false,
        "label": "Role name",
        "choices": [
          {
            "value": 3,
            "display_name": "owner"
          },
          {
            "value": 2,
            "display_name": "moderator"
          },
          {
            "value": 1,
            "display_name": "staff"
          },
          {
            "value": 0,
            "display_name": "user"
          }
        ]
      }
    ```

#### Permissions
User has to have at least owner role in given event.

#### Response codes:
- `200 OK` - Role was succesfully updated
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to update a post
- `404 NOT FOUND` - `pk` value doesn't match any id

### DELETE method

#### Permissions:
User has at least owner permission in current group or is the owner of this role

#### Response codes:
- `204 NO CONTENT` - Role was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to delete a role
- `404 NOT FOUND` - `pk` value doesn't match any id



## /event-contact

TBD

## /event-contact/`pk`

TBD

## /social-media

TBD

## /social-media/`pk`

TBD

# Posts_comments app

### Description:
Posts, comments and votes 

## /post
### Description:
List all posts or create new post

### Methods:
- `GET`: Display posts
- `POST`: Create new post

### GET method

#### Example:
```json
{
  "count": 40,
  "next": "http://0.0.0.0:8000/post?limit=25&offset=25",
  "previous": null,
  "results": [
    {
      "id": 1,
      "vote_count": 1,
      "has_voted": false,
      "title": "research",
      "desc": "Property really upon reduce.",
      "created_at": "2023-08-22T06:41:35.968000+02:00",
      "modified_at": null,
      "picture": null,
      "event": 7
    },
    {
      "id": 2,
      "vote_count": 4,
      "has_voted": false,
      "title": "public",
      "desc": "Play watch American mind describe. Human leave easy. Before south head memory ok.",
      "created_at": "2023-09-27T21:49:39.038000+02:00",
      "modified_at": null,
      "picture": null,
      "event": 4
    },
  ...
}
```
#### Response codes:
- `200 OK` - Events get listed
- `400 BAD REQUEST` - Invalid request parameters

### POST method

#### Parameters:
- `title`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Title",
        "max_length": 150
      }
    ```
- `desc`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Description",
        "max_length": 300
      }
    ```
- `picture`:
    ```json
      {
        "type": "image upload",
        "required": false,
        "read_only": false,
        "label": "Picture",
        "max_length": 100
      }
    ```
- `event`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Event"
      }
    ```

#### Example response
```json
{
{
  "id": 41,
  "vote_count": 0,
  "has_voted": false,
  "title": "example",
  "desc": "example",
  "created_at": "2024-04-19T10:39:24.948910+02:00",
  "modified_at": null,
  "picture": null,
  "event": 22
}
}
```

#### Permissions
User has to have at least moderator role in given event.

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to create a post

## /post/`pk`
### Description:
Display, edit, delete posts with pk id

### Methods:
- `GET`: Display posts
- `PUT`: Update post information
- `DELETE`: Delete the post

### GET method

#### Example:
```json
{
  "id": 1,
  "vote_count": 1,
  "has_voted": false,
  "title": "research",
  "desc": "Property really upon reduce.",
  "created_at": "2023-08-22T06:41:35.968000+02:00",
  "modified_at": null,
  "picture": null,
  "event": 7
}
```
#### Response codes:
- `200 OK` - Events get listed
- `400 BAD REQUEST` - Invalid request parameters
- `404 NOT FOUND` - `pk` value doesn't match any id

### PUT method

#### Parameters:
- `title`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Title",
        "max_length": 150
      }
    ```
- `desc`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Description",
        "max_length": 300
      }
    ```
- `picture`:
    ```json
      {
        "type": "image upload",
        "required": false,
        "read_only": false,
        "label": "Picture",
        "max_length": 100
      }
    ```
- `event`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Event"
      }
    ```

#### Example response
```json
{
{
  "id": 41,
  "vote_count": 0,
  "has_voted": false,
  "title": "example",
  "desc": "example",
  "created_at": "2024-04-19T10:39:24.948910+02:00",
  "modified_at": null,
  "picture": null,
  "event": 22
}
}
```

#### Permissions
User has to have at least moderator role in given event.

#### Response codes:
- `200 OK` - Post was succesfully updated
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to update a post
- `404 NOT FOUND` - `pk` value doesn't match any id

### DELETE method

#### Response codes:
- `204 NO CONTENT` - ConcertifyUser and PaymentInfo was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to delete a post
- `404 NOT FOUND` - `pk` value doesn't match any id

## /comment
### Description:
List all comments or create new comment

### Methods:
- `GET`: Display comments
- `POST`: Create new comment

### GET method

#### Example:
```json
{
  "count": 80,
  "next": "http://0.0.0.0:8000/comment?limit=25&offset=25",
  "previous": null,
  "results": [
    {
      "id": 1,
      "vote_count": 4,
      "has_voted": false,
      "title": "amount",
      "desc": "Material result again year. Event wear apply movement ability.",
      "created_at": "2023-11-24T23:54:46.942000+01:00",
      "modified_at": null,
      "post": 28,
      "user": 9
    },
    {
      "id": 2,
      "vote_count": 1,
      "has_voted": false,
      "title": "cup",
      "desc": "Hour say as have.",
      "created_at": "2023-09-24T23:26:39.099000+02:00",
      "modified_at": null,
      "post": 1,
      "user": 7
    } "event": 4
    },
  ...
}
```
#### Response codes:
- `200 OK` - Events get listed
- `400 BAD REQUEST` - Invalid request parameters

### POST method

#### Parameters:
- `title`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Title",
        "max_length": 150
      }
    ```
- `desc`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Description",
        "max_length": 300
      }
    ```
- `post`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Post"
      }
    ```

#### Example response
```json
{
  "id": 81,
  "vote_count": 0,
  "has_voted": false,
  "title": "example",
  "desc": "example",
  "created_at": "2024-04-19T11:59:43.545857+02:00",
  "modified_at": null,
  "post": 1,
  "user": 25
}
```

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /comment/`pk`
### Description:
Display, edit, delete comment with pk id

### Methods:
- `GET`: Display comments
- `PUT`: Update comment information
- `DELETE`: Delete the comment

### GET method

#### Example:
```json
{
  "id": 1,
  "vote_count": 4,
  "has_voted": false,
  "title": "amount",
  "desc": "Material result again year. Event wear apply movement ability.",
  "created_at": "2023-11-24T23:54:46.942000+01:00",
  "modified_at": null,
  "post": 28,
  "user": 9
}
```
#### Response codes:
- `200 OK` - Events get listed
- `400 BAD REQUEST` - Invalid request parameters
- `404 NOT FOUND` - `pk` value doesn't match any id

### PUT method

#### Parameters:
- `title`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Title",
        "max_length": 150
      }
    ```
- `desc`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Description",
        "max_length": 300
      }
    ```
- `picture`:
    ```json
      {
        "type": "image upload",
        "required": false,
        "read_only": false,
        "label": "Picture",
        "max_length": 100
      }
    ```
- `event`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Event"
      }
    ```

#### Example response
```json
{
{
  "id": 41,
  "vote_count": 0,
  "has_voted": false,
  "title": "example",
  "desc": "example",
  "created_at": "2024-04-19T10:39:24.948910+02:00",
  "modified_at": null,
  "picture": null,
  "event": 22
}
}
```

#### Permissions
User has to have at least moderator role in given event.

#### Response codes:
- `200 OK` - Post was succesfully updated
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to update a post
- `404 NOT FOUND` - `pk` value doesn't match any id

### DELETE method

#### Response codes:
- `204 NO CONTENT` - ConcertifyUser and PaymentInfo was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to delete a post
- `404 NOT FOUND` - `pk` value doesn't match any id


## /post-vote
### Description:
Create new post vote

### Methods:
- `POST`: Create new post vote

### POST method

#### Parameters:
- `post`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Post"
      }
    ```

#### Example response
```json
{
  "id": 123,
  "post": 1,
  "user": 25
}
```

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /post-vote/`pk`
### Description:
Delete post vote with pk id

### Methods:
- `DELETE`: Delete post vote with given `pk`

### DELETE method

#### Response codes:
- `204 NO CONTENT` - ConcertifyUser and PaymentInfo was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to delete a post
- `404 NOT FOUND` - `pk` value doesn't match any id


## /comment-vote
### Description:
Create new comment vote

### Methods:
- `POST`: Create new comment vote

### POST method

#### Parameters:
- `comment`:
    ```json
      {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Comment"
      }
    ```

#### Example response
```json
{
  "id": 241,
  "comment": 1,
  "user": 25
}
```

#### Response codes:
- `200 OK` - Post was succesfuly created
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /comment-vote/`pk`
### Description:
Delete comment vote with pk id

### Methods:
- `DELETE`: Delete comment vote with given `pk`

### DELETE method

#### Response codes:
- `204 NO CONTENT` - ConcertifyUser and PaymentInfo was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
- `403 FORBIDDEN` - User does not have permission to delete a post
- `404 NOT FOUND` - `pk` value doesn't match any id


# Users app

### Description:
User related requests

## /create

### Description:
Create user

### Methods:
- `POST`: create new ConcertifyUser

### Post method

#### Parameters:
- `first_name`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "First name",
        "max_length": 150
      }
    ```
- `last_name`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Last name",
        "max_length": 150
      }
    ```
- `username`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Username",
        "help_text": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        "max_length": 150
      }
    ```
- `email`:
    ```json
      {
        "type": "email",
        "required": true,
        "read_only": false,
        "label": "Email address",
        "max_length": 254
      }
    ```
- `password`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Password",
        "min_length": 9,
        "max_length": 128
      }
    ```
- `payment_info`:
    ```json
      {
        "type": "nested object",
        "required": false,
        "read_only": false,
        "label": "Payment info",
      }
    ```
  Children:
  - `line1`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Address line 1",
        "max_length": 300
      }
    ```
  - `line2`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Address line 2",
        "max_length": 300
      }
    ```
  - `city`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "City",
        "max_length": 150
      }
    ```
  - `postal_code`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Postal code",
        "max_length": 20
      }
    ```
  - `country`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Country",
        "max_length": 3
      }
    ```
  - `telephone`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Telephone number",
        "max_length": 128
      }
    ```
  - `mobile`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Mobile phone number",
        "max_length": 128
      }
    ```

#### Response codes:
- `201 CREATED` - ConcertifyUser and PaymentInfo was succesfully created
- `400 BAD REQUEST` - Invalid request parameters

## /profile

### Description:
Display and edit current user profile

### Methods:
- `GET`: Display profile
- `PUT`: Update profile
- `DELETE`: Delete profile

### GET method

#### Example:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "johndoe@example.org",
  "payment_info": {
    "id": 24,
    "line1": "FPO AP 79870",
    "line2": "USNS Wright",
    "city": "Los Angeles",
    "postal_code": "60632",
    "country": "BO",
    "telephone": "+48893202891",
    "mobile": "+48248249993",
    "user": 24
  }
}
```
#### Response codes:
- `200 OK` - ConcertifyUser and PaymentInfo was succesfully returned
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

### PUT method

#### Parameters:
- `first_name`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "First name",
        "max_length": 150
      }
    ```
- `last_name`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Last name",
        "max_length": 150
      }
    ```
- `username`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Username",
        "help_text": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        "max_length": 150
      }
    ```
- `email`:
    ```json
      {
        "type": "email",
        "required": true,
        "read_only": false,
        "label": "Email address",
        "max_length": 254
      }
    ```
- `payment_info`:
    ```json
      {
        "type": "nested object",
        "required": false,
        "read_only": false,
        "label": "Payment info",
      }
    ```
  Children:
  - `line1`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Address line 1",
        "max_length": 300
      }
    ```
  - `line2`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Address line 2",
        "max_length": 300
      }
    ```
  - `city`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "City",
        "max_length": 150
      }
    ```
  - `postal_code`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Postal code",
        "max_length": 20
      }
    ```
  - `country`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Country",
        "max_length": 3
      }
    ```
  - `telephone`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Telephone number",
        "max_length": 128
      }
    ```
  - `mobile`:
    ```json
      {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Mobile phone number",
        "max_length": 128
      }
    ```

#### Example response
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "johndoe@example.org",
  "payment_info": {
    "id": 24,
    "line1": "FPO AP 79870",
    "line2": "USNS Wright",
    "city": "Los Angeles",
    "postal_code": "60632",
    "country": "BO",
    "telephone": "+48893202891",
    "mobile": "+48248249993",
    "user": 24
  }
}
```

#### Response codes:
- `200 OK` - ConcertifyUser and PaymentInfo was succesfully updated
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

### DELETE method

#### Response codes:
- `204 NO CONTENT` - ConcertifyUser and PaymentInfo was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /profile/password

### Description:
Display and edit current user profile

### Methods:
- `PUT`: Update password 

### PUT method

#### Parameters:
- `old_password`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Old password",
        "max_length": 128
      }
    ```
- `password1`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Password1",
        "max_length": 128
      }
    ```
- `password2`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Password2",
        "max_length": 128
      }
    ```

#### Response codes:
- `200 OK` - Password was succesfully updated
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /login
### Methods:
- `POST`: login user

#### Parameters:
- `username`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Username",
        "max_length": 150
      }
    ```
- `password`:
    ```json
      {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Password",
        "max_length": 128
      }
    ```

#### Example response
```json
{
    "expiry": "2024-04-19T03:44:05.393381+02:00",
    "token": "080d3a2ec6552a9ac57e403fb28aba4f27d37722f2793aad3b2d7081b1d60d54",
    "user": {
        "username": "example"
    }
}
```

#### Response codes:
- `200 OK` - User succesfully logged in
- `400 BAD REQUEST` - Invalid request parameters

## /logout
### Methods:
- `POST`: delete current token

#### Response codes:
- `204 NO CONTENT` - Token was succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials

## /logoutall
### Methods:
- `POST`: delete all user tokens

#### Response codes:
- `204 NO CONTENT` - Tokens were succesfully deleted
- `400 BAD REQUEST` - Invalid request parameters
- `401 UNAUTHORIZED` - Invalid credentials
