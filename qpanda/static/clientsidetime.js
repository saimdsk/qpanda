/**
 * Created by yaseen on 2/17/16.
 */

$(document).ready(function() {
    /*
    Instead of using timezones, we pass seconds since the epoch to js (using a template filter). We multiply it by 1000
    because javascript can calculate the date based on MILLISECONDS since the epoch. And boom! Done. No need for all the
    other code!
     */

    $('span.timeasked').each(function(i, obj) {
        var secssinceepoch = $(this).attr('title');
        var d = new Date(secssinceepoch * 1000);

        $(this).attr('title', d);
    });
});