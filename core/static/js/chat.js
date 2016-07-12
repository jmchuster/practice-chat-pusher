$(function() {

  var source   = $("#room-template").html();
  var roomTemplate = Handlebars.compile(source);
  var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

  $.ajaxSetup({
    headers: {
      'X-CSRFToken': csrfToken
    }
  });

  var pusher = new Pusher(ENV['PUSHER_APP_KEY'], {
    encrypted: true,
    authEndpoint: '/auth',
    auth: {
      headers: {
        'X-CSRFToken': csrfToken
      }
    }
  });

  new PublicRoomList({
    pusher: pusher,
    publicRooms: $('.public-rooms'),
    roomContainer: $('.room-container'),
    btnAddPublicRoom: $('.add-public-room'),
    roomTemplate: roomTemplate
  });

});
