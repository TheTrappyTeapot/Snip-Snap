(function () {
  "use strict";

  const DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  function makePill(shift) {
    var pill = document.createElement("span");
    pill.className = "timetable-shift-pill";
    pill.dataset.shiftId = shift.shift_id;

    var label = document.createTextNode(shift.start_time + "\u2013" + shift.end_time + " ");
    pill.appendChild(label);

    var btn = document.createElement("button");
    btn.className = "timetable-remove-btn";
    btn.title = "Remove";
    btn.textContent = "\u00d7";
    btn.dataset.shiftId = shift.shift_id;
    pill.appendChild(btn);

    return pill;
  }

  function bindRemoveBtn(btn) {
    btn.addEventListener("click", function () {
      var shiftId = parseInt(btn.dataset.shiftId, 10);
      var pill = btn.closest(".timetable-shift-pill");

      fetch("/api/shifts/" + shiftId, { method: "DELETE" })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.ok && pill) pill.remove();
        })
        .catch(function () {});
    });
  }

  // Wire up existing remove buttons
  document.querySelectorAll(".timetable-remove-btn").forEach(bindRemoveBtn);

  // Add shift
  var addBtn = document.getElementById("add-shift-btn");
  var shiftDay = document.getElementById("shift-day");
  var shiftStart = document.getElementById("shift-start");
  var shiftEnd = document.getElementById("shift-end");
  var shiftError = document.getElementById("shift-error");

  if (addBtn) {
    addBtn.addEventListener("click", function () {
      shiftError.textContent = "";
      var day = parseInt(shiftDay.value, 10);
      var start = shiftStart.value;
      var end = shiftEnd.value;

      if (!start || !end) {
        shiftError.textContent = "Please enter start and end times.";
        return;
      }
      if (start >= end) {
        shiftError.textContent = "Start time must be before end time.";
        return;
      }

      addBtn.disabled = true;

      fetch("/api/shifts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ day_of_week: day, start_time: start, end_time: end }),
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.ok) {
            var container = document.getElementById("shifts-day-" + day);
            if (container) {
              var pill = makePill({ shift_id: data.shift_id, start_time: start, end_time: end });
              bindRemoveBtn(pill.querySelector(".timetable-remove-btn"));
              container.appendChild(pill);
            }
            shiftStart.value = "";
            shiftEnd.value = "";
          } else {
            shiftError.textContent = data.error || "Could not add shift.";
          }
        })
        .catch(function () {
          shiftError.textContent = "Network error. Please try again.";
        })
        .finally(function () {
          addBtn.disabled = false;
        });
    });
  }
})();
