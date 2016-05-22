// Your Client ID can be retrieved from your project in the Google
// Developer Console, https://console.developers.google.com

var CLIENT_ID

function initClientId(client_id){
    CLIENT_ID = client_id;
};

var SCOPES = ['https://www.googleapis.com/auth/plus.login'];

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
    if (authResult && !authResult.error && authResult.hd === "stuy.edu") {
	console.log(authResult)
	gapi.client.load('plus', 'v1').then(function() {
	    var request = gapi.client.plus.people.get({
		'userId': 'me'
            });

	    request.then(function(resp) {
		console.log(resp)
	    }, function(reason) {
		console.log('Error: ' + reason.result.error.message);
	    });
	});
    }
};

/**
 * Initiate auth flow in response to user clicking authorize button.
 *
 * @param {Event} event Button click event.
 */
function handleAuthClick(event) {
    gapi.auth.authorize(
        {client_id: CLIENT_ID, scope: SCOPES, immediate: false},
        handleAuthResult);
    return false;
};

/**
 * Load Gmail API client library. List labels once client library
 * is loaded.
 */
function loadGmailApi() {
    gapi.client.load('gmail', 'v1', listLabels);
};

/**
 * Sign a user out
 * Source: https://developers.google.com/identity/sign-in/web/sign-in#get_profile_information
 */
function signOut(){
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function(){
    console.log('User signed out.');
  });
}


document.getElementById('teacher').addEventListener("click", handleAuthClick);
document.getElementById('student').addEventListener("click", handleAuthClick);
