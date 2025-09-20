(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        } 
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    //owl navbar carousel
     $(".owl-navbar-carosel").owlCarousel({
      loop: true,
    //   margin: 10,
    //   nav: true,
      responsive: {
        0: {
          items: 3
        },
        600: {
          items: 3
        },
        1000: {
          items: 3
        }
      }
    });

    //category carousel
    $(".middle-nav-carousel .owl-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 6,
        nav : true,
        navText: [
        '<button class="btn rounded-circle custom-nav-btn"><i class="bi bi-arrow-left-short text-white"></i></button>',
        '<button class="btn rounded-circle custom-nav-btn"><i class="bi bi-arrow-right-short text-white"></i></button>'
    ],
        responsiveClass: true,
        responsive: {
            0: {
                items: 4
            },
            576: {
                items: 4
            },
            768: {
                items: 6
            },
            992: {
                items: 7
            },
            1200: {
                items: 7
            }
        }
    });
    // Treding carousel & New arraible same
    $(".trending-product-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-right"></i>',
            '<i class="bi bi-arrow-left"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:2
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });


    

    // Modal Video
    


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });


    // ajax load category
    
    // 

})(jQuery);





  // Run once on initial load
  document.addEventListener('DOMContentLoaded', initializePageScripts);

  // Re-run every time HTMX swaps in content
  document.body.addEventListener('htmx:afterSwap', function (evt) {
    if (evt.detail.target.id === 'main-content') {
      initializePageScripts();
    }
  });

