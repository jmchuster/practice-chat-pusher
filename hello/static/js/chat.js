$(function() {

  var subscribed = false;
  $("#ok").prop('disabled', true);

  var pusher = new Pusher(ENV['PUSHER_APP_KEY'], {
    encrypted: true
  });

  var channel = pusher.subscribe('chat_channel');
  channel.bind('message_event', function(data) {
    var date = new Date(data.timestamp);
    var dateString = (date.getHours() % 12 || 12)  + ':' + date.getMinutes() + ' ' + (date.getHours() >= 12 ? 'AM' : 'PM');
    $('#messages').append(
      '<li>' +
        data.username + ' (' + dateString + '): ' + data.message +
      '</li>');
  });
  channel.bind('pusher:subscription_succeeded', function() {
    subscribed = true;
    $("#ok").prop('disabled', false);
  });

  $('form').submit(function(event) {
    event.preventDefault();

    if (subscribed === false) {
      return;
    }

    var username = $('#username').val().trim();

    var message = $('#message').val().trim();
    if (message === '') {
      return;
    }
    $('#message').val('');

    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        username: username,
        message: message
      },
      dataType: 'json',
      success: function(data) {
        console.log(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        // do nothing
      },
      complete: function(jqXHR, textStatus) {
        // do nothing
      }
    });
  });

});
