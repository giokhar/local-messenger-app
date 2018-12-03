var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

function messageTime(){
  // Function that returns the time message was received
  return new Date().getHours() + ":" + ('0'+new Date().getMinutes()).slice(-2);
}


socket.on( 'connect', function() {

  var form = $( 'form' ).on( 'submit', function( e ) {
    e.preventDefault()
    let id = $('.reply').attr('id').replace("reply-", "");
    let user_input = $( '.reply' ).val()
    socket.emit( 'my event', {
      id : id,
      text : user_input
    } )
  } )
} );

// When user joins it add to the panel on the left
socket.on( 'user_joined', function( data ) {
  $( 'div.panel-col' ).append( '<div class="recent-user" id="'+data.id+'"><div class="recent-avatar"><img src="static/img/2.jpg" class="a0uk"></div><div class="chat-name-recent-message"><div class="recent-user-name">'+data.username+'</div><div class="recent-user-message">No messages yet...</div></div><div class="message-count"></div></div>' )
  $( 'div.messages--wrap').append( $('<div class="messages-body" id="messages-body-'+data.id+'"></div>').hide())
});

// When user sends you a message
socket.on( 'message_received', function( data ) {
  $( 'div#messages-body-'+data.id).append( '<div class="msg"><div class="message-reply-body friend"><div class="message-text">'+data.text+'</div><div class="message-time">'+messageTime()+'</div></div></div>' );
  if ($("#"+data.id).css("background-color") != "rgb(0, 135, 213)"){ // If the tab is currently active don't make messages bold
    $("#"+data.id).find('.recent-user-message').text(data.text).css("font-weight", "700");
    $("#"+data.id).find('.recent-user-name').css("font-weight", "700");
  }
  let user_info = $("#"+data.id);
  $("#"+data.id).remove();
  $( 'div.panel-col' ).prepend(user_info.show(300));
  if ($("#"+data.id).find(".message-count").length){
    let count = $("#"+data.id).find('.count');
    count.text(parseInt(count.text())+1);
  } else { $("#"+data.id).append('<div class="message-count"><div class="count">1</div></div>');}
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
});

socket.on( 'message_sent', function( data ) {
  console.log( data )
  $( 'div#messages-body-'+data.id).append( '<div class="data"><div class="message-reply-body you_"><div class="message-text">'+data.text+'</div><div class="message-time">'+messageTime()+'</div></div></div>' )
  $('.reply').val(''); // Reset the textbox after sending a message
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
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
  $( '.reply' ).attr('id', 'reply-'+$(this).attr('id'));
  $('div.messages-body').not("#messages-body-"+$(this).attr('id')).hide();
  $("div.recent-user").css("background-color", "#31ACF3")
  $(this).css("background-color","#0087D5");
  $(this).find('.recent-user-name').css("font-weight", "100");
  $(this).find('.recent-user-message').css("font-weight", "100");
  $('div.panel-username').text($(this).find('.recent-user-name').text());
  $('div.panel-chat-avatar img').attr('src', $(this).find('.recent-avatar img').attr('src')).hide().show(500);
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
});