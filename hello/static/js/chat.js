$(function() {

  var subscribed = false;
  $("#ok").prop('disabled', true);

  var pusher = new Pusher(ENV['PUSHER_APP_KEY'], {
    encrypted: true
  });

  var channel = pusher.subscribe('chat_channel');
  channel.bind('message_event', function(data) {
    $('#messages').append('<li>' + data.message + '</li>');
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

    var message = $('#message').val();
    if (message.trim() === '') {
      return;
    }
    $('#message').val('');

    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
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
