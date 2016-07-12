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

  var public_rooms_channel = pusher.subscribe('public-public_rooms');
  public_rooms_channel.bind('new_room_event', function(room) {
    $('.public-rooms').prepend(
      "<li class='public-room list-group-item' data-room-id='" + room.id + "' data-room-channel='" + room.channel + "' data-room-name='" + room.name + "'>" +
        room.name + "<span class='public-room-count badge'>0</span>" +
      "</li>"
    );
  })


  $('.add-public-room').popover({
    html: true,
    content: "<form class='form-public-room'><input type='text' class='new-name-public-room form-control' placeholder='New room name...' /></form>",
    container: 'body',
    trigger: 'manual'
  });

  $('.add-public-room').on('click', function() {
    $('.add-public-room').popover('show');
    $('.form-public-room input').focus();
  });

  $(document).on('submit', '.form-public-room', function(event) {
    event.preventDefault();

    $.ajax({
      type: 'POST',
      url: '/public_rooms',
      data: {
        name: $('.new-name-public-room').val()
      },
      dataType: 'json'
    });

    $('.add-public-room').popover('hide');
  })

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
      csrftoken: csrfToken
    });
  });

});
