// JavaScript Document
$(document).ready(function() {
   $('.social, .report, .more, .list-chat-send-message, .list-chat-message-control, .mobile-header-menu-btn, .feelingbox, .language-button').dropdown({
      inDuration: 300,
      outDuration: 225,
      constrain_width: false, // Does not change width of dropdown to that of the activator
      hover: false, // Activate on hover
      gutter: 0, // Spacing from edge
      belowOrigin: true
   });
   // Chat Page Panel Control
   $('.panel-chat-mobile-btn').sideNav({
      menuWidth: 300, // Default is 240
      edge: 'left', // Choose the horizontal origin
      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
      draggable: true // Choose whether you can drag to open on touch screens
   });
   // Propagetion Control
   $('.feelingList-content, .collapsible, .tabs').on('click', function(event) {
      event.stopPropagation();
   });
   // This tab is for chat page control
   // If you change the ul.tabs class name or if you ant to change the buttom border color active tabs selector
   // You should change also this class name like ul.yourClass
   $('ul.tabs').tabs();
   // This tab is for profile and newsfeed page control
   // If you change the ul.tabs-post class name or if you ant to change the buttom border color active tabs selector
   // You should change also this class name like ul.yourClass
   $('ul.tabs-post').tabs();
   // Tooltip control
   // If you add some other tooltip like hoverover user avatar then you can see username with tooltip
   $('.fm, .sign-in-with').tooltip({
      delay: 50
   });
   // This is image popup box. If you want to activate some other popup image you should add the class name here
   // Like  $('materialboxed, .yournewclass').materialbox();.
   $('.materialboxed').materialbox();
   // Carousel slider. You can see this carousel from game page, video page ect.
   // If you want to add some other class named carousel you should add that class name here
   $('.carousel.carousel-slider, .carousel-game.carousel-game-slider').carousel({
      full_width: true
   });
   // This js working just in videos page first click show other recommended videos and second click hide other shoed videos
   $("body").on("click", ".more-video-Button", function() {
      $(".video-recommended").toggleClass("active");
      $(".more-video-Button").text($(".more-video-Button").text() === "Show more" ? "Show less" : "Show more");
   });
   // Media player is here working with video and mp3,mp4 formats
   // You can change the width and height here
   $('audio,video').mediaelementplayer({

      audioWidth: '100%',
      audioHeight: 30
   });
   $('audio,video').mediaelementplayer({
      //mode: 'shim',
      success: function(player, node) {
         $('#' + node.id + '-mode').html('mode: ' + player.pluginType);
      }
   });
   // Collabse is here
   // Working on feeling section when you click feeling button then you see the collapsible box
   // If you want to change the class name you should change also this class name .collapsible
   $('.collapsible').collapsible();
   $('.chips').material_chip();
   /*Post Form Modal Box STARTED*/
   $('.modal').modal();
   $('.postType').modal({
      dismissible: true, // Modal can be dismissed by clicking outside of the modal
      opacity: .5, // Opacity of modal background
      in_duration: 300, // Transition in duration
      out_duration: 200, // Transition out duration
      starting_top: '4%', // Starting top style attribute
      ending_top: '10%', // Ending top style attribute
      ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
         $('#mod1').modal('open');
      },
      complete: function() {
            $('#mod1').modal('close');
         } // Callback for Modal close
   });

   $('.feelingbox').modal({
      dismissible: true, // Modal can be dismissed by clicking outside of the modal
      opacity: .5, // Opacity of modal background
      in_duration: 300, // Transition in duration
      out_duration: 200, // Transition out duration
      starting_top: '4%', // Starting top style attribute
      ending_top: '10%', // Ending top style attribute
      ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
         $('#mod2').modal('open');
      },
      complete: function() {
            $('#mod2').modal('close');
         } // Callback for Modal close
   });
   /*Post Form Modal Box FINISHED*/
   /*Left Sidebar Menu OPEN CLOSE STARTED*/
   $('body').on('click', '.logo', function() {
      var navPosition = $(this).attr('data-position');
      $('.left-sidebar-menu').addClass('open');
      $('body').addClass('menu-open');
      return false;
   });

   //
   // Use the javascript below when implementing. The code above is for demo purposes only.
   //
   // $('.menu').click(function() {
   //   $('nav').addClass('open');
   //   $('body').addClass('menu-open');
   //   return false;
   // });

   $(document).click(function() {
      $('body').removeClass('menu-open');
      $('.left-sidebar-menu').removeClass('open');
   });
  
   // Starting hover effect
   // When user hovering .star div
   // This code will toggleing rate-btn-hover
   $(".star").hover(
      function() {
         // Increase the stars if hovering more then one
         var prevStars = $(this).prevAll();
         // Add rate-btn-hover
         prevStars.toggleClass('rate-btn-hover');
      }
   );
   // Activate the rated star
   $("body").on("click", ".star", function() {
      // Add rate-btn-active if clicked
      $(this).siblings().removeClass('rate-btn-active')
         // Check if changed the star
      var prevStars = $(this).prevAll().addBack();
      // Add rated star on prevStars
      prevStars.addClass('rate-btn-active');
   });
   if (!document.querySelectorAll) {
      document.querySelectorAll = function(selectors) {
         var style = document.createElement('style'),
            elements = [],
            element;
         document.documentElement.firstChild.appendChild(style);
         document._qsa = [];

         style.styleSheet.cssText = selectors + '{x-qsa:expression(document._qsa && document._qsa.push(this))}';
         window.scrollBy(0, 0);
         style.parentNode.removeChild(style);

         while (document._qsa.length) {
            element = document._qsa.shift();
            element.style.removeAttribute('x-qsa');
            elements.push(element);
         }
         document._qsa = null;
         return elements;
      };
   }

   if (!document.querySelector) {
      document.querySelector = function(selectors) {
         var elements = document.querySelectorAll(selectors);
         return (elements.length) ? elements[0] : null;
      };
   }

   if (typeof String.prototype.trim !== 'function') {
      String.prototype.trim = function() {
         return this.replace(/^\s+|\s+$/g, '');
      }
   }

   var tabTogglers = document.querySelectorAll('div.header');

   for (var i = 0, len = tabTogglers.length; i < len; i++) {
      tabTogglers[i].onclick = function(e) {
         if (hasClass(this.parentNode.parentNode.parentNode, 'inactive')) removeClass(this.parentNode.parentNode.parentNode, 'inactive');
         else addClass(this.parentNode.parentNode.parentNode, 'inactive');
      };
   }

   function hasClass(elem, theClass) {
      var className = elem.className;
      if (className.indexOf(theClass) < 0) return false;
      else return true;
   }

   function addClass(elem, theClass) {
      var className = elem.className;
      className += ' ' + theClass;
      elem.className = className.trim();

      return false;
   }

   function removeClass(elem, theClass) {
      var className = elem.className;
      className = className.replace(theClass, '');
      elem.className = className.trim();

      return false;
   }
   autosize(document.querySelectorAll("form-control"));
});