/**
 * Created by yaseen on 2/17/16.
 */

// Before reading any further, please realise that I do not understand javascript. I learnt a little bit over 2 years
// ago and that was from following a tutorial. I've done absolutely no research or learning about how to write good
// javascript. Instead I just write the code as I need it. So if it looks like it is hacked together, you're right.

// TODO Pick a style
// I'm using underscores e.g. 'from_answer', camelcased e.g. 'credentialsValid()', and regular e.g. 'registerselected'.

$(document).ready(function() {

    var registerSelected = false;
    var password1, password2, registerFeedback;
    // these variables were constantly being retrieved from the DOM by jquery on keyboard input. So instead they're
    // assigned once.

    $('span.time').each(function(i, obj) {
        // Instead of even using seconds/milliseconds since epoch django can convert datetimefield to an RFC 2822
        // compliant formatted date, which javascript can use to construct a date. Even easier than before!
        var rfc2822DateString = $(this).attr('title');
        var d = new Date(rfc2822DateString);

        $(this).attr('title', d);
    });

    $('button.share').click(function() {
        // clicking on the share link will open up a highlighted input text allowing easy copy-paste for the user.
        var shareLink = $('#sharelink');
        shareLink.attr('type', 'text');
        shareLink.select();
    });

    $('input#registerbutton').click(function() {
        // Used to avoid wasteless calls to checkAuthDetails().
        registerSelected = true;

        // Display the hidden confirmpasswordfield and give it focus.
        $('div#hiddenregister').css('display', 'block');
        $('input#confirmpasswordfield').focus();

        // Change the form action to /register/ instead of login. Add a next get paremeter to know where to redirect.
        $('form#authenticate').attr('action', '/register/?next=' + window.location.pathname);

        // We hide this button. And display an input submit that looks the exact same. This is done because they have
        // different click reactions. This displays the hidden confirm password. The other one checks the registration
        // input to make sure it is valid.
        $(this).attr('type', 'hidden');

        $('input#loginbutton').attr('type', 'hidden'); // self explanatory.

        // Change it from hidden to submit.
        $('input#hiddenregisterbutton').attr('type', 'submit');
    });

    $('input#usernamefield').on('input', function() {
        if (registerSelected) {
            checkAuthDetails()
        }
    });

    $('input#passwordfield').on('input', function() {
        if (registerSelected) {
            checkAuthDetails();
        }
    });

    $('input#confirmpasswordfield').on('input', function() {
        if (registerSelected) {
            checkAuthDetails();
        }
    });

    function checkAuthDetails() {
        // Called every time there is a keyboard input in the auth fields.

        // We check the registration details to see if they are long enough, the passwords match, and that the username
        // uses only valid characters.

        if (password1 == null || password2 == null || registerFeedback == null) {
            // If not yet assigned, assigned them. We do this to avoid having to constantly search the DOM for elements
            // on every keyboard input event.
            password1 = $('input#passwordfield');
            password2 = $('input#confirmpasswordfield');
            registerFeedback = $('#registerfeedback');
        }

        if (password2.val().length == 0) {
            // We don't want to start off displaying an error message.
            registerFeedback.css('display', 'none');
        }

        else if (credentialsValid()) {
            registerFeedback.attr('class', 'glyphicon glyphicon-ok form-control-feedback fade in');
            registerFeedback.css('display', 'block');
            registerFeedback.css('color', '#3c763d');
            password2.attr('class', 'auth confirmpasswordfieldsuccess');
            password2.attr('title', 'Credentials are valid.')
        }

        else {
            registerFeedback.attr('class', 'glyphicon glyphicon-remove form-control-feedback fade in');
            registerFeedback.css('display', 'block');
            registerFeedback.css('color', '#a94442');
            password2.attr('class', 'auth confirmpasswordfielderror');
        }
    }


    $('input.checkregistration').click(function(event) {
        // On the form submit we check for validation even though its already been done. If there is a submit though we
        // handle it further in credentialsValid.
        credentialsValid(true, event);
    });

    function credentialsValid(formSubmit, event) {
        /* the usage of formsubmit is explained in the registrationerror function */

        var username = $('input#usernamefield');
        var re = /^[a-zA-Z-_][a-zA-Z0-9-_]{4,}$/;
        var errorMessage = '';

        if (username.val().length < 5) {
            errorMessage = 'Username needs to be atleast 5 characters.';
        }

        else if (!re.test(username.val())) {
            errorMessage = 'Username can only contain letters, numbers, underscores, and hyphens.';
        }

        else if (password1.val() != password2.val()) {
            errorMessage = 'Passwords do not match.';
        }

        else if(password1.val().length < 6) {
            errorMessage = 'Password needs to be atleast 6 characters.';
        }

        else {
            // Passed all the tests. Credentials are valid!
            return true;
        }

        // Failed the tests. Display the appropriate errormessage and return false.
        registrationError(formSubmit, event, errorMessage);
        return false;
    }

    function registrationError(formSubmit, event, text) {
        /*
        We call credentialsValid every time a user inputs text into the password fields. We don't need to display the
        error div on every keystroke so instead we display the error message in a tooltip on the confirmpasswordfield.
        We still want to display the error box if the user clicks submit though and didn't read the tooltip. So we check
        if the submit event happened, if so we stop it and display the error div. Until then we just display the tooltip.
         */

        if (formSubmit) {
            // If it was a submit display the error in the dismissable box.
            $('strong#errortext').text(text);
            $('div#registererrorbox').css('display', 'block');
            event.preventDefault();
        }

        // If it wasn't a submit (or even if it was) display the error message in a tooltip.
        $('input#confirmpasswordfield').attr('title', text);
    }

    $('.jshide').click(function() {
        // Bootstrap data-dismiss removes the element. If we only want to hide it we use this.

        // If the user submits an invalid registration form we should display an error. If they dismiss it and send
        // invalid data again we should again display an error. Data-dismiss would remove the element and wouldn't allow
        // the error div to be displayed on error n > 1. So we made the functionality ourselves.
        $('div#registererrorbox').hide();
    });

    $('.close[data-dismiss="alert"]').click(function() {
        $(this).parent().remove();
        // This is based on consideration 1. We don't need all of boostrap.js just for this functionality.
    });

    window.onpopstate = function(event) {
        // Called when a user goes back after loading more answers using AJAX.

        /*
        When we use getmoreanswers it submits an ajax request for more answers and changes the window.location bar to
        show the updated url. If the user reloads the page, they will be returned to the current answers they are
        viewing. However if you click back it will load the previous url but keep the same answers. We need to implement
        a solution that gets the previous answers.
        */

        var currentUrl, dest, pushTo, fromAnswer, popTo, moreAnswers;

        // If we're on the page qpanda.co/1234567/?from=10 and we press back to go to qpanda.co/1234567.
        // qpanda.co/1234567/?from=10 will have event.state as null and qpanda.co/1234567 will never pop.
        if (event.state == null) {
            currentUrl = window.location.pathname;

            if (currentUrl[currentUrl.length -1] !== '/') {
                currentUrl += '/';
            }

            dest = currentUrl + 'moreanswers/?from=0';
            pushTo = currentUrl + 'moreanswers/?from=10';
            fromAnswer = 10;
            moreAnswers = false;

            jsonGetAnswers(dest, currentUrl, pushTo, fromAnswer, moreAnswers);
        }

        // e.g. going from qpanda.co/1234567/?from=20 to qpanda.co/1234567/?from=10
        else {
            pushTo = event.state['pushTo'];
            popTo = event.state['popTo'];
            fromAnswer = event.state['fromAnswer'];
            currentUrl = window.location.pathname;

            if (currentUrl[currentUrl.length -1] !== '/') {
                currentUrl += '/';
            }

            dest = currentUrl + 'moreanswers/?from=' + fromAnswer;

            jsonGetAnswers(dest, popTo, pushTo, fromAnswer+10, false)
        }
    };

    function jsonGetAnswers(dest, popTo, pushTo, fromAnswer, moreAnswers) {
        /*
        dest = destination of json get request
        popto = the url that we'll popto (if the back button is clicked)
        pushto = the url that we will push (using pushState)
        from_answer = the answer we use as a reference point in the json request
        moreanswers = boolean to see if we want more answers. If true get more, else get previous answers.
         */

        $.getJSON(dest, function(data) {
            if (moreAnswers) {
                deserialise(data, fromAnswer+10);
                window.history.pushState({'fromAnswer': fromAnswer, 'pushTo': pushTo, 'popTo': popTo}, '', pushTo);
            }

            else {
                deserialise(data, fromAnswer);
            }
        })
        .fail(function() {
            console.log('AJAX request to ' + dest + ' failed...');
        });
    }

    $('input#getmoreanswers').click(function() {
        var currentUrl = window.location.pathname;
        // window.location.pathname returns whats in the address bar following the .com .co or whatever we're using.
        // If however if we don't add the trailing slash the ajax request will be made to qpanda.co/1234567moreanswers.
        // That's why we check for the slash.

        if (currentUrl[currentUrl.length -1] !== '/') {
            currentUrl += '/'
        }

        var fromAnswer = parseInt($('#answerlist').attr("data-fromanswer"));
        // data-fromanswer tells you the answer index it is displaying up to. I.e. If the answers with index 0 to 9 are
        // being displayed data-fromanswer will have a value of 10.

        if (fromAnswer < 0 ) {
            fromAnswer = 10;
        }

        var destUrl = currentUrl + 'moreanswers/?from=' + fromAnswer;
        var popTo;

        if (fromAnswer <= 10) {
            popTo = window.location.pathname
        } else {
            popTo = window.location.pathname + '?from=' + (fromAnswer-10);
        }

        var pushTo = window.location.pathname + '?from=' + (fromAnswer);

        jsonGetAnswers(destUrl, popTo, pushTo, fromAnswer, true);
    });

    function deserialise(data, fromAnswer) {
        // from_answer will be used to set the next data-fromanswer attribute in the new answerlist.

        var moreAnswers = data['more_answers'];
        if (!moreAnswers) {
            $('input#getmoreanswers').hide();
        } else {
            $('input#getmoreanswers').show();
        }

        var data2 = data['answers'];
        var keys = Object.keys(data2);
        // It's called data2 because it is a dict within a dict and I don't know what else to call it.

        $('#answerlist').attr('data-fromanswer', fromAnswer);
        var answers = $('.list-group-item');

        for (var i=0; i < answers.length && i < keys.length; i++) {
            var key = keys[i];
            var jsonAnswer = data2[key]; // A specific answer in the JSONDict
            var a = answers[i]; // A specific answer in the unordered list.


            var answerText = $(a).find(".answertext").html(jsonAnswer.answer_text);
            if (jsonAnswer.username != 'Anonymous') {
                $(a).find("span.username").html('<a>' + jsonAnswer.username + '</a>');
            } else {
                $(a).find("span.username").html('Anonymous');
            }
            var d = new Date(jsonAnswer.pub_date);
            var answerDate = $(a).find('span.anstime');
            answerDate.attr('title', d);
            answerDate.html(jsonAnswer.time_since);

            if (!$(a).is(':visible')) {
                // if certain answers were hidden before because there wasn't 10 answers available we show them again.
                $(a).show();
            }
        }

        if (answers.length > keys.length) {
            for (i = keys.length; i < answers.length; i++) {
                // if we load a page with only a few answers, we hide the old answers. We can't remove them because if
                // we press back the answer won't be displayed. If the user clicks back the old answers will be shown
                // again in the "if (!$(a).is(':visible'))" block.
                a = answers[i];
                $(a).hide();
            }
        }
    }
});
