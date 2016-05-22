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
    if (authResult && !authResult.error) {
	if(authResult.hd === "stuy.edu"){
	    gapi.client.load('plus', 'v1').then(function() {
		var request = gapi.client.plus.people.get({
		    'userId': 'me'
		})
		
		request.then(function(resp) {
		    $.getJSON("/add_user", {
			username: resp.result.displayName,
			email: resp.result.emails[0].value
		    }).done(function(){
			window.location.reload();
		    });
		}, function(reason) {
		    console.log('Error: ' + reason.result.error.message);
		});
	    });
	}else{
	    signOut();
	}
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
 * Source: http://stackoverflow.com/a/32892148
 */
function signOut(){
    
    var token = gapi.auth.getToken();
    if (token) {
	var accessToken = gapi.auth.getToken().access_token;
	if (accessToken) {
	    xhttp.open("GET", 'https://accounts.google.com/o/oauth2/revoke?token=' + accessToken, true);
	}
    }
    gapi.auth.setToken(null);
    gapi.auth.signOut();
}

