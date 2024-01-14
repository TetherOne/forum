

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
            }
        },

        "/api/articles/{article_id}": {
            "get": {
                "summary": "Get article by ID",
                "description": "Returns a article with the given ID",
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
            }
        }
    }
}



