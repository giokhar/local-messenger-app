var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

$(document).ready(function(){
  $('div.messages-body').hide(); // When page loads, hide the body of every chat by default
});

function messageTime(){
  // Function that returns the time message was received
  return new Date().getHours() + ":" + ('0'+new Date().getMinutes()).slice(-2); // get the current hour and minute in this format 00:00
}

socket.on( 'connect', function() {
  var form = $( 'form' ).on( 'submit', function( e ) { // when user sends a message invoke socketio for back-end
    e.preventDefault();
    socket.emit( 'my_event', {
      id : $('.reply').attr('id').replace("reply-", ""), // get the 'id' from 'reply-id'
      text : $( '.reply' ).val() // get the text typed by the user
    })
  })
});

// // when user sends a message invoke socketio for front-end
socket.on( 'message_sent', function( data ) {
  $( 'div#messages-body-'+data.id).append( '<div class="msg"><div class="message-reply-body you_"><div class="message-text">'+data.text+'</div><div class="message-time">'+messageTime()+'</div></div></div>' ) // append the element when message is sent
  $("#"+data.id).find('.recent-user-message').text(data.text); // change the recent message value in the panel
  $('.reply').val(''); // Reset the textbox after sending a message
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
});

// When user sends you a message
socket.on( 'message_received', function( data ) {
  $( 'div#messages-body-'+data.id).append( '<div class="msg"><div class="message-reply-body friend"><div class="message-text">'+data.text+'</div><div class="message-time">'+messageTime()+'</div></div></div>' ); // append the message received in the chatroom 
  if ($("#"+data.id).css("background-color") != "rgb(0, 135, 213)"){ // If the tab is currently active don't make messages bold
    $("#"+data.id).find('.recent-user-message').text(data.text).css("font-weight", "700"); // make new message bold
    $("#"+data.id).find('.recent-user-name').css("font-weight", "700"); // make new message username bold
  }
  let user_info = $("#"+data.id);
  $("#"+data.id).remove(); // remove the username from the panel for prepending
  $( 'div.panel-col' ).prepend(user_info.show(300)); // prepend the new messages on top 
  if ($("#"+data.id).find(".message-count").length){ // check if there is a counter already created
    let count = $("#"+data.id).find('.count'); 
    count.text(parseInt(count.text())+1); // increase the counter when new message comes
  } else { $("#"+data.id).append('<div class="message-count"><div class="count">1</div></div>');} // create the counter if there is no unread messages
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
});


// When user joins it add to the panel on the left
socket.on( 'user_joined', function( data ) {
  let default_message = "Just joined the network"; // default message shown on the panel when user joins
  let icon = "static/img/2.jpg";
  $( 'div.panel-col' ).append( '<div class="recent-user" id="'+data.id+'"><div class="recent-avatar"><img src="'+icon+'" class="a0uk"></div><div class="chat-name-recent-message"><div class="recent-user-name">'+data.username+'</div><div class="recent-user-message">'+default_message+'</div></div><div class="message-count"></div></div>' ) // append new avatar and user info when new use joins
  $( 'div.messages--wrap').append( $('<div class="messages-body" id="messages-body-'+data.id+'"></div>').hide()) // hide the created chatroom body by default
  $("#"+data.id).find('.recent-user-name').css("font-weight", "700"); // bold the opened username
  $("#"+data.id).find('.recent-user-message').css("font-weight", "700"); // bold the opened message
});

// When click username it will open the appropriate chatbox
$(document).on('click', 'div.recent-user', function()
{
  $('div.messages-body').show(700); // show all the messages before hiding all except one
  $('div.message-textbox').show(); // show textbox only when we click on a user
  $( '.reply' ).val( '' ).focus(); // automatically focus on the textbox
  $( '.reply' ).attr('id', 'reply-'+$(this).attr('id')); // reply-id matters to send the message to the right person
  $('div.messages-body').not("#messages-body-"+$(this).attr('id')).hide(); // hide all except the one we want
  $("div.recent-user").css("background-color", "#31ACF3") // change all the colors to default
  $(this).css("background-color","#0087D5"); // make the chosen user darker
  $(this).find('.recent-user-name').css("font-weight", "100"); // unbold the opened username
  $(this).find('.recent-user-message').css("font-weight", "100"); // unbold the opened message
  $('div.panel-username').text($(this).find('.recent-user-name').text()); // change the username on top
  $('div.panel-chat-avatar img').attr('src', $(this).find('.recent-avatar img').attr('src')).hide().show(500); // change the avatar on top
  $(this).find(".message-count").remove(); // remove the counter badge when we open the message
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
});