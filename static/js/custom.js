var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);


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
    $( '.reply' ).val( '' ).focus()
  } )
} );

socket.on( 'my response', function( data ) {
  console.log( data )
  let time = new Date().getHours() + ":" + ('0'+new Date().getMinutes()).slice(-2);
  if (data.my_message !== undefined) {
    $( 'div.messages-body' ).append( '<div class="data"><div class="message-reply-body you_"><div class="message-text">'+data.my_message+'</div><div class="message-time">'+time+'</div></div></div>' )
  }
  if (data.friend_message !== undefined){
    $( 'div.messages-body' ).append( '<div class="data"><div class="message-reply-body friend"><div class="message-text">'+data.friend_message+'</div><div class="message-time">'+time+'</div></div></div>' )
  }
  if (data.new_user !== undefined){
    $( 'div.panel-col' ).append( '<div class="recent-user" id="'data.new_user'"><div class="recent-avatar"><img src="static/img/2.jpg" class="a0uk"></div><div class="chat-name-recent-message"><div class="recent-user-name">'+data.new_user+'</div><div class="recent-user-message">No messages yet...</div></div><div class="message-count"></div></div>' )
  }
  // Always scroll down when message sent
  $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER)
});