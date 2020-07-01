$(document).ready(function() {
 // executes when HTML-Document is loaded and DOM is ready
console.log("Document is ready");


  $( ".tileLanding" ).hover(
      function() {
        $(this).addClass('shadow-lg').css('cursor', 'pointer');
      }, function() {
        $(this).removeClass('shadow-lg');
      }
  );

  $(".contact-card").hover(
      function () {
        $(this).find('div .contact-info').css('color', 'white');
        $(this).find('div .contact-info-detail').css('color', 'white');
      }, function () {
        $(this).find('div .contact-info').css('color', '#007bff');
        $(this).find('div .contact-info-detail').css('color', '#444444');
      }
  );

// document ready
});