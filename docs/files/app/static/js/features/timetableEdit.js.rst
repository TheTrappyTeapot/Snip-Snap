timetableEdit.js - Schedule Editing Feature
==========================================

**Purpose**: Feature for editing barbershop working hours schedule.

**What it does**:

- Manages schedule editing interface
- Validates time ranges
- Handles break time management
- Manages day-off settings
- Syncs with timetable component
- Saves to backend
- Shows changes preview
- Handles timezone considerations

**How to use**:

Initialize in dashboard::

    const scheduleEditor = new TimetableEditFeature('scheduleContainer', barberId);
    scheduleEditor.load();
    scheduleEditor.onSave(() => showSuccess());

**Key Functions**:

- ``TimetableEditFeature(container, barberId)``: Initialize
- ``load()``: Fetch current schedule
- ``editDay(day)``: Edit specific day
- ``setHours(day, open, close)``: Set opening hours
- ``addBreak(day, start, end)``: Add break time
- ``removeBreak(day, breakId)``: Remove break
- ``setDayOff(day)``: Mark day as closed
- ``save()``: Persist changes

**Validation**:

- Open time before close time
- No overlapping breaks
- Valid time format
- Break within open hours

**API Endpoints**:

- ``GET /api/schedule/<barber_id>``: Get schedule
- ``PUT /api/schedule``: Save changes

**Features**:

- 7-day schedule view
- Set hours per day
- Add/remove breaks
- Mark days off
- Time validation
- Preview changes

The script in app/static/js/features/timetableEdit.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/shifts/ and /api/shifts to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/timetableEdit.js` provides frontend browser behavior. Function responsibilities: `makePill` creates the timetable shift-pill DOM element with time text and remove button metadata; `bindRemoveBtn` attaches the delete API call and removes the matching shift pill after a successful response.
