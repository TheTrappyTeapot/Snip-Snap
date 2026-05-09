searchAutocomplete.js - Search Autocomplete Component
===================================================

**Purpose**: Real-time search suggestions with autocomplete dropdown.

**What it does**:

- Provides search suggestions as user types
- Manages dropdown list of suggestions
- Handles keyboard navigation (arrow keys, enter)
- Makes API calls for search results
- Highlights matching text
- Debounces API calls for performance
- Manages focus and blur events

**How to use**:

Include in page::

    <script src="{{ url_for('static', filename='js/components/searchAutocomplete.js') }}"></script>

Initialize autocomplete::

    const search = new SearchAutocomplete('searchInput', {
        endpoint: '/api/search',
        debounceMs: 300,
        minChars: 2
    });
    search.onSelect((result) => goToResult(result));

**Key Functions**:

- ``SearchAutocomplete(inputId, options)``: Initialize
- ``search(query)``: Trigger search
- ``setResults(results)``: Update suggestions
- ``selectResult(index)``: Select a suggestion
- ``clearResults()``: Hide dropdown
- ``navigateDown()``: Arrow down
- ``navigateUp()``: Arrow up

**Features**:

- Real-time suggestions
- Keyboard navigation
- Debounced API calls
- Highlight matches
- Click or Enter to select
- Escape to close
- Loading indicator
- "No results" message

The script in app/static/js/components/searchAutocomplete.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/searchAutocomplete.js` provides frontend browser behavior. Function responsibilities: `normalise` normalizes input values; `isValidItem` checks whether valid item; `createEl` creates DOM element; `createSearchBarAutocomplete` creates search bar autocomplete; `open` opens the UI panel; `close` closes the UI panel; `setHighlight` sets highlight; `renderNoResults` renders no results; `renderResults` renders results; `filterItems` filters items list; `selectItem` selects item; `refresh` refreshes UI state.