Great idea. This is exactly how you avoid every colleague’s AI reinventing (and breaking) your architecture.

Below is a **ready-to-paste `AI-README.md`** written **for AI tools**, not humans.
It is explicit, directive, and constraint-based — so their ChatGPT behaves like a junior dev who’s already onboarded.

---

# AI-README.md

**(Instructions for AI assistants working on this repository)**

## Purpose of this file

This file explains the **project architecture, constraints, and conventions** so that any AI assistant (e.g. ChatGPT) used by contributors can immediately generate **compatible, non-destructive code**.

AI assistants **must follow this document** when suggesting or generating code.

---

## Tech stack

* **Backend**: Flask (Python)
* **Frontend**: HTML (Jinja templates), CSS, vanilla JavaScript
* **Database**: PostgreSQL
* **No frontend frameworks** (no React, Vue, etc.)
* **No ORMs yet** (raw SQL via a DB layer)

---

## High-level architecture (DO NOT VIOLATE)

The app is deliberately layered:

```
Routes (Flask)
   ↓
Database layer (SQL, connections)
   ↓
Templates (HTML structure)
   ↓
Static assets (CSS / JS behaviour)
```

### Absolute rules

* ❌ **No SQL inside Flask route functions**
* ❌ **No database access from templates or JS**
* ❌ **No HTML generation inside JavaScript**
* ❌ **No secrets or credentials in JS or committed files**
* ❌ **No changes to file structure without agreement**

---

## Folder structure (authoritative)

```
app/
  app.py                # Flask entry point and routes ONLY
  db/
    connection.py       # Database connection logic only
    queries.py          # SQL queries only (no Flask)
  templates/
    base.html           # Shared layout
    *.html              # Page templates (extend base.html)
  static/
    css/
      main.css
      components/
        searchAutocomplete.css
    js/
      components/
        searchAutocomplete.js
      pages/
        discover.js
```

---

## Flask (`app/app.py`)

### Responsibilities

* Define routes
* Call database query functions
* Pass data to templates

### Forbidden

* Writing SQL
* Business logic
* HTML generation

**Correct pattern:**

```python
data = get_something_from_db()
return render_template("page.html", data=data)
```

---

## Templates (`app/templates/`)

### Rules

* Use **Jinja inheritance**
* Pages must extend `base.html`
* Templates define **structure only**

### Forbidden

* Database access
* Complex logic
* Fetch calls

**Correct pattern:**

```html
{% extends "base.html" %}
{% block content %}
  <h1>Page</h1>
{% endblock %}
```

---

## JavaScript architecture

### Component JS (`static/js/components/`)

Reusable, page-agnostic logic.

Example:

* `searchAutocomplete.js`

**Rules**

* No page-specific logic
* No assumptions about backend
* Communicate via callbacks only

---

### Page manager JS (`static/js/pages/`)

One file per page.

**Responsibilities**

* Initialise components
* Own page-specific behaviour
* Handle callbacks from components

**Example**

```js
createSearchBarAutocomplete(
  mountElement,
  onSelectHandler,
  items
);
```

---

## Shared autocomplete component (CRITICAL)

### Authoritative behaviour

The search autocomplete component:

* Accepts items with shape:

```js
{
  id: number,          // Database PK
  type: "tag" | "barber" | "barbershop",  // Table name
  label: string        // Display name
}
```

* Matching:

  * Case-insensitive
  * "contains"
  * Minimum 1 character
  * Limit 6 results

* UI:

  * Icon per type
  * Dropdown closes on:

    * selection
    * ESC
    * click outside

* Callback:

```js
onSelect(selectedItemObject)
```

### Forbidden

* Modifying component behaviour without discussion
* Hardcoding page logic inside the component

---

## Database layer (`app/db/`)

### `connection.py`

* Reads DB config from environment variables
* Opens/closes connections

### `queries.py`

* Contains **only SQL and query functions**
* Returns plain Python data

### Forbidden

* Flask imports
* Template rendering
* JS-style logic

---

## Environment & secrets

* Use `.env` for:

  * DB credentials
* `.env` is gitignored
* AI must **never** suggest committing secrets

---

## Git & workflow rules

* Feature branches only
* No direct commits to `main`
* One logical change per commit
* Respect existing file structure

---

## When unsure

If an AI assistant is unsure where code belongs:

1. **Do not guess**
2. Ask the human developer
3. Default to **non-destructive suggestions**

---

## Summary for AI assistants

* This is a **layered Flask app**
* Keep responsibilities clean
* Reuse existing components
* Never bypass the DB layer
* Never invent structure

If you follow this file, your output will integrate cleanly.

---

If you want, next I can:

* add a **PR template for humans + AI**
* add a **DB schema contract for AI**
* add an **“allowed changes” checklist for AI**

Just say the word.
