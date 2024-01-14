swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Forum API",
        "version": "1.0"
    },
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Forum API",
        "version": "1.0"
    },
    "paths": {
        "/api/users": {
            "get": {
                "summary": "Get all users",
                "description": "Returns a list of all users",
                "responses": {
                    "404": {
                        "description": "No users found"
                    }
                }
            },
            "post": {
                "summary": "Create users",
                "description": "Creates one or more users",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/User"  # Reference to the User model definition
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Users registered successfully"
                    },
                    "400": {
                        "description": "Invalid data format. Expected a list of users."
                    }
                }
            }
        },
        "/api/users/{user_id}": {
            "get": {
                "summary": "Get user by ID",
                "description": "Returns a user with the given ID",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "type": "integer",
                        "required": True,
                        "description": "The ID of the user to retrieve"
                    }
                ],
                "responses": {
                    "404": {
                        "description": "User not found"
                    }
                }
            }
        },
        "/api/articles": {
            "get": {
                "summary": "Get all articles",
                "description": "Returns a list of all articles",
                "responses": {
                    "404": {
                        "description": "No articles found"
                    }
                }
            },
            "post": {
                "summary": "Create articles",
                "description": "Creates one or more articles",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Article"  # Reference to the Article model definition
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Articles created successfully"
                    },
                    "400": {
                        "description": "Invalid data format. Expected a list of articles."
                    }
                }
            }
        },
        "/api/articles/{article_id}": {
            "get": {
                "summary": "Get article by ID",
                "description": "Returns an article with the given ID",
                "parameters": [
                    {
                        "name": "article_id",
                        "in": "path",
                        "type": "integer",
                        "required": True,
                        "description": "The ID of the article to retrieve"
                    }
                ],
                "responses": {
                    "404": {
                        "description": "Article not found"
                    }
                }
            },
            "delete": {
                "summary": "Delete article",
                "description": "Deletes an article with the given ID",
                "parameters": [
                    {
                        "name": "article_id",
                        "in": "path",
                        "type": "integer",
                        "required": True,
                        "description": "The ID of the article to delete"
                    }
                ],
                "responses": {
                    "404": {
                        "description": "Article not found"
                    }
                }
            }
        }
    },
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["username", "email", "password"]
        },
        "Article": {
            "type": "object",
            "properties": {
                "name_of_article": {"type": "string"},
                "text_of_article": {"type": "string"},
                "category": {"type": "string"},
                "user_id": {"type": "integer"},
            },
            "required": ["name_of_article", "ext_of_article", "category", "user_id"]
        }
    }
}
