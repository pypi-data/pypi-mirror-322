/*
 * potluck.js
 *
 * Javascript support for common potluck server active elements like
 * timers.
 *
 * Must be included as a module and/or with defer.
 */

// jshint esversion: 6
/* global window, document, console, IntersectionObserver */
/* jshint -W097 */
/* jshint -W014 */
/* jshint -W080 */
/* jshint -W040 */

"use strict";

/*--------*
 * Timers *
 *--------*/

// Duration constants in seconds
var ONE_MINUTE = 60;
var ONE_HOUR = 60 * ONE_MINUTE;
var ONE_DAY = 24 * ONE_HOUR;
var ONE_WEEK = 7 * ONE_DAY;

// Milliseconds between timer updates. Timer inaccuracy will be no more
// than half of this value on average.
var TICK_INTERVAL = 500;

function fuzzy_time(seconds) {
    // Converts a number of seconds into a fuzzy time string that rounds
    // to the largest unit (minutes/hours/days/weeks). Ignores the sign
    // of the argument.
    if (seconds < 0) {
        seconds = -seconds;
    }

    // Compute time remaining
    let weeks = seconds / ONE_WEEK;
    let days = (seconds % ONE_WEEK) / ONE_DAY;
    let hours = (seconds % ONE_DAY) / ONE_HOUR;
    let minutes = Math.floor((seconds % ONE_HOUR) / ONE_MINUTE);
    seconds = Math.floor(seconds % ONE_MINUTE);

    if (Math.floor(weeks) > 1) {
        if (weeks % 1 > 0.75) {
            return "almost " + Math.ceil(weeks) + " weeks";
        } else {
            return Math.floor(weeks) + " weeks";
        }
    } else if (Math.floor(weeks) == 1) {
        return Math.floor(7 + days) + " days";
    } else if (Math.floor(days) > 1) {
        if (days % 1 > 0.75) {
            return "almost " + Math.ceil(days) + " days";
        } else {
            return Math.floor(days) + " days";
        }
    } else if (Math.floor(days) == 1) {
        return Math.floor(24 + hours) + " hours";
    } else if (hours > 4) {
        if (hours % 1 > 0.75) {
            return "almost " + Math.ceil(hours) + " hours";
        } else {
            return Math.floor(hours) + " hours";
        }
    } else if (Math.floor(hours) > 0) {
        return Math.floor(hours) + "h " + minutes + "m";
    } else if (minutes > 30) {
        return minutes + " minutes";
    } else if (minutes > 0) {
        let s_str = "" + seconds;
        if (s_str.length == 1) {
            s_str = "0" + s_str;
        }
        return minutes + "m " + s_str + "s";
    } else {
        return seconds + " seconds";
    }
}

// Active countdown timers support
function tick_timer(timer) {
    // Updates the data-time attribute of a countdown timer, and updates
    // the contents of the timer element to display the remaining (or
    // exceeded, if negative) time in appropriate units.

    // Compute new seconds-remaining
    let now = new Date();
    let elapsed_ms = now - timer.last_tick;
    timer.seconds -= elapsed_ms / 1000;
    timer.last_tick = now;

    // Update display
    if (timer.seconds > 0) {
        timer.innerHTML = "(" + fuzzy_time(timer.seconds) + " from&nbsp;now)";
    } else {
        timer.innerHTML = "(" + fuzzy_time(timer.seconds) + " ago)";
    }

    // Reschedule ourselves
    window.setTimeout(tick_timer, TICK_INTERVAL, timer);
}

// Set up callbacks for timers
for (let timer of document.querySelectorAll(".timer")) {
    let seconds = timer.getAttribute("data-time");
    if (seconds == null) {
        continue; // ignore this element
    }
    let seconds_float = parseFloat(seconds);
    if (isNaN(seconds_float)) {
        console.warn(
            "Invalid data-time attribute for a .timer:",
            timer,
            seconds
        );
        continue; // can't process this element
    }
    timer.seconds = seconds_float;
    timer.last_tick = new Date();
    timer.setAttribute("role", "timer"); // ensure ARIA attributes are set
    timer.setAttribute("aria-live", "off");
    tick_timer(timer);
}

/*------------*
 * Validation *
 *------------*/

function validate_task_submit(task_form) {
    // Takes a task form DOM element and runs validation to
    // disable/enable the submit button and add/remove relevant messages.

    let prid = task_form.getAttribute("data-project");
    let taskid = task_form.getAttribute("data-task");

    let file_browser = task_form.querySelector('input[name="upload"]');
    let time_spent = task_form.querySelector('input[name="time_spent"]');
    let submit_button = task_form.querySelector('input[type="submit"]');

    // If validation is disabled via the global checkbox, or if this task
    // is finalized, skip validation, remove messages, and enable the
    // upload button.
    let task_item = task_form.parentElement.parentElement;
    let project_item = task_item.parentElement.parentElement;

    let unsubmitted = task_item.classList.contains("unsubmitted");

    let validation_control = document.getElementById("enable_validation");
    if (
        validation_control == null
     || !validation_control.checked
     || project_item.classList.contains("status-final")
    ) {
        set_validation_messages(task_form, {});
        submit_button.removeAttribute("disabled");
        submit_button.classList.remove("invalid");
        file_browser.removeAttribute("aria-describedby");
        time_spent.removeAttribute("aria-describedby");
        return;
    }

    let filename_label = task_form.querySelectorAll('label')[0];
    let task_filename = filename_label.firstElementChild.innerText.trim();

    // Build an mapping from topics to messages
    let messages = {};

    // Validate the filename
    let current_filename = undefined;
    if (file_browser.files.length > 0) {
        current_filename = file_browser.files[0].name;
    }

    if (current_filename == undefined) {
        current_filename = file_browser.value.split('\\').pop();
    }

    if (current_filename != task_filename) {
        if (unsubmitted) {
            messages.filename = (
                "You must select a file named <code>" + task_filename
              + "</code>"
            );
        } else {
            messages.filename = (
                "To resubmit, select a file named <code>" + task_filename
              + "</code>"
            );
        }
    }

    // Validate the time spent field
    let spent = time_spent.value;

    if (spent == "") {
        if (unsubmitted) {
            messages.time_spent = "You must estimate your time spent.";
        } else {
            messages.time_spent = "To resubmit, estimate your time spent.";
        }
    } else if (isNaN(parseFloat(spent))) {
        messages.time_spent = (
            "Please enter a decimal number of hours (like '0.3', '2', or"
          + " '3.5') for time spent."
        );
    }

    // Set the validation messages
    set_validation_messages(task_form, messages);

    // Enable/disable the upload button
    let file_desc_id = prid + '-' + taskid + '-filename';
    let time_desc_id = prid + '-' + taskid + '-time_spent';
    if (Object.keys(messages).length > 0) {
        submit_button.setAttribute("disabled", true);
        submit_button.classList.add("invalid");
        file_browser.setAttribute("aria-describedby",file_desc_id);
        time_spent.setAttribute("aria-describedby", time_desc_id);
    } else {
        submit_button.removeAttribute("disabled");
        submit_button.classList.remove("invalid");
        file_browser.removeAttribute("aria-describedby");
        time_spent.removeAttribute("aria-describedby");
    }
}

function set_validation_messages(task_form, messages) {
    // Removes any old validation messages for a form and adds new ones.
    // Messages should be a mapping from topics to HTML message strings.

    let prid = task_form.getAttribute("data-project");
    let taskid = task_form.getAttribute("data-task");

    let task_item = task_form.parentElement.parentElement;
    let msg_list = task_item.querySelector("ul.messages");

    // Return if there's no message list
    if (msg_list == null) { return; }

    // Remove all old validation messages
    for (let vmsg of msg_list.querySelectorAll("li.validation")) {
        msg_list.removeChild(vmsg);
    }

    // Create and append new validation messages
    for (let msg_topic of Object.keys(messages)) {
        let msg = document.createElement("li");
        msg.classList.add("validation");
        msg.classList.add("topic-" + msg_topic);
        msg.setAttribute("id", prid + '-' + taskid + '-' + msg_topic);
        msg.innerHTML = messages[msg_topic];
        msg_list.appendChild(msg);
    }
}

// Set up form validation
for (let task_form of document.querySelectorAll("form.task_submit")) {
    // Initial validation
    validate_task_submit(task_form);

    for (let input of task_form.querySelectorAll("input")) {
        input.addEventListener(
            "change",
            // jshint -W083
            // task_form is safely per-iteration because it's a for/of
            function () { validate_task_submit(task_form); }
            // jshint +W083
        );
        input.addEventListener(
            "keyup",
            // jshint -W083
            // task_form is safely per-iteration because it's a for/of
            function () { validate_task_submit(task_form); }
            // jshint +W083
        );
    }
}

let validation_switch = document.getElementById("enable_validation");
if (validation_switch != null) {
    validation_switch.addEventListener(
        "change",
        function () {
            // re-validate every task
            for (
                let task_form
             of document.querySelectorAll("form.task_submit")
            ) {
                validate_task_submit(task_form);
            }
        }
    );
}

/*----------------------*
 * Extension Management *
 *----------------------*/

/*
 * Adds 24 to the numeric value of a text input with a certain ID. Emits
 * a warning if the value isn't numeric or the input can't be found.
 */
function add24(id) {
    let target = document.getElementById(id);
    if (target == undefined) {
        console.warn("Can't add 24 to nonexistent element '" + id + "'.");
        return;
    }
    let old = parseFloat(target.value);
    if (isNaN(old)) {
        console.warn(
            "Can't add 24 to non-numeric value '" + target.value + "'."
        );
        return;
    }
    target.value = "" + (old + 24);
}

/*
 * Like add24 but subtracts. Doesn't subtract below 0.
 */
function subtract24(id) {
    let target = document.getElementById(id);
    if (target == undefined) {
        console.warn(
            "Can't subtract 24 from nonexistent element '" + id + "'."
        );
        return;
    }
    let old = parseFloat(target.value);
    if (isNaN(old)) {
        console.warn(
            "Can't subtract 24 from non-numeric value '" + target.value + "'."
        );
        return;
    }
    target.value = "" + Math.max(0, (old - 24));
}

/* Attach add/subtract 24 to the appropriate buttons */
for (let button of document.querySelectorAll("input.add24")) {
    button.addEventListener("click", function () {
        add24(this.getAttribute("data-target"));
    });
}

for (let button of document.querySelectorAll("input.subtract24")) {
    button.addEventListener("click", function () {
        subtract24(this.getAttribute("data-target"));
    });
}

/*-----------------------*
 * Gradesheet management *
 *-----------------------*/

/*
 * Given an HTML table element, returns a string representing the table's
 * contents as TSV data. If table cells contain tab characters, the
 * formatting will be thrown off. For cells that span multiple columns,
 * their contents are placed into the first column they span and the
 * others are left empty.
 */
function renderTable(tableElement) {
    let result = "";
    for (let part of tableElement.children) {
        let tag = part.tagName.toLowerCase();
        if (tag == "thead" || tag == "tbody" || tag == "tfoot") {
            for (let row of part.children) {
                let rTag = row.tagName.toLowerCase();
                if (rTag == "tr") {
                    let rowRepr = "";
                    for (let cell of row.children) {
                        let cTag = cell.tagName.toLowerCase();
                        if (cTag == "th" || cTag == "td") {
                            rowRepr += cell.innerText;
                            for (let i = 0; i < cell.colSpan; ++i) {
                                rowRepr += "\t";
                            }
                        }
                    }
                    // Slice off last tab character
                    rowRepr = rowRepr.slice(rowRepr, rowRepr.length-1);
                    // Add this row to our result
                    result += rowRepr + "\n";
                }
            }
        }
    }
    return result;
}

let grade_table = document.getElementById("grades");
let copy_area = document.getElementById("copy-area");

// Copy over grade info on page load.
// We could simply set copy_area.value to grade_table.innerText, but this
// wouldn't line up the columns correctly because we have multi-column
// cells.
if (grade_table != null && copy_area != null) {
    document.addEventListener("DOMContentLoaded", function () {
        copy_area.value = renderTable(grade_table);
    });
}

if (copy_area != null) {
    // Set up select-all-on-click
    copy_area.addEventListener("click", function (ev) {
      copy_area.select();
    });
}
