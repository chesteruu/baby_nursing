var elapsedTimeText = document.getElementsByClassName("elapsed-time-text")[0];

/** Stores the reference to the elapsed time interval*/
var elapsedTimeIntervalRef;

/** Stores the start time of timer */
var startTime = new Date(document.getElementById("last_nursing_time").value);


/** Starts the stopwatch */
function startStopwatch() {
    // Every second
    elapsedTimeIntervalRef = setInterval(() => {
        // Compute the elapsed time & display
        elapsedTimeText.innerText = timeAndDateHandling.getElapsedTime(startTime); //pass the actual record start time

        // Improvement: Can Stop elapsed time and resert when a maximum elapsed time
        //              has been reached.
    }, 1000);
}


startStopwatch();