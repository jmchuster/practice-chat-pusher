function PublicRoomList(config) {
  this.pusher = config.pusher;

  this.$publicRooms = config.publicRooms;
  this.$roomContainer = config.roomContainer;
  this.$btnAddPublicRoom = config.btnAddPublicRoom;
  this.roomTemplate = config.roomTemplate;

  this.init();
  this.initChannel();
}

PublicRoomList.prototype.init = function() {
  this.$publicRooms.on('click', '.public-room', $.proxy(this.subscribeRoom, this));

  this.$btnAddPublicRoom.popover({
    html: true,
    content: "<form class='form-public-room'><input type='text' class='new-name-public-room form-control' placeholder='New room name...' /></form>",
    container: 'body',
    trigger: 'manual'
  });
  this.$btnAddPublicRoom.on('click', $.proxy(this.addPublicRoom, this));
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
}

PublicRoomList.prototype.initChannel = function() {
  this.channel = this.pusher.subscribe('public-public_rooms');
  this.channel.bind('new_room_event', $.proxy(this.newRoomEvent, this));
  this.channel.bind('room_count_event', $.proxy(this.roomCountEvent, this));
}

PublicRoomList.prototype.newRoomEvent = function(room) {
  this.$publicRooms.prepend(
    "<li class='public-room list-group-item' data-room-id='" + room.id + "' data-room-channel='" + room.channel + "' data-room-name='" + room.name + "'>" +
      room.name + "<span class='public-room-count badge'>0</span>" +
    "</li>"
  );
}

PublicRoomList.prototype.roomCountEvent = function(room) {
  this.$publicRooms.find(".public-room[data-room-channel='" + room.channel + "'] .badge").text(room.count);
}

PublicRoomList.prototype.subscribeRoom = function(event) {

  var roomId = $(event.target).attr('data-room-id');
  var roomChannel = $(event.target).attr('data-room-channel');
  var roomName = $(event.target).attr('data-room-name');

  // already opened and running
  var roomPanel = this.$publicRooms.find('.public-room-panel[data-room-id=' + roomId + ']');
  if (roomPanel.length > 0) {
    $('html, body').animate({
        scrollTop: roomPanel.offset().top
    }, 1000);
    return;
  }

  new PublicRoom({
    pusher: this.pusher,
    roomId: roomId,
    roomChannel: roomChannel,
    roomName: roomName,
    roomTemplate: this.roomTemplate,
    roomContainer: this.$roomContainer
  });

}

PublicRoomList.prototype.addPublicRoom = function() {
  this.$btnAddPublicRoom.popover('show');
  $('.form-public-room input').focus();
}
