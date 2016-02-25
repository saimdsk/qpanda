/**
 * Created by yaseen on 2/17/16.
 */

$(document).ready(function() {
    
    $('span.time').each(function(i, obj) {
        // Instead of even using seconds/milliseconds since epoch django can convert datetimefield to an RFC 2822 compliant
        // formatted date, which javascript can use to construct a date. Even easier than before!
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
        $('input#confirmpasswordfield').focus();
        // display the confirm password input field and give it focus.

        $('form#authenticate').attr('action', '/register/');
        // change the submit action to call qpanda.co/register/ instead of qpanda.co/login/.

        $(this).attr('type', 'hidden');
        $('input#hiddenregisterbutton').attr('type', 'submit');
        // input#register is a button and not submit, because when we click it we want to display the confirm password
        // input field. However on a second click of register (once the confirmpassword field has been filled) we want
        // to actually submit the form. So what we do is hide the button and display and identical looking submit.
    });

    $('input#passwordfield').on('input', function() {
        passwordsmatch()
    });

    $('input#confirmpasswordfield').on('input', function() {
        passwordsmatch()
    });

    function passwordsmatch() {
        var password1 = $('input#passwordfield');
        var password2 = $('input#confirmpasswordfield');

        var registerfeedback = $('#registerfeedback');

        if (password2.val().length == 0) {
            registerfeedback.css('display', 'none');
        }

        else if (password1.val() != password2.val()) {
            registerfeedback.attr('class', 'glyphicon glyphicon-remove form-control-feedback fade in');
            registerfeedback.css('display', 'block');
            registerfeedback.css('color', '#a94442');
            password2.attr('class', 'authenticate confirmpasswordfielderror');
        }

        else {
            registerfeedback.attr('class', 'glyphicon glyphicon-ok form-control-feedback fade in');
            registerfeedback.css('display', 'block');
            registerfeedback.css('color', '#3c763d');
            password2.attr('class', 'authenticate confirmpasswordfieldsuccess');
        }
    }


    $('input#hiddenregisterbutton').click(function(event) {
        var username = $('input#usernamefield');
        var password1 = $('input#passwordfield');
        var password2 = $('input#confirmpasswordfield');

        var re = /^[a-zA-Z-_][a-zA-Z0-9-_]{4,}$/;

        if (username.val().length < 5) {
            registrationerror(event, 'Username needs to be atleast 5 characters adlsssssssssssssssllllllllllllll.');
            // TODO Figure out how to deal with a long error message.
        }

        else if (!re.test(username.val())) {
            registrationerror(event, 'Username can only contain letters, numbers, underscores, and hyphens.')
        }

        else if (password1.val() != password2.val()) {
            registrationerror(event, 'Passwords do not match.');
        }

        else if(password1.val().length < 6) {
            registrationerror(event, 'Password needs to be atleast 6 characters.')
        }
    });

    function registrationerror(event, text) {
        $('strong#errortext').text(text);
        $('div#registererrorbox').css('display', 'block');
        event.preventDefault();
    }

    $('.jshide').click(function() {
        // We use the bootstrap alerts to display our other errors. When we submit the form we want to validate
        $('div#registererrorbox').hide();
    });

    /*
    To be totally honest. I wrote a little bit of javascript years ago. I'm guessing that I'm ordering the components
    of my code horribly. But I promise I'll fix it eventually. I'm just learning on the fly, and unfortunately the
    javascript is going to be the most loosely-organised and hacked together part of this project.
     */

    $('.close[data-dismiss="alert"]').click(function() {
        $(this).parent().remove();
        // This is based on consideration 1. We don't need all of boostrap.js just for this functionality.
    })
});
