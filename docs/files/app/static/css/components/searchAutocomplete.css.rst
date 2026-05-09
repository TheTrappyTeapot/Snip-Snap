searchAutocomplete.css - Search Autocomplete Styles
==================================================

**Purpose**: Styles for search input with dropdown suggestions/autocomplete.

**What it styles**:

- Search input field styling
- Dropdown suggestion list
- Highlighted matching text
- Search result items
- Loading indicator
- No results message

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/searchAutocomplete.css') }}">

HTML structure::

    <div class="search-autocomplete">
        <input type="text" class="search-input" placeholder="Search..." />
        <div class="autocomplete-dropdown">
            <div class="autocomplete-item">Result 1</div>
            <div class="autocomplete-item">Result 2</div>
        </div>
    </div>

**Key CSS Classes**:

- ``.search-autocomplete``: Container
- ``.search-input``: Input field
- ``.autocomplete-dropdown``: Suggestion list
- ``.autocomplete-item``: Individual suggestion
- ``.autocomplete-item.active``: Highlighted item
- ``.loading``: Loading state

**Features**:

- Real-time suggestions
- Keyboard navigation (arrow keys, enter)
- Highlight matching text
- Loading spinner
- Click or Enter to select
- Escape to close dropdown

app/static/css/components/searchAutocomplete.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the searchAutocomplete component. It styles selectors such as .sa-root, .sa-field, .sa-input, and .sa-input:focus.
