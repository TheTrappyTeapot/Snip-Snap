/**
 * Renders a timetable/schedule widget
 * @param {string} selector - CSS selector for the mount point
 * @param {object} config - Configuration object
 * @param {string} config.title - Title for the timetable section
 * @param {object} config.schedule - Schedule data (object with day_num as key)
 * @param {array} config.dayLabels - Array of day names (Monday-Sunday)
 * @param {number} config.currentDay - Current day number (0-6)
 * @param {object} config.closingInfo - Object with closing_soon and mins_until_close
 * @param {string} config.cssPrefix - BEM class prefix (e.g., 'barbershop__' or 'barber-profile__')
 * @param {string} config.scheduleType - Type of schedule: 'opening_hours' or 'shifts'
 */
export function renderTimetable(selector, config) {
  const {
    title,
    schedule,
    dayLabels,
    currentDay,
    closingInfo,
    cssPrefix,
    scheduleType = 'opening_hours'
  } = config;

  const element = document.querySelector(selector);
  if (!element) {
    console.warn(`Timetable: element not found for selector "${selector}"`);
    return;
  }

  const classList = `${cssPrefix}timetable`;
  const section = document.createElement('section');
  section.className = `${cssPrefix}section`;

  const titleEl = document.createElement('h3');
  titleEl.className = `${cssPrefix}title`;
  titleEl.textContent = title;
  section.appendChild(titleEl);

  const timetableDiv = document.createElement('div');
  timetableDiv.className = classList;

  for (let dayNum = 0; dayNum < 7; dayNum++) {
    const isClosed = !(dayNum in schedule);
    const isCurrentDay = dayNum === currentDay;
    const isClosingSoon = isCurrentDay && closingInfo && closingInfo.closing_soon;
    const shouldHighlight = isCurrentDay && (isClosed || isClosingSoon);
    
    const rowDiv = document.createElement('div');
    const rowClass = scheduleType === 'shifts' ? `${cssPrefix}row` : `hour-row`;
    rowDiv.className = shouldHighlight ? `${rowClass} ${rowClass}--closing-soon` : rowClass;

    // Day label
    const dayDiv = document.createElement('div');
    const dayClass = scheduleType === 'shifts' ? `${cssPrefix}day` : `hour-day`;
    dayDiv.className = dayClass;
    dayDiv.textContent = dayLabels[dayNum];
    rowDiv.appendChild(dayDiv);

    // Times
    const timesDiv = document.createElement('div');
    const timesClass = scheduleType === 'shifts' ? `${cssPrefix}times` : `hour-times`;
    timesDiv.className = timesClass;

    if (!isClosed) {
      if (scheduleType === 'shifts') {
        // Handle shifts array format
        const shifts = schedule[dayNum];
        shifts.forEach(shift => {
          const timeBlock = document.createElement('div');
          timeBlock.className = `${cssPrefix}time-block`;
          timeBlock.textContent = `${shift.start_time} - ${shift.end_time}`;
          timesDiv.appendChild(timeBlock);
        });
      } else {
        // Handle opening hours format
        const hours = schedule[dayNum];
        const timeBlock = document.createElement('div');
        timeBlock.className = 'hour-time-block';
        timeBlock.textContent = `${hours.open} - ${hours.close}`;
        timesDiv.appendChild(timeBlock);
      }
    } else {
      const closedDiv = document.createElement('div');
      const closedClass = scheduleType === 'shifts' ? `${cssPrefix}closed` : `hour-closed`;
      closedDiv.className = closedClass;
      closedDiv.textContent = 'Closed';
      timesDiv.appendChild(closedDiv);
    }

    // Add closing indicator if closing within 2 hours
    if (isCurrentDay && isClosingSoon && closingInfo.mins_until_close <= 120) {
      const indicatorDiv = document.createElement('div');
      const indicatorClass = scheduleType === 'shifts' ? `${cssPrefix}closing-indicator` : `hour-closing-indicator`;
      indicatorDiv.className = indicatorClass;
      indicatorDiv.textContent = `Closing in ${closingInfo.mins_until_close} min`;
      timesDiv.appendChild(indicatorDiv);
    }

    rowDiv.appendChild(timesDiv);

    timetableDiv.appendChild(rowDiv);
  }

  section.appendChild(timetableDiv);
  element.replaceWith(section);
}
