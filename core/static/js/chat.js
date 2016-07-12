$(function() {

  var source   = $("#room-template").html();
  var roomTemplate = Handlebars.compile(source);

  var pusher = new Pusher(ENV['PUSHER_APP_KEY'], {
    encrypted: true,
    authEndpoint: '/auth',
    auth: {
      headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
      }
    }
  });

  $('.public-rooms').on('click', '.public-room', function() {

    var roomId = $(this).attr('data-room-id');
    var roomChannel = $(this).attr('data-room-channel');
    var roomName = $(this).attr('data-room-name');

    // already opened and running
    if ($('.public-room-panel[data-room-id=' + roomId + ']').length > 0) {
      return;
    }

    new PublicRoom({
      pusher: pusher,
      roomId: roomId,
      roomChannel: roomChannel,
      roomName: roomName,
      roomTemplate: roomTemplate,
      roomContainer: $('.room-container'),
      csrftoken: $('input[name=csrfmiddlewaretoken]').val()
    });
  });

});
