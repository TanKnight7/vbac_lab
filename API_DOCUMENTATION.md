# VBAC Lab API Documentation

## Overview
- **Base URL**: `/api/`
- **Authentication**: Token-based Authentication or Session Authentication.
- **Content-Type**: `application/json`

## Role Access Matrix
The following table summarizes which roles can perform actions on each resource.

| Resource | Action | Allowed Roles |
| :--- | :--- | :--- |
| **Users** | Create | Super Admin, Admin |
| | Read (List/Retrieve) | Super Admin, Admin, Editor, Author, Contributor |
| | Update/Delete | Super Admin, Admin |
| **Groups** | Any Action | Super Admin, Admin |
| **Posts** | Create | Super Admin, Admin, Editor, Author, Contributor |
| | Read (Public) | Everyone (Public posts only) |
| | Read (All) | Super Admin, Admin, Editor (Can see all) |
| | Update (Own) | Author (Own posts) |
| | Update (Any) | Super Admin, Admin, Editor |
| | Delete | Super Admin, Admin, Editor, Author (Own only) |
| **Pages** | Create | Super Admin, Admin, Editor |
| | Read | Everyone |
| | Update/Delete | Super Admin, Admin, Editor |
| **Media** | Upload | Super Admin, Admin, Editor, Author |
| | Read | Super Admin, Admin, Editor, Author, Contributor, Subscriber |
| | Update/Delete | Super Admin, Admin |
| **Comments** | Create | Super Admin, Admin, Editor, Author, Contributor, Subscriber |
| | Read | Everyone (Public posts), Author (Own) |
| | Update (Own) | Author (Own comments) |
| | Delete | Super Admin, Admin, Editor, Author (Own only) |

| **Plugins** | Create | Super Admin |
| | Read | Super Admin, Admin |
| | Update/Delete | Super Admin, Admin |

---

## 1. User Management
### Users
**Base URL**: `/api/users/`

#### `GET /api/users/`
- **Description**: List all users.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author, Contributor.
- **Response**: List of User objects.

#### `POST /api/users/`
- **Description**: Create a new user.
- **Allowed Roles**: Super Admin, Administrator.
- **Request Body**:
  - `username` (string, required)
  - `password` (string, required, write-only)
  - `email` (string)
  - `groups` (list of urls)
- **Response**: Created User object.

#### `GET /api/users/{id}/`
- **Description**: Retrieve user details.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author, Contributor.

#### `PUT /api/users/{id}/`
- **Description**: Update user details.
- **Allowed Roles**: Super Admin, Administrator.

#### `DELETE /api/users/{id}/`
- **Description**: Delete a user.
- **Allowed Roles**: Super Admin, Administrator.

### Groups
**Base URL**: `/api/groups/`

#### `GET /api/groups/`
- **Description**: List all groups.
- **Allowed Roles**: Super Admin, Administrator.
- **Response**: List of Group objects.

#### `POST /api/groups/`
- **Description**: Create a new group.
- **Allowed Roles**: Super Admin, Administrator.
- **Request Body**:
  - `name` (string, required)

---

## 2. Content Management
### Posts
**Base URL**: `/api/posts/`

#### `GET /api/posts/`
- **Description**: List posts. Public users see only 'publish' status. Authenticated users see their own posts and public posts. Admins/Editors see all.
- **Allowed Roles**: Public (Anyone).
- **Response**: List of Post objects.

#### `POST /api/posts/`
- **Description**: Create a new post. Default status is 'draft'.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author, Contributor.
- **Request Body**:
  - `title` (string, required)
  - `content` (string, required)
  - `status` (string: 'draft', 'publish', 'private')
- **Response**: Created Post object.

#### `GET /api/posts/{id}/`
- **Description**: Retrieve post details.
- **Allowed Roles**: Public (Anyone).

#### `PUT /api/posts/{id}/`
- **Description**: Update a post. Authors can update their own posts. Higher roles can update any post.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author, Contributor.
  - **Publishing**: Only Super Admin, Administrator, Editor, Author.
  - **Private**: Only Super Admin, Administrator, Editor.

#### `DELETE /api/posts/{id}/`
- **Description**: Delete a post.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author, Contributor.
  - **Note**: Contributors/Authors can only delete their own Drafts. Published/Private posts generally require higher privileges.

### Pages
**Base URL**: `/api/pages/`

#### `GET /api/pages/`
- **Description**: List pages.
- **Allowed Roles**: Public (Anyone).
- **Response**: List of Page objects.

#### `POST /api/pages/`
- **Description**: Create a new page.
- **Allowed Roles**: Super Admin, Administrator, Editor.
- **Request Body**:
  - `title` (string, required)
  - `content` (string, required)
  - `status` (string)

#### `GET /api/pages/{id}/`
- **Description**: Retrieve page details.
- **Allowed Roles**: Public (Anyone).

#### `PUT /api/pages/{id}/`
- **Description**: Update a page.
- **Allowed Roles**: Super Admin, Administrator, Editor.

#### `DELETE /api/pages/{id}/`
- **Description**: Delete a page.
- **Allowed Roles**: Super Admin, Administrator, Editor.

### Media
**Base URL**: `/api/media/`

#### `GET /api/media/`
- **Description**: List media files.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author, Contributor, Subscriber.
- **Response**: List of Media objects.

#### `POST /api/media/`
- **Description**: Upload a media file. Max size 5MB.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author.
- **Request Body**:
  - `name` (string, required)
  - `file` (file, required)

#### `DELETE /api/media/{id}/`
- **Description**: Delete a media file.
- **Allowed Roles**: Super Admin, Administrator.

### Comments
**Base URL**: `/api/posts/{post_id}/comments/`

#### `GET /api/posts/{post_id}/comments/`
- **Description**: List comments for a specific post.
- **Allowed Roles**: Public (for published posts), Author (for own comments).
- **Response**: List of Comment objects.

#### `POST /api/posts/{post_id}/comments/`
- **Description**: Create a new comment on a post.
- **Allowed Roles**: Authenticated Users.
- **Request Body**:
  - `post` (integer, required)
  - `content` (string, required)
- **Response**: Created Comment object.

#### `GET /api/posts/{post_id}/comments/{id}/`
- **Description**: Retrieve comment details.
- **Allowed Roles**: Public (Anyone).

#### `PUT /api/posts/{post_id}/comments/{id}/`
- **Description**: Update a comment.
- **Allowed Roles**: Author (Own comments only).

#### `DELETE /api/posts/{post_id}/comments/{id}/`
- **Description**: Delete a comment.
- **Allowed Roles**: Super Admin, Administrator, Editor, Author (Own comments only).

---

## 3. System
### Plugins
**Base URL**: `/api/plugins/`

#### `GET /api/plugins/`
- **Description**: List plugins.
- **Allowed Roles**: Super Admin, Administrator.

#### `POST /api/plugins/`
- **Description**: Add a plugin.
- **Allowed Roles**: Super Admin (Only).
- **Request Body**:
  - `name` (string)
  - `version` (string)
  - `settings` (json)

#### `DELETE /api/plugins/{id}/`
- **Description**: Remove a plugin.
- **Allowed Roles**: Super Admin, Administrator.

---

## Data Models (Schemas)

### User
```json
{
  "url": "string (url)",
  "username": "string",
  "email": "string",
  "groups": ["string (url)"]
}
```

### Group
```json
{
  "url": "string (url)",
  "name": "string"
}
```

### Post
```json
{
  "id": "integer",
  "title": "string",
  "content": "string",
  "author": "string (url)",
  "author_username": "string (read-only)",
  "status": "string ('draft', 'publish', 'private')",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Page
```json
{
  "id": "integer",
  "title": "string",
  "content": "string",
  "author": "string (url)",
  "author_username": "string (read-only)",
  "status": "string",
  "created_at": "datetime"
}
```

### Media
```json
{
  "id": "integer",
  "name": "string",
  "file": "string (url)",
  "author": "string (url)",
  "author_username": "string (read-only)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Comment
```json
{
  "id": "integer",
  "post": "integer",
  "author": "integer (user id)",
  "author_username": "string (read-only)",
  "content": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Plugin
```json
{
  "id": "integer",
  "name": "string",
  "version": "string",
  "is_active": "boolean",
  "settings": "json"
}
```
