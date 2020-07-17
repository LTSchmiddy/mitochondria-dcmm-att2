'use strict';

console.log("Time Loaded");

const time_data = {
    display_max_weeks: 4,
    should_display_time_ago_loop_run: false,
    display_time_ago_loop_rate: 5000,

    seconds_to_hms: function (p_sec) {
        let retVal = "";

        let weeks = 0;
        let days = 0;
        let hours = 0;
        let minutes = 0;
        let seconds = 0;

        // Weeks:
        if (p_sec >= 6048001) {
            weeks = Math.floor(p_sec / 6048001);
            retVal += weeks.toString() + "w ";
            p_sec = p_sec % 6048001;
        }

        // Days:
        if (p_sec >= 86400) {
            days = Math.floor(p_sec / 86400);
            retVal += days.toString() + "d ";
            p_sec = p_sec % 86400;
        }


        // Hours:
        if (p_sec >= 3600) {
            hours = Math.floor(p_sec / 3600);
            retVal += hours.toString() + ":";
            p_sec = p_sec % 3600;
        }

        // Minutes
        if (p_sec >= 60) {
            minutes = Math.floor(p_sec / 60);
            if (hours > 0 && minutes < 10) {
                retVal += "0" + minutes.toString() + ":";
            } else {
                retVal += minutes.toString() + ":";
            }

            p_sec = p_sec % 60;
        } else {
            retVal += "0:";
        }

        seconds = Math.floor(p_sec)

        if (p_sec < 10) {
            retVal += "0" + seconds.toString();
        } else {
            retVal += seconds.toString();
        }

        return {
            weeks: weeks,
            days: days,
            hours: hours,
            minutes: minutes,
            seconds: seconds,
            timecode: retVal
        };
    },

    how_long_ago: function(timestamp_sec) {
        let current_time = new Date();

        let time_ago = current_time.getTime()/1000 - timestamp_sec;

        // console.log(current_time);
        // console.log(current_time.getTime());
        // console.log(time_ago);

        return this.seconds_to_hms(time_ago);
        // let retVal = new Date(time_ago);

        // return retVal;
    },

    time_ago_display_str: function (timestamp_sec) {
        let time_ago = this.how_long_ago(timestamp_sec);

        // let retVal = "";

        if (time_ago.weeks > this.display_max_weeks) {
            return new Date(timestamp_sec * 1000).toDateString();
        }

        if (time_ago.weeks > 0) {
            return `${time_ago.weeks} weeks ago`;
        }

        if (time_ago.days > 0) {
            return `${time_ago.days} days ago`;
        }

        if (time_ago.hours > 0) {
            return `${time_ago.hours} hours ago`;
        }

        if (time_ago.minutes > 0) {
            return `${time_ago.minutes} minutes ago`;
        }

        return `${time_ago.seconds} seconds ago`;

    },

    update_all_display_time_ago: function () {
        $('.display-time-ago').each((index, el)=> {
            time_data.update_display_time_ago(el);
        });
    },

    update_display_time_ago: function(elem) {
        let sel = $(elem);
        let my_timestamp = parseInt(sel.attr('data-timestamp'));

        sel.html(this.time_ago_display_str(my_timestamp));
    },

    start_display_time_ago_loop: function() {
        this.should_display_time_ago_loop_run = true;
        this.display_time_ago_loop();

    },

    end_display_time_ago_loop: function() {
        this.should_display_time_ago_loop_run = false;

    },

    display_time_ago_loop: function () {
        this.update_all_display_time_ago();

        if (this.should_display_time_ago_loop_run) {
            setTimeout(this.display_time_ago_loop.bind(this), this.display_time_ago_loop_rate);
        }
    }


}

$(document).ready(()=>{
    time_data.start_display_time_ago_loop();
});


