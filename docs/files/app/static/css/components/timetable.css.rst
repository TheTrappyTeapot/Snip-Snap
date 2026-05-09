timetable.css - Timetable/Schedule Component Styles
==================================================

**Purpose**: Styles for displaying and managing working hours schedule.

**What it styles**:

- Timetable grid layout (days × hours)
- Time slot cells
- Open/closed hours styling
- Timetable header (days of week)
- Time labels (hours)
- Highlight current time
- Edit mode styles

**How to use**:

Include in CSS::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/timetable.css') }}">

HTML structure::

    <table class="timetable">
        <thead>
            <tr><th>Mon</th><th>Tue</th><th>Wed</th></tr>
        </thead>
        <tbody>
            <tr>
                <td class="slot-open">09:00-17:00</td>
                <td class="slot-closed">Closed</td>
            </tr>
        </tbody>
    </table>

**Key CSS Classes**:

- ``.timetable``: Main table
- ``.slot-open``: Open hours cell
- ``.slot-closed``: Closed cell
- ``.slot-current``: Current time highlight
- ``.timetable-edit``: Edit mode styles

**Features**:

- Day-by-day view
- Hour ranges for each day
- Open/closed status
- Current time indicator
- Edit mode for barbers
- Break time display

app/static/css/components/timetable.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the timetable component. It styles selectors such as .barber-profile__section, .barber-profile__title, .hour-row, and .barber-profile__timetable.
