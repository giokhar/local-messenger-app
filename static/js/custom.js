var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

function messageTime(){
  // Function that returns the time message was received
  return new Date().getHours() + ":" + ('0'+new Date().getMinutes()).slice(-2);
}


socket.on( 'connect', function() {
  socket.emit( 'my event', {
    data: 'User Connected'
  } )
  var form = $( 'form' ).on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = location.search.split('username=')[1];
    let user_input = $( '.reply' ).val()
    socket.emit( 'my event', {
      user_name : user_name,
      my_message : user_input
    } )
  } )
} );

socket.on( 'my_response', function( data ) {
  console.log( data )
  if (data.my_message !== undefined) {
    $( 'div.messages-body' ).append( '<div class="data"><div class="message-reply-body you_"><div class="message-text">'+data.my_message+'</div><div class="message-time">'+time+'</div></div></div>' )
  }
  // Always scroll down when message sent
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER)
});

// When user joins it add to the panel on the left
socket.on( 'user_joined', function( data ) {
  $( 'div.panel-col' ).append( '<div class="recent-user" id="'+data.id+'"><div class="recent-avatar"><img src="static/img/2.jpg" class="a0uk"></div><div class="chat-name-recent-message"><div class="recent-user-name">'+data.username+'</div><div class="recent-user-message">No messages yet...</div></div><div class="message-count"></div></div>' )
  $( 'div.messages--wrap').append( $('<div class="messages-body" id="messages-body-'+data.id+'"></div>').hide())
});

// When user sends you a message
socket.on( 'message_received', function( data ) {
  $( 'div#messages-body-'+data.id).append( '<div class="msg"><div class="message-reply-body friend"><div class="message-text">'+data.text+'</div><div class="message-time">'+messageTime()+'</div></div></div>' );
  $("#"+data.id).find('.recent-user-message').text(data.text).css("font-weight", "700");
  $("#"+data.id).find('.recent-user-name').css("font-weight", "700");
  let user_info = $("#"+data.id);
  $("#"+data.id).remove();
  $( 'div.panel-col' ).prepend(user_info.show(300));
  if ($("#"+data.id).find(".message-count").length){
    let count = $("#"+data.id).find('.count');
    count.text(parseInt(count.text())+1);
  } else { $("#"+data.id).append('<div class="message-count"><div class="count">1</div></div>');}
});


$(document).ready(function(){
$('div.messages-body').hide(); // When page loads, hide body of every chat
});
// When click username it will open the appropriate chatbox
$(document).on('click', 'div.recent-user', function()
{
  $('div.messages-body').show(700);
  $('div.message-textbox').show();
  $( '.reply' ).val( '' ).focus();
  $('div.messages-body').not("#messages-body-"+$(this).attr('id')).hide();
  $("div.recent-user").css("background-color", "#31ACF3")
  $(this).css("background-color","#0087D5");
  $(this).find('.recent-user-name').css("font-weight", "100");
  $(this).find('.recent-user-message').css("font-weight", "100");
  $('div.panel-username').text($(this).find('.recent-user-name').text());
  $('div.panel-chat-avatar img').attr('src', $(this).find('.recent-avatar img').attr('src')).hide().show(500);
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER)
});