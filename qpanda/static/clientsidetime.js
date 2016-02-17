/**
 * Created by yaseen on 2/17/16.
 */

$(document).ready(function() {

    var offset = new Date().getTimezoneOffset();
    // offset returns the difference between UTC timezone and client timezone in seconds.
    // e.g. Sydney is 11 hours ahead (during AEDT) which is an offset of -660. Because Sydney is ahead in time compared
    // to UTC the offset is negative. It can be represented in UTC as UTC+11 though, because it is 11 hours ahead.
    var utcoffset = offset / 60.0 * -1;

    console.log('UTCOFFSET: ' + utcoffset);

    $('span.timeasked').each(function(i, obj) {
        if (utcoffset > 0) {
            $(this).attr('title', 'UTC+' + utcoffset);
        }
        else if (utcoffset < 0) {
            $(this).attr('title', 'UTC' + utcoffset);
        }
        else { //when the offset is 0, i.e. on UTC time.
            $(this).attr('title', 'UTC');
        }

    });
});