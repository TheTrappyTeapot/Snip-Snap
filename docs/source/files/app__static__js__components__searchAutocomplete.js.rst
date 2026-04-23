app/static/js/components/searchAutocomplete.js
==============================================

Overview
--------

The script in app/static/js/components/searchAutocomplete.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/searchAutocomplete.js` provides frontend browser behavior. Function responsibilities: `normalise` normalizes input values; `isValidItem` checks whether valid item; `createEl` creates DOM element; `createSearchBarAutocomplete` creates search bar autocomplete; `open` opens the UI panel; `close` closes the UI panel; `setHighlight` sets highlight; `renderNoResults` renders no results; `renderResults` renders results; `filterItems` filters items list; `selectItem` selects item; `refresh` refreshes UI state.