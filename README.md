# PWP SPRING 2025
# WatchList Web API
# Group information
* Student 1. Aleksanteri Kylmäaho  aleksanteri.kylmaaho@student.oulu.fi
* Student 2. Joonas Kelloniemi niko.kelloniemi@student.oulu.fi
* Student 3. Emil Kelhälä emil.kelhala@student.oulu.fi
* Student 4. Tomi Nikula tomi.nikula@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

# MongoDB 8.0.4 setup and population

After cloning repo
- .env file is needed in the root where MONGODB_CONNECTION_STRING="pointing_to_MongoDB_Atlas_project" is defined. 

- pip install -r requirements.txt

- running mockdata.py initializes the database and populates it (database needs to be empty for this)

- After running mockdata.py, data can be visually inspected from MongoDB Atlas project (needs access)

# Running

Due to the current setup of the project, the API can be run with the following command in folder `project_watchlist`: `flask --app __init__:create_app run` (`--debug` can be added to the end)

# Testing

To run the tests for the API, you should complete following steps:

1. Install the application by running `pip install -e .` in the root folder of the project
2. Move to the `tests`-folder
3. Run `pytest --cov-report term-missing --cov=project_watchlist`, the database gets populated automatically and cleaned up afterwards.

# To do:
- Unit test (ideas)
    - (run) Every endpoint with legit values
    - Error handling tests (invalid inputs, missing field)
    - Tests for database validation rules
