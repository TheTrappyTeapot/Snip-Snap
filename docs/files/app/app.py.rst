app/app.py - Flask Application Factory
======================================

**Purpose**: Core Flask application initialization and configuration.

**What it does**:

This module creates and configures the Flask web application with all necessary settings, blueprints, and middleware. It loads environment variables from a `.env` file and registers all routes and API endpoints.

**Key Functions**:

- ``create_app()``: Factory function that creates the Flask app instance with all configurations
- Registers blueprints (API routes)
- Configures cache headers to prevent browser caching of sensitive data
- Sets up the SECRET_KEY from environment variables

**How to use**:

This is the entry point of the application. Import and run it with::

    from app.app import app
    app.run(debug=True)  # Run the development server

Or via command line::

    python -m app.app

**Key Components**:

- Routes are automatically registered via ``register_routes()``
- API endpoints are registered via Flask Blueprint ``api_bp``
- Cache headers prevent sensitive data from being stored in browser cache

Overview
--------

It loads environment configuration, initializes CORS support, and registers route and API modules. The create_app function is the factory used by local runs and deployment entry points. Running the module directly starts the Flask server for development.

Purpose
-------

This module in `app/app.py` provides backend application behavior. Function responsibilities: `create_app` creates Flask app instance.