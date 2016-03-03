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

        $('form#authenticate').attr('action', '/register/?next=' + window.location.pathname);

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
        // we don't need to keep searching the DOM for these objects. The variables should just be declared once.
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


    $('input.checkregistration').click(function(event) {
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

    // I'm pretty sure I should declare these functions outside document.ready(), right?
    // TODO Investigate javascript function declaration syntax
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
    });

    $('input#getmoreanswers').click(function() {
        dest = window.location.pathname;

        /*
        window.location.pathname returns whats in the address bar following the .com .co or whatever TLD we're using. If
        however if we don't add the trailing slash the ajax request will be made to qpanda.co/1234567moreanswers. That's
        why we check for the slash.
        */

        if (dest[dest.length -1] !== '/') {
            dest += '/'
        }

        /*
        TODO: Do some math to check what comments to load.
        We have it set to get from answer 10 onwards. We need to change that. We need to check what comment the user is
        currently at, get 10 more from that, and append a get parameter to the address bar so that if the user refreshes
        the page, they will load the answers they were currently reading.
         */
        $.getJSON(dest + 'moreanswers/?from=10', function(data, status) {
            if (status == 'success') {
                deserialise(data)
            } else {
                console.log('AJAX request to ' + dest + ' failed...');
            }
        });
    });

    function deserialise(data) {
        data2 = data['answers'];
        keys = Object.keys(data2);

        output = '';

        for (var i=0; i < keys.length; i++) {
            key = keys[i];
            user = data2[key];

            // We are just outputting whats in answers.html again pretty much.
            if (i == 0) {
                output += '<ul class="list-group" id="answerlist">';
            }

            output += '<li class="list-group-item">';
            output += '<div>' + user.answer_text + '</div>';
            output += '<div class="answerfooter">';

            if (user.username != '') {
                output +='<a id="username">' + user.username + '</a>';
            }
            else {
                output += '<span>Anonymous</span>';
            }

            d = new Date(user.pub_date);
            datespan = '<span class="time timeasked" title="' + d + '">' + user.time_since + '</span>';

            output += datespan;
            output += '</div></li>';

            if (i == keys.length-1) {
                output += '</ul>';
                $('ul#answerlist').replaceWith(output);
            }

            // Leaving these console.logs in case they are needed in the future...
            console.log('username: ' + user.username);
            console.log('answer text: ' + user.answer_text);
            console.log('pub_date: ' + user.pub_date);
            console.log('time_since: ' + user.time_since);
            console.log('locale date: ' + d);
        }
    }
});
