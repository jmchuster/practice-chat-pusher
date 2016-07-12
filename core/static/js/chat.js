$(function() {

  var subscribed = false;
  $("#ok").prop('disabled', true);

  var pusher = new Pusher(ENV['PUSHER_APP_KEY'], {
    encrypted: true,
    authEndpoint: '/auth',
    auth: {
      headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
      }
    }
  });

  var timeToString = function(time) {
      return (time.getHours() % 12 || 12)  + ':' + time.getMinutes() + ' ' + (time.getHours() >= 12 ? 'AM' : 'PM');
  };

  var addMessage = function(data) {
    $('#messages').append(
      '<li>' +
        data.username + ' (' + timeToString(new Date(data.timestamp)) + '): ' + data.message +
      '</li>');
  };

  var addMember = function(member, newMember) {
    $('#users').prepend(
      "<li class='user' data-id='" + member.id + "'>" +
        member.info.username +
      '</li>');
    if (newMember === true) {
      $('.user[data-id=' + member.id + ']')
        .addClass('strong')
        .prepend("<i class='fa fa-fw fa-sign-in'></i>");
      window.setTimeout(function() {
        $('.user[data-id=' + member.id + ']').removeClass('strong');
        $('.user[data-id=' + member.id + '] i').remove();
      }, 2 * 1000);

      $('#messages').append(
        '<li><i>' +
          member.info.username + ' has joined the room (' + timeToString(new Date()) + ')' +
        '</i></li>');
    }
  };

  var removeMember = function(member) {
    $('.user[data-id=' + member.id + '] i').remove();
    $('.user[data-id=' + member.id + ']')
      .addClass('text-muted')
      .append("<i class='fa fa-fw fa-sign-out'></i>");
    window.setTimeout(function() {
      $('.user[data-id=' + member.id + ']').remove();
    }, 2 * 1000);
    $('#messages').append(
      '<li><i>' +
        member.info.username + ' has left the room (' + timeToString(new Date()) + ')' +
      '</i></li>');
  };

  var channel = pusher.subscribe('presence-chat_channel');
  channel.bind('message_event', function(data) {
    addMessage(data);
  });
  channel.bind('pusher:subscription_succeeded', function(members) {
    var me = channel.members.me;
    var userId = me.id;
    $('#username').val(me.info.username);

    $('#user-count').html(Math.max(0, members.count - 1));
    members.each(function(member) {
      if (member.id !== userId) {
        addMember(member);
      }
    });

    $('#messages').append(
      '<li><i>' +
        'You have joined the room (' + timeToString(new Date()) + ')' +
      '</i></li>');

    subscribed = true;
    $("#ok").prop('disabled', false);
  });
  channel.bind('pusher:member_added', function(member) {
    addMember(member, true);
    $('#user-count').html(Math.max(0, channel.members.count - 1));
  });
  channel.bind('pusher:member_removed', function(member) {
    removeMember(member);
    $('#user-count').html(Math.max(0, channel.members.count - 1));
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
