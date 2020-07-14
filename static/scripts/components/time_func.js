export function time_func(val) {
    let retVal = "";

    let hours = 0;
    let minutes = 0;
    let seconds = 0;

    // Hours:
    if (val >= 3600) {
        hours = Math.floor(val / 3600);
        retVal += hours.toString() + ":";
        val = val % 3600;
    }

    // Minutes
    if (val >= 60) {
        minutes = Math.floor(val / 60);
        if (hours > 0 && minutes < 10){
            retVal += "0" + minutes.toString() + ":";
        } else {
            retVal += minutes.toString() + ":";
        }

        val = val % 60;
    } else {
        retVal += "0:";
    }

    seconds = Math.floor(val)

    if (val < 10){
        retVal += "0" + seconds.toString();
    } else {
        retVal += seconds.toString();
    }

    return {
        hours: hours,
        minutes: minutes,
        seconds: seconds,
        timecode: retVal
    };
}
