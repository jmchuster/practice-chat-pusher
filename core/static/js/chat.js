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
    var roomPanel = $('.public-room-panel[data-room-id=' + roomId + ']');
    if (roomPanel.length > 0) {
      $('html, body').animate({
          scrollTop: roomPanel.offset().top
      }, 1000);
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
