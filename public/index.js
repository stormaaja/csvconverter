function setLoggedOut() {
  $('#currentUsername').text("");
  $('#logout').hide();
  $('#loginForm').show();
  $("#log *").prop("disabled", true);
  $("#log").addClass("disabled");
}

function setLoggedIn(user) {
  $('#currentUsername').text(user);
  $('#logout').show();
  $('#loginForm').hide();
  $("#log *").prop("disabled", false);
  $("#log").removeClass("disabled");
}

function getStatus(success) {
  $.get('/status', function(data) {
    success(data);
  });
}

function watchStatus() {
  getStatus(function(status) {
    $('#status').text(status["message"]);
    if (status["code"] === 1) {
      setTimeout(function(){ watchStatus(); }, 3000);
    }
  });
}

$('#buttonLogin').on('click', function() {
  $.post('/session', {
      username: $('#username').val(), password: $('#password').val() })
  .done(function(data) {
    $('#textAreaLog').text("Logged in");
    setLoggedIn(data);
    watchStatus();
  }).fail(function(data) {
    $('#textAreaLog').text("Login failed: " + data.responseText);
  });
});

$('#buttonStartUpdate').on('click', function() {
  $.post('/update')
  .done(function(data) {
    $('#textAreaLog').text(data);
    watchStatus();
  }).fail(function(data) {
    $('#textAreaLog').text("Login failed: " + data.responseText);
  });
});

$('#buttonLogout').on('click', function() {
  $.ajax({
    type: "DELETE",
    url: '/session',
    success: function() {
      setLoggedOut();
      $('#textAreaLog').text("Logged out");
    },
    fail: function() { $('#textAreaLog').text("Logout failed"); }
  });
});

$('#loadLogButton').on('click', function() {
  var url = "/log?info=" + $('#filterInfo').is(':checked')
    + "&warning=" +  $('#filterWarning').is(':checked')
    + "&error=" +  $('#filterError').is(':checked');

  $.get(url, function(data) {
    if (data.length > 0) {
      $('#textAreaLog').text(data);
    } else {
      $('#textAreaLog').text("No lines to show");
    }
  }).fail(function(data) {
    $('#textAreaLog').text(data.responseText);
    if (data.status === 401) {
      setLoggedOut();
    }
  });
});

$(function() {
  $.get('/session', function(data) {
    setLoggedIn(data);
    watchStatus();
  }).fail(function(data) {
    if (data.status === 401) {
      setLoggedOut();
    }
  });
});
