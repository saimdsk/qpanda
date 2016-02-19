/**
 * Created by yaseen on 2/17/16.
 */

$(document).ready(function() {
    // Instead of even using seconds/milliseconds since epoch django can convert datetimefield to an RFC 2822 compliant
    // formatted date, which javascript can use to construct a date. Even easier than before!

    $('span.time').each(function(i, obj) {
        var rfc2822datestring = $(this).attr('title');
        var d = new Date(rfc2822datestring);

        $(this).attr('title', d);
    });

    $('button.share').click(function() {
        $('#sharelink').attr('type', 'text');
        $('#sharelink').select();
    });

    $('input#register').click(function() {
        // There is one form for login or register because that's awesome UX. If we are registering a user, upon
        // clicking register we will display a hidden element and focus on it for the user to confirm their password.
        $('div#hiddenregister').css('display', 'block');
        $('input#confirmpassword').focus();
    });
});