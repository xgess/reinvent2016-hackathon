api_schema = {
    "swagger": "2.0",
    "info": {
        "version": "1.0.0",
        "title": "Saving Animals"
    },
    "paths": {
        "/poaching": {
            "get": {
                "summary": "Get a bunch of data about poaching",
                "description": "This has all the data about poaching.\n",
                "parameters": [
                    {
                        "name": "start_date",
                        "in": "query",
                        "description": "Start Range for Data",
                        "required": False,
                        "type": "string",
                        "format": "datetime"
                    },
                    {
                        "name": "end_date",
                        "in": "query",
                        "description": "End Range for Data",
                        "required": False,
                        "type": "string",
                        "format": "datetime"
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "description": "Max number of elements to return. Defaults to 1000.",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "categories",
                        "in": "query",
                        "description": "UUID of a location to filter on",
                        "required": True,
                        "enum": ['weapons', 'weapons_seized', 'poacher_encounters', 'wildlife', 'people_observed', 'hunting_camp', 'patrol_observation'],
                        "type": "string"
                    }
                ]
            }
        },
        "/human_activity": {
            "get": {
                "summary": "Get a bunch of data about human activity",
                "description": "This has all the data about human activity.\n",
                "parameters": [
                    {
                        "name": "start_date",
                        "in": "query",
                        "description": "Start Range for Data",
                        "required": False,
                        "type": "string",
                        "format": "datetime"
                    },
                    {
                        "name": "end_date",
                        "in": "query",
                        "description": "End Range for Data",
                        "required": False,
                        "type": "string",
                        "format": "datetime"
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "description": "Max number of elements to return. Defaults to 1000.",
                        "required": True,
                        "type": "integer"
                    }
                ]
            }
        }
    }
}
