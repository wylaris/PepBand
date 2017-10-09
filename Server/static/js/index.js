/**
 * Created by michaelperez on 3/17/17.
 */
function changeScreen()
{
    if(this.hash !== undefined) {
        var name = this.hash.substr(1);

        var signIn = $('.sign-in');
        var signUp = $('.sign-up');
        var home = $('.home');

        if (name == "SignIn") {
            $('#signin').addClass('active');
            $('#signout').removeClass('active');
            $('#home').removeClass('active');
            signUp.fadeOut("slow", function () {
                home.fadeOut("slow", function () {
                    signIn.fadeIn("slow");
                });
            });
        }
        else if (name == "SignUp") {
            $('#signin').removeClass('active');
            $('#signout').addClass('active');
            $('#home').removeClass('active');
            signIn.fadeOut("slow", function () {
                home.fadeOut("slow", function () {
                    signUp.fadeIn("slow");
                });
            });
        }
        else {
             $('#signin').removeClass('active');
            $('#signout').removeClass('active');
            $('#home').addClass('active');
            signIn.fadeOut("slow", function () {
                signUp.fadeOut("slow", function () {
                    home.fadeIn("slow");
                });
            });
        }
    }
}

function processLogIn(event)
{

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

    var formData = {
            username : $('#usernamelog').val(),
            password : $('#passwordlog').val()
        };


        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url         : '/accounts/auth/', // the url where we want to POST
            data        : formData, // our data object
            dataType    : 'json', // what type of data do we expect back from the server
                        encode          : true
        })
        // using the done promise callback
            .done(function(data) {
                console.log(data);
                if(data['status'] == "OK")
                {
                    console.log("sdadssd");
                    window.location.replace(data['url']);
                }
                else
                {
                    $('#errorlogin').text(data['errors']);
                }

                // here we will handle errors and validation messages
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();

        $('.error-c').text('');
}



$( document ).ready(function() {
    changeScreen();
    $('.sign').click(changeScreen);

    $('#loginform').submit(function(event) {
            processLogIn(event)
    });

});

function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


