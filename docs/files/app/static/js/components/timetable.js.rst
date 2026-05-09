timetable.js - Schedule/Timetable Component
==========================================

**Purpose**: Manage and display barbershop working hours schedule.

**What it does**:

- Displays weekly schedule grid
- Manages open/closed hours
- Handles schedule editing
- Manages break times
- Validates time ranges
- Saves to API
- Shows current time indicator
- Handles timezone considerations

**How to use**:

Include in dashboard::

    <script src="{{ url_for('static', filename='js/components/timetable.js') }}"></script>

Initialize schedule::

    const schedule = new Timetable('scheduleContainer', barberId);
    schedule.load();
    schedule.enableEdit(true);

**Key Functions**:

- ``Timetable(container, barberId)``: Initialize
- ``load()``: Fetch schedule from API
- ``render()``: Display schedule
- ``editSlot(day, time)``: Edit time slot
- ``setHours(day, open, close)``: Set day hours
- ``addBreak(day, start, end)``: Add break time
- ``save()``: Save changes to API
- ``validate()``: Check validity

**API Endpoints**:

- ``GET /api/schedule/<barber_id>``: Get schedule
- ``PUT /api/schedule``: Update schedule

**Features**:

- 7-day week view
- Open/closed status
- Break time support
- Time range validation
- Current time highlight
- Edit mode
- Timezone handling

The script in app/static/js/components/timetable.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/timetable.js` provides frontend browser behavior.