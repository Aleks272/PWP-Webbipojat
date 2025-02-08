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

- After running mockdata.py, data can be visually inspected from MongoDB Atlas project (need access)
