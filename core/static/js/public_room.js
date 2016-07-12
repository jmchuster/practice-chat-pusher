function PublicRoom(config) {

  this.pusher = config.pusher;
  this.roomId = config.roomId,
  this.roomChannel = config.roomChannel,
  this.roomName = config.roomName,
  this.roomTemplate = config.roomTemplate,
  this.$roomContainer = config.roomContainer;
  this.csrftoken = config.csrftoken;

  this.init();
  this.initChannel();
}

PublicRoom.prototype.init = function() {
  this.$roomContainer.append(
    this.roomTemplate({
      'room-id': this.roomId,
      'room-channel': this.roomChannel,
      'room-name': this.roomName
    })
  );

  this.$panel = $('.public-room-panel[data-room-id=' + this.roomId + ']');
  this.$panelBody = this.$panel.find('.panel-body');
  this.$userCount = this.$panel.find('.user-count');
  this.$users = this.$panel.find('.users');
  this.$messages = this.$panel.find('.messages');
  this.$message = this.$panel.find('.message');
  this.$btnSend = this.$panel.find('.send');
  this.$form = this.$panel.find('form');
  this.$status = this.$panel.find('.status');
  this.subscribed = false;

  this.$message.focus();

  this.$form.on('submit', $.proxy(this.submitForm, this));

  this.$btnHide = this.$panel.find('.hide-panel');
  this.$btnShow = this.$panel.find('.show-panel');
  this.$btnClose = this.$panel.find('.close-panel');

  this.$btnHide.on('click', $.proxy(this.hidePanel, this));
  this.$btnShow.on('click', $.proxy(this.showPanel, this));
  this.$btnClose.on('click', $.proxy(this.closePanel, this));
}

PublicRoom.prototype.initChannel = function() {
  this.channel = this.pusher.subscribe(this.roomChannel);
  this.channel.bind('pusher:subscription_succeeded', $.proxy(this.onSubscriptionSucceeded, this));
  this.channel.bind('pusher:member_added', $.proxy(this.onMemberAdded, this));
  this.channel.bind('pusher:member_removed', $.proxy(this.onMemberRemoved, this));
  this.channel.bind('message_event', $.proxy(this.onMessageEvent, this));
}

PublicRoom.prototype.hidePanel = function() {
  this.$panelBody.slideUp();
}

PublicRoom.prototype.showPanel = function() {
  this.$panelBody.slideDown();
}

PublicRoom.prototype.closeChannel = function() {
  this.channel.unbind('pusher:subscription_succeeded');
  this.channel.unbind('pusher:member_added');
  this.channel.unbind('pusher:member_removed');
  this.channel.unbind('message_event');
  this.pusher.unsubscribe(this.roomChannel);
}

PublicRoom.prototype.closePanel = function() {
  this.closeChannel();
  this.$panel.remove();
}

PublicRoom.prototype.timeToString = function(time) {
  return (time.getHours() % 12 || 12)  + ':' + ('00' + time.getMinutes()).slice(-2) + ' ' + (time.getHours() >= 12 ? 'AM' : 'PM');
};

PublicRoom.prototype.onSubscriptionSucceeded = function(members) {
  var me = this.channel.members.me;
  var userId = me.id;

  this.$userCount.html(members.count);
  members.each($.proxy(this.addMember, this));

  this.$messages.append(
    '<li><i>' +
      'You have joined the room (' + this.timeToString(new Date()) + ')' +
    '</i></li>');

  this.subscribed = true;
  this.$btnSend.prop('disabled', false);
};

PublicRoom.prototype.onMemberAdded = function(member) {
  this.addMember(member, true);
  this.$userCount.html(this.channel.members.count);
}

PublicRoom.prototype.onMemberRemoved = function(member) {
  this.removeMember(member);
  this.$userCount.html(this.channel.members.count);
}

PublicRoom.prototype.addMember = function(member, newMember) {
  this.$users.prepend(
    "<li class='user' data-id='" + member.id + "'>" +
      member.info.username +
    '</li>');
  if (newMember === true) {
    this.$users.find('.user[data-id=' + member.id + ']')
      .addClass('strong')
      .prepend("<i class='fa fa-fw fa-sign-in'></i>");
    window.setTimeout($.proxy(function() {
      this.$users.find('.user[data-id=' + member.id + ']').removeClass('strong');
      this.$users.find('.user[data-id=' + member.id + '] i').remove();
    }, this), 2 * 1000);

    this.$messages.append(
      '<li><i>' +
        member.info.username + ' has joined the room (' + this.timeToString(new Date()) + ')' +
      '</i></li>');
  }
};

PublicRoom.prototype.removeMember = function(member) {
  this.$users.find('.user[data-id=' + member.id + '] i').remove();
  this.$users.find('.user[data-id=' + member.id + ']')
    .addClass('text-muted')
    .append("<i class='fa fa-fw fa-sign-out'></i>");
  window.setTimeout($.proxy(function() {
    this.$users.find('.user[data-id=' + member.id + ']').remove();
  }, this), 2 * 1000);
  this.$messages.append(
    '<li><i>' +
      member.info.username + ' has left the room (' + this.timeToString(new Date()) + ')' +
    '</i></li>');
};

PublicRoom.prototype.onMessageEvent = function(data) {
  this.$messages.append(
    '<li>' +
      data.username + ' (' + this.timeToString(new Date(data.timestamp)) + '): ' + data.message +
    '</li>');
};

PublicRoom.prototype.submitForm = function() {
  event.preventDefault();

  if (this.subscribed === false) {
    return;
  }

  var message = this.$message.val().trim();
  if (message === '') {
    return;
  }
  this.$message.val('');

  $.ajax({
    type: 'POST',
    url: this.$form.attr('action'),
    data: {
      csrfmiddlewaretoken: this.csrftoken,
      message: message
    },
    dataType: 'json',
    success: $.proxy(function(data) {
      this.$status.removeClass('text-danger').text('Last message sent at ' + this.timeToString(new Date()) + '.')
    }, this),
    error: $.proxy(function(jqXHR, textStatus, errorThrown) {
      this.$status.addClass('text-danger').text('There was an error sending your message (' + this.timeToString(new Date()) + ').')
    }, this)
  });
};
