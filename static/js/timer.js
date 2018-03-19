$(document).ready(function() {

    function startTimer(duration, display) {
        var timer = duration, minutes, seconds, milliseconds;
        var refresh = setInterval(function () {
            // noinspection JSCheckFunctionSignatures
            minutes = parseInt(timer / 100 / 60, 10);
            // noinspection JSCheckFunctionSignatures
            seconds = parseInt((timer / 100)% 60, 10);
            // noinspection JSCheckFunctionSignatures
            milliseconds = parseInt(timer % 100, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            milliseconds = milliseconds < 10 ? "0" + milliseconds : milliseconds;

            var output = minutes + " : " + seconds + " : " + milliseconds;
            display.text(output);
            final_time = timer;
            if (ticktick && --timer < 0) {
                display.text("Time's Up!");
                clearInterval(refresh);
            }
        }, 10);

    }

    jQuery(function ($) {
        var display = $('#time');
        startTimer(Minutes, display);
    });

});