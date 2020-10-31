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

  $(".add-to-cart").click(function(e){
      e.preventDefault();
      let id = $(this).closest('.enclosing').attr('id');
      add_to_cart(id);
  });

  $(".increase-item").click(function(e){
      e.preventDefault();
      let id = $(this).closest('.enclosing').attr('id');
      let div = $(this).closest('.enclosing');
      increase_item(id, div);
  });

  $(".decrease-item").click(function(e){
      e.preventDefault();
      let id = $(this).closest('.enclosing').attr('id');
      let div = $(this).closest('.enclosing');
      decrease_item(id, div);
  });

// document ready
});

function add_to_cart(id) {
    $.ajax({
        type: 'GET',
        url: '/account/cart/add/' + id,
        success: function (response) {
            location.reload(true)
            $('#' + id).focus()
        },
        error: function (response) {
            console.log("Not Good")
        }
    })
};

function increase_item(id, div) {
    $.ajax({
        type: 'GET',
        url: '/account/cart/add/' + id,
        success: function (response) {
            let input = div.find('.quantity')
            input.val(response['quantity'])
        },
        error: function (response) {
            console.log("Not Good")
        }
    })
};

function decrease_item(id, div) {
    $.ajax({
        type: 'GET',
        url: '/account/cart/decrease/' + id,
        success: function (response) {
            if (response['quantity'] > 0){
                let input = div.find('.quantity')
                input.val(response['quantity'])
            } else {
                location.reload(true)
                $('#' + id).focus()
            }
        },
        error: function (response) {
            console.log("Not Good")
        }
    })
};