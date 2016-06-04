// Your Client ID can be retrieved from your project in the Google
// Developer Console, https://console.developers.google.com

var CLIENT_ID;

function initClientId(client_id){
    CLIENT_ID = client_id;
};

var SCOPES = ['profile', 'email'];

/**
 * Check if current user has authorized this application.
 */
function checkAuth() {
    gapi.auth.authorize(
        {
            'client_id': CLIENT_ID,
            'scope': SCOPES.join(' '),
            'immediate': true
        }, handleAuthResult);
};

/**
 * Handle response from authorization server.
 *
 * @param {Object} authResult Authorization result.
 */
function handleAuthResult(authResult) {
    if (authResult && !authResult.error) {
	    gapi.client.load('plus', 'v1').then(function() {
		var request = gapi.client.plus.people.get({
		    'userId': 'me'
		})
		request.then(function(resp) {
		    if(resp.result.domain === "stuy.edu"){
			$.getJSON("/addUser", {
			    'username': resp.result.displayName,
			    'email': resp.result.emails[0].value,
			    'auth': auth,
			}, function(data){
			    window.location.reload(true)
			});
		    }else{
			document.getElementsByClassName("col-lg-12 text-center")[0].innerHTML="You need to sign in with a stuy.edu email. You can press the logout button to log out of your current gmail.";
			document.getElementsByClassName("col-lg-12 text-center")[0].style.color="red";
		    }
		}, function(reason) {
			console.log('Error: ' + reason.result.error.message);
		});
	    });
    }else if(authResult.error != "immediate_failed"){
	$.getJSON("/logout", {
	});
    }
}

/**
 * Initiate auth flow in response to user clicking authorize button.
 *
 * @param {Event} event Button click event.
 */
function handleAuthClick(event) {
    if(event != null){
	auth = event.target.id;
    }else if(document.getElementById("classes") != null){
	auth = "student";
    }else{
	auth = "teacher";
    }
    gapi.auth.authorize(
        {client_id: CLIENT_ID, scope: SCOPES, immediate: false},
        handleAuthResult);
    return false;
};

/**
 * Sign a user out
 */
function signOut(){
    var winning = window.open("","","width=500,height=500");
    winning.location = "https://accounts.google.com/logout";
    setInterval(function(){
	try{
        winning.location.href;
	}catch(err){
            winning.close();
	    $.getJSON("/logout", {
	    }, function(data){
		window.location.reload(true)
	    });
	}
    }, 100);
};

document.getElementById('teacher').addEventListener("click", handleAuthClick);
document.getElementById('student').addEventListener("click", handleAuthClick);
