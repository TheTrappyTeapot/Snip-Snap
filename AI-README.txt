PURPOSE

This document defines exactly how code must be structured in this project.

Any AI assistant generating code for this repository MUST follow these rules.

This project uses a structured architecture with clear separation between:

Components

Features

Pages

Services (backend)

Do NOT invent new folder structures.
Do NOT move files unless instructed.
Do NOT mix frontend and backend responsibilities.

PROJECT STRUCTURE (AUTHORITATIVE)

app/
app.py
db/
services/
templates/
static/
css/
components/
features/
pages/
js/
components/
features/
pages/

ARCHITECTURE OVERVIEW

There are four layers in this application:

Components (Reusable UI pieces)

Features (Vertical application behaviour)

Pages (Feature composition)

Services (Backend feature logic)

Each layer has strict responsibilities.

COMPONENTS

Location:
static/js/components/
static/css/components/

Definition:
A component is a small, reusable frontend UI element.

Examples:

SearchBarAutocomplete

PhotoUploadInput

TagList

Modal

Button

Rules:

Components must be reusable.

Components must NOT contain business logic.

Components must NOT call backend routes directly.

Components must NOT know about Flask or the database.

Components communicate via callbacks or emitted events only.

Components manage only their own UI state.

Correct:
Component receives data and a callback function.
Component calls the callback when user interacts.

Incorrect:
Component performs fetch() to backend.
Component contains feature-level logic.
Component manipulates page-level layout.

FEATURES

Location:
static/js/features/
static/css/features/

Definition:
A feature is a vertical slice of application behaviour.

A feature:

Composes multiple components.

Owns interaction logic.

Communicates with the backend via fetch().

Manages feature-specific state.

Examples:

uploadPost

discoverSearch

followBarber

likePost

Rules:

A feature may use multiple components.

A feature handles form submission.

A feature may call backend routes using fetch().

A feature should be self-contained.

A feature must NOT contain database logic.

A feature must NOT render full pages.

Correct:
uploadPost.js imports PhotoUploadInput and TagList,
handles submission,
sends POST request to backend.

Incorrect:
Feature directly writes SQL.
Feature modifies unrelated page elements.

PAGES

Location:
static/js/pages/
static/css/pages/

Definition:
A page is responsible for composing features into a screen.

Pages:

Initialise features.

Connect DOM elements to features.

Contain minimal logic.

Rules:

Pages must NOT contain business logic.

Pages must NOT call the database.

Pages must NOT duplicate feature logic.

Pages should only initialise features.

Correct:
barber_dashboard.js initialises uploadPost feature.

Incorrect:
barber_dashboard.js contains image validation logic.

SERVICES (BACKEND)

Location:
app/services/

Definition:
A service file contains backend logic for a single feature.

Each feature should have one corresponding service file.

Example:
services/upload_post_service.py

Rules:

Services contain validation logic.

Services handle filesystem operations.

Services call database query functions.

Services return structured results.

Services must NOT render templates.

Services must NOT contain route decorators.

Services must NOT contain frontend code.

Correct:
Service validates image, saves file, calls create_haircut_post().

Incorrect:
Service returns HTML.
Service contains Flask route decorators.

ROUTES (app.py)

Routes must be thin.

Routes:

Receive request

Call service

Render template or return JSON

Routes must NOT:

Contain heavy validation logic

Contain file handling logic

Contain database logic

Correct:
result = handle_upload_post(request)

Incorrect:
Entire upload logic written inside route.

DATABASE LAYER (app/db/)

Rules:

Only SQL queries.

No Flask imports.

No template rendering.

No business logic.

STRICT SEPARATION RULES

Frontend (static/) and Backend (services/, db/) are completely separate environments.

Do NOT:

Import JavaScript into Python.

Import Python into JavaScript.

Put Python files inside static/.

Put JS inside services/.

HOW TO IMPLEMENT A NEW FEATURE

For a new feature named "exampleFeature":

Create frontend feature file:
static/js/features/exampleFeature.js

Create optional CSS:
static/css/features/exampleFeature.css

Create backend service:
services/example_feature_service.py

Add thin route in app.py:
route calls service only.

Page initialises feature.

TASK TYPES

This repository uses three task categories:

COMPONENT TASK

Build reusable UI element.

Must be reusable.

Must not include business logic.

FEATURE TASK

Full vertical behaviour.

Requires frontend feature file.

Requires backend service file.

May require DB query additions.

PAGE TASK

Compose features.

Initialise features.

Minimal logic only.

IF UNSURE

If unsure where code belongs:

UI reusable element → Component

User interaction + backend call → Feature

Backend validation or filesystem → Service

SQL query → db/queries.py

Route definition → app.py

Screen composition → Page

Never guess.
Follow this document.