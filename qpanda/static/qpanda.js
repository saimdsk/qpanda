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
        var sharelink = $('#sharelink');
        sharelink.attr('type', 'text');
        sharelink.select();
    });

    $('input#registerbutton').click(function() {
        // There is one form for login or register because that's awesome UX. If we are registering a user, upon
        // clicking register we will display a hidden element and focus on it for the user to confirm their password.

        $('div#hiddenregister').css('display', 'block');
        $('input#confirmpassword').focus();
        // display the confirm password input field and give it focus.

        $('form#authenticate').attr('action', '/register/');
        // change the submit action to call qpanda.co/register/ instead of qpanda.co/login/.

        $(this).attr('type', 'hidden');
        $('input#hiddenregisterbutton').attr('type', 'submit');
        // input#register is a button and not submit, because when we click it we want to display the confirm password
        // input field. However on a second click of register (once the confirmpassword field has been filled) we want
        // to actually submit the form. So what we do is hide the button and display and identical looking submit.
    });

    $('input#hiddenregisterbutton').click(function(event) {
        var password1 = $('input#passwordfield');
        var password2 = $('input#confirmpasswordfield');

        var registrationerrordiv = $('div#registererrorbox');
        var registrationerrortext = $('strong#errortext');
        if (password1.val() != password2.val()) {
            console.log('here');
            registrationerrortext.text('Passwords do not match.');
            registrationerrordiv.css('display', 'block');
            event.preventDefault();
        }
    });

});