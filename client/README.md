# Watchlist Web client

This directory contains the client for Watchlist Web API. To run the client, you need `node` installed on your system.

## Installing

Run `npm install` in this directory to install all dependencies.

## Running

You need to have the API server running before starting the client, so that the client can fetch data from the API. See main [README](../README.md#running) for steps to run it.

Run `npm run dev` to run the dev server. The client app is then available in [`http://localhost:5173`](http://localhost:5173)

## Linting

The project is configured with ESLint. You can lint it by running `npm run lint` in the root folder of the project.

## Container

The client can be run as a Docker container. Image is available at [https://hub.docker.com/r/ekelhala/pwp-client](https://hub.docker.com/r/ekelhala/pwp-client)
