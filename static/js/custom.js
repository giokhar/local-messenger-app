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
      message : user_input
    } )
    $( '.reply' ).val( '' ).focus()
  } )
} );

socket.on( 'my response', function( msg ) {
  console.log( msg )
  let time = new Date().getHours() + ":" + new Date().getMinutes();
  if( typeof msg.user_name !== 'undefined' && msg.message != '' ) {
    $( 'div.messages-body' ).append( '<div class="msg"><div class="message-reply-body you_"><div class="message-text">'+msg.message+'</div><div class="message-time">'+time+'</div></div></div>' )
    // Always scroll down when message sent
    $('.messages--wrap').scrollTop(Number.MAX_SAFE_INTEGER)
  }
});