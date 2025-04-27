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

To run the API server, you can set the environment variable `FLASK_APP` to `project_watchlist`, and then execute command `flask run` in the root folder of the project.

```console
set FLASK_APP=project_watchlist
flask run
```

Another way of running the API is to use the command `flask --app=project_watchlist run` in the project root folder.

# Testing

To run the tests for the API, you should complete following steps:

1. Install the application by running `pip install -e .` in the root folder of the project
2. Move to the `tests`-folder
3. Run `pytest --cov-report term-missing --cov=project_watchlist`, the database gets populated automatically and cleaned up afterwards.

# Linting

You can run `pylint` for the API with the command `pylint project_watchlist` in the root folder of this project.

# Running and linting the client

Instructions for these can be found in the client's [README](./client/README.md)

# Deployment

The API and client can be deployed to Rahti by using the configurations provided in folder `deployment`.

The API server needs a secret for connecting to the MongoDB instance. In order to make this work, we need to use Kubernetes secrets. After putting the MongoDB connection string to `.env` file in project root directory, we can use the following command to create a secret that the deployment expects to have in order to connect to MongoDB:

`oc create secret generic watchlist-secrets --from-env-file .env`

Note! The connection string in `.env` should not be in quotes (e.g `" "`) otherwise the deployment fails.

After doing this, we can just create the deployment by running this command (assuming we are still in root folder):

`oc apply -f deployment/deployment.yml`

Done! The deployment should now be created. Our own deployment is running at [https://watchlists-pwp-course-webbipojat.2.rahtiapp.fi/](https://watchlists-pwp-course-webbipojat.2.rahtiapp.fi/)
