/**
 * Created by yaseen on 2/17/16.
 */

// TODO Pick a style
// I'm using underscores e.g. 'from_answer', camelcased e.g. 'credentialsValid()', and regular e.g. 'registerselected'.

$(document).ready(function() {

    var registerselected = false;
    var password1, password2, registerfeedback;

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
        /* This highlights the sharelink text to make it easy to copy and paste the link. */
    });

    $('input#registerbutton').click(function() {
        registerselected = true;

        // There is one form for login or register because that's awesome UX. If we are registering a user, upon
        // clicking register we will display a hidden element and focus on it for the user to confirm their password.

        $('div#hiddenregister').css('display', 'block');
        $('input#confirmpasswordfield').focus();
        // display the confirm password input field and give it focus.

        $('form#authenticate').attr('action', '/register/?next=' + window.location.pathname);
        /* this is used for redirecting to the next page. If the user logs in on the homepage or an askedquestion page
           we should redirect to that page on register or login. */

        $(this).attr('type', 'hidden');
        $('input#loginbutton').attr('type', 'hidden');
        $('input#hiddenregisterbutton').attr('type', 'submit');
        // input#register is a button and not submit, because when we click it we want to display the confirm password
        // input field. However on a second click of register (once the confirmpassword field has been filled) we want
        // to actually submit the form. So what we do is hide the button and display and identical looking submit.
    });

    $('input#usernamefield').on('input', function() {
        if (registerselected) {
            passwordsmatch()
        }
        // TODO Branch passwordsmatch into passwordsvalid and usernamevalid
    });

    $('input#passwordfield').on('input', function() {
        if (registerselected) {
            passwordsmatch();
        }
    });

    $('input#confirmpasswordfield').on('input', function() {
        if (registerselected) {
            passwordsmatch();
        }
    });

    function passwordsmatch() {
        if (password1 == null || password2 == null || registerfeedback == null) {
            password1 = $('input#passwordfield');
            password2 = $('input#confirmpasswordfield');
            registerfeedback = $('#registerfeedback');
        }

        if (password2.val().length == 0) {
            registerfeedback.css('display', 'none');
        }

        else if (!credentialsValid()) {
            registerfeedback.attr('class', 'glyphicon glyphicon-remove form-control-feedback fade in');
            registerfeedback.css('display', 'block');
            registerfeedback.css('color', '#a94442');
            password2.attr('class', 'auth confirmpasswordfielderror');
        }

        else {
            registerfeedback.attr('class', 'glyphicon glyphicon-ok form-control-feedback fade in');
            registerfeedback.css('display', 'block');
            registerfeedback.css('color', '#3c763d');
            password2.attr('class', 'auth confirmpasswordfieldsuccess');
            password2.attr('title', 'Credentials are valid.')
        }
    }


    $('input.checkregistration').click(function(event) {
        credentialsValid(true, event);
    });

    function credentialsValid(formsubmit, event) {
        /* the usage of formsubmit is explained in the registrationerror function */

        var username = $('input#usernamefield');

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

        registrationerror(formsubmit, event, errormessage);

        return false;
    }

    function registrationerror(formsubmit, event, text) {
        /*
        We call credentialsValid every time a user inputs text into the password fields. We don't need to display the
        error div on every keystroke so instead we display the error message in a tooltip on the confirmpasswordfield.
        We still want to display the error box if the user clicks submit though and didn't read the tooltip. So we check
        if the submit event happened, if so we stop it and display the error div. Until then we just display the tooltip.
         */

        if (formsubmit) {
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

    window.onpopstate = function(event) {
        /*
        When we use getmoreanswers it submits an ajax request for more answers and changes the window.location bar to
        show the updated url. If the user reloads the page, they will be returned to the current answers they are
        viewing. However if you click back it will load the previous url but keep the same answers. We need to implement
        a solution that gets the previous answers.
        */

        // Apparently I should be using const. Const is block level unlike var which is function level.

        var currenturl, dest, pushto, from_answer, popto, moreanswers;
        if (event.state == null) {
            console.log(window.location.href);

            currenturl = window.location.pathname;
            if (currenturl[currenturl.length -1] !== '/') {
                currenturl += '/';
            }
            dest = currenturl + 'moreanswers/?from=0';
            pushto = currenturl + '?from=10';
            from_answer = 0;
            moreanswers = false;

            jsongetanswers(dest, pushto, dest, from_answer, moreanswers);
        }
        else {
            pushto = event.state['pushto'];
            popto = event.state['popto'];
            from_answer = event.state['from_answer'];

            currenturl = window.location.pathname;
            if (currenturl[currenturl.length -1] !== '/') {
                currenturl += '/';
            }

            dest = currenturl + 'moreanswers/?from=' + from_answer;

            console.log('--------------------------------------');
            console.log('dest: ' + pushto);
            console.log('popto: ' + popto);
            console.log('from: ' + from_answer);
            console.log('--------------------------------------');

            jsongetanswers(dest, popto, pushto, from_answer+10, false)
        }
    };

    function jsongetanswers(dest, popto, pushto, from_answer, moreanswers) {
        /*
        dest = destination of get request
        popto = the dictionary that we need to use to know what to pop back to
        pushto = the url that we push to
        from_answer = the answer we use as a reference point.
        moreanswers = boolean to see if we want more answers. If true get more, else get previous answers.
         */

        console.log('desturl: ' + dest);
        console.log('popto: ' + popto);
        console.log('pushto: ' + pushto);
        console.log('from_answer: ' + from_answer);

        $.getJSON(dest, function(data) {
            if (moreanswers) {
                deserialise(data, from_answer+10);
                window.history.pushState({'from_answer': from_answer, 'pushto': pushto, 'popto': popto}, '', pushto);
            }

            else {
                deserialise(data, from_answer-10);
            }
        })
        .fail(function() {
            console.log('AJAX request to ' + dest + ' failed...');
        });
    }

    $('input#getmoreanswers').click(function() {
        var currenturl = window.location.pathname;

        /*
        window.location.pathname returns whats in the address bar following the .com .co or whatever TLD we're using. If
        however if we don't add the trailing slash the ajax request will be made to qpanda.co/1234567moreanswers. That's
        why we check for the slash.
        */

        if (currenturl[currenturl.length -1] !== '/') {
            currenturl += '/'
        }

        var answer_list = $('#answerlist');
        var from_answer = parseInt(answer_list.attr("data-fromanswer"));

        /*
        SUPER SUPER IMPORTANT
        FIX THIS. SUPER SUPER HACKED TOGETHER!
         */

        if (from_answer < 0 ) {
            from_answer = 10;
        }

        var desturl = currenturl + 'moreanswers/?from=' + from_answer;
        var popto;

        if (from_answer <= 10) {
            popto = window.location.pathname
        } else {
            popto = window.location.pathname + '?from=' + (from_answer-10);
        }
        var pushto = window.location.pathname + '?from=' + (from_answer);

        jsongetanswers(desturl, popto, pushto, from_answer, true);

        /*
        $.getJSON(currenturl + 'moreanswers/?from=' + from_answer, function(data) {
                deserialise(data, from_answer+10);

                // If the user refreshes the page after an ajax get, it will load the answers from the get request
                // onwards. They won't have to click the getmoreanswers button to get to where they want.

                // you can't change window.location because that triggers a reload, pushstate doesn't trigger reload.
                var prevstate;
                if (from_answer < 10) {
                    prevstate = {'popto': window.location.href};
                }

                else {
                    prevstate = {'popto': window.location.href + '?from=' + from_answer};
                }
                window.history.pushState(prevstate, '', currenturl + '?from=' + from_answer);
            })
        .fail(function() {
            console.log('AJAX request to ' + currenturl + ' failed...');
        });*/
    });

    function deserialise(data, from_answer) {
        // from_answer will be used to set the next data-fromanswer attribute in the new answerlist.

        var more_answers = data['more_answers'];
        if (!more_answers) {
            $('input#getmoreanswers').hide();
        } else {
            $('input#getmoreanswers').show();
        }

        var data2 = data['answers'];
        var keys = Object.keys(data2);

        /* It's called data2 because it is a dict within a dict and I don't know what else to call it. */

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

            if (user.username != 'Anonymous') {
                output +='<a id="username">' + user.username + '</a>';
            }
            else {
                output += '<span>Anonymous</span>';
            }

            var d = new Date(user.pub_date);
            output += '<span class="time timeasked" title="' + d + '">' + user.time_since + '</span>';

            output += '</div></li>';

            if (i == keys.length-1) {
                output += '</ul>';
                $('ul#answerlist').replaceWith(output);
            }
        }
    }
});
