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
        /*
        We're programmers and we use our keyboards very often. As much as possible actually. Using the keyboard is just
        much easier than switching back and forth between the mouse/touchpad and keyboard. When I submit forms I love
        typing [tab] typing [tab] typing [tab] typing [tab]... and so on until [enter]. So with our form I investigated
        how it worked. I knew that I was going to run into the problem where if a user clicked on register but actually
        wanted to log in.

        Because the login submit is closest to the form I realised that if a user clicked register but pressed enter
        after filling in the password form, it would call login and not register. However because I'm changing the form
        action attribute either button will still submit to /register/.
         */
        // There is one form for login or register because that's awesome UX. If we are registering a user, upon
        // clicking register we will display a hidden element and focus on it for the user to confirm their password.

        $('div#hiddenregister').css('display', 'block');
        $('input#confirmpasswordfield').focus();
        // display the confirm password input field and give it focus.

        $('form#authenticate').attr('action', '/register/?next=' + window.location.pathname);

        $(this).attr('type', 'hidden');
        $('input#loginbutton').attr('type', 'hidden');
        $('input#hiddenregisterbutton').attr('type', 'submit');
        // input#register is a button and not submit, because when we click it we want to display the confirm password
        // input field. However on a second click of register (once the confirmpassword field has been filled) we want
        // to actually submit the form. So what we do is hide the button and display and identical looking submit.
    });

    $('input#usernamefield').on('input', function() {
        passwordsmatch();
        /*
        Before this was added, there were problems with having an invalid username. If the user entered an invalid
        username, then entered a valid password and invalid password, and then corrected the username, the error message
        would still appear. It occurred because we only checked if the username was valid on the change of passwords,
        not on the change of usernames.

        TODO Check passwordsmatch only if the user has clicked on register
        on input will be called frequently, even if the user is not registering. We should check if the user is
        registering before we waste calling passwordsmatch and performing unnecessary computations.

        TODO Branch passwordsmatch into passwordsvalid and usernamevalid
         */
    });

    $('input#passwordfield').on('input', function() {
        passwordsmatch();
    });

    $('input#confirmpasswordfield').on('input', function() {
        passwordsmatch();
    });

    function passwordsmatch() {
        // we don't need to keep searching the DOM for these objects. The variables should just be declared once.
        var password1 = $('input#passwordfield');
        var password2 = $('input#confirmpasswordfield');

        var registerfeedback = $('#registerfeedback');

        if (password2.val().length == 0) {
            registerfeedback.css('display', 'none');
        }

        else if (!credentialsValid()) {
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
            password2.attr('title', 'Credentials are valid.')
        }
    }


    $('input.checkregistration').click(function(event) {
        credentialsValid(true, event);
    });

    function credentialsValid(eventoccurred, event) {
        var username = $('input#usernamefield');
        var password1 = $('input#passwordfield');
        var password2 = $('input#confirmpasswordfield');

        var re = /^[a-zA-Z-_][a-zA-Z0-9-_]{4,}$/;

        errormessage = '';

        if (username.val().length < 5) {
            errormessage = 'Username needs to be atleast 5 characters.';
            // TODO Figure out how to deal with a long error message.
        }
        else if (!re.test(username.val())) {
            errormessage = 'Username can only contain letters, numbers, underscores, and hyphens.';
        }
        else if (password1.val() != password2.val()) {
            errormessage = 'Passwords do not match.';
        }
        else if(password1.val().length < 6) {
            errormessage = 'Password needs to be atleast 6 characters.';
        }
        else {
            return true;
        }

        if (eventoccurred) {
            registrationerror(true, event, errormessage);
        }
        else {
            registrationerror(false, event, errormessage)
        }
        return false;
    }

    // I'm pretty sure I should declare these functions outside document.ready(), right?
    // TODO Investigate javascript function declaration syntax
    function registrationerror(eventoccurred, event, text) {
        /*
        We call credentialsValid everytime a user inputs text into the password fields. We don't want to constantly keep
        bringing up the error div. So instead we display the error message in a tooltip on the confirmpasswordfield. We
        still want to display the error box if the user clicks submit though and didn't read the tooltip. So we check if
        the submit event happened, if so we stop it and display the error div. Until then we just display the tooltip.
         */
        if (eventoccurred) {
            $('strong#errortext').text(text);
            $('div#registererrorbox').css('display', 'block');
            event.preventDefault();
        }

        $('input#confirmpasswordfield').attr('title', text);
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

        var answer_list = $('#answerlist');
        var from_answer = parseInt(answer_list.attr("data-fromanswer"));
        $.getJSON(dest + 'moreanswers/?from=' + from_answer, function(data) {
                deserialise(data, from_answer+10);

                // If the user refreshes the page after an ajax get, it will load the answers from the get request
                // onwards. They won't have to click the getmoreanswers button to get to where they want.

                // you can't change window.location because that triggers a reload, pushstate doesn't trigger reload.
                window.history.pushState({}, '', dest + '?from=' + from_answer);
            })
        .fail(function() {
            console.log('AJAX request to ' + dest + ' failed...');
        });
    });

    function deserialise(data, from_answer) {
        // from_answer will be used to set the next data-fromanswer attribute in the new answerlist.

        var more_answers = data['more_answers'];
        if (!more_answers) {
            $('input#getmoreanswers').remove();
        }

        var data2 = data['answers'];
        var keys = Object.keys(data2);

        var output = '';

        for (var i=0; i < keys.length; i++) {
            var key = keys[i];
            var user = data2[key];

            // We are just outputting whats in answers.html again pretty much.

            // I don't think I should delete the <ul> and replace it with another one. I think I should just change the
            // <li> contents within it. Especially since we are setting the data-fromanswer attr again in this function.
            if (i == 0) {
                output += '<ul class="list-group" id="answerlist" data-fromanswer="' + from_answer + '">';
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

            var d = new Date(user.pub_date);
            var datespan = '<span class="time timeasked" title="' + d + '">' + user.time_since + '</span>';

            output += datespan;
            output += '</div></li>';

            if (i == keys.length-1) {
                output += '</ul>';
                $('ul#answerlist').replaceWith(output);
            }

            // Leaving these console.logs in case they are needed in the future...
            /*
            console.log('username: ' + user.username);
            console.log('answer text: ' + user.answer_text);
            console.log('pub_date: ' + user.pub_date);
            console.log('time_since: ' + user.time_since);
            console.log('locale date: ' + d);
            */
        }
    }
});
