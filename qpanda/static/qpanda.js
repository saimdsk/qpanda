/**
 * Created by yaseen on 2/17/16.
 */

$(document).ready(function() {
    // Instead of even using seconds/milliseconds since epoch django can convert datetimefield to an RFC 2822 compliant
    // formatted date, which javascript can use to construct a date. Even easier than before!

    $('span.timeasked').each(function(i, obj) {
        var jsdatestring = $(this).attr('title');
        var d = new Date(jsdatestring);

        console.log('jsdatestring: ' + jsdatestring);
        console.log('converted date: ' + d);

        $(this).attr('title', d);
    });
});