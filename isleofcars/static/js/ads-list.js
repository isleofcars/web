$(document).ready(() => {
    $('.ads').imagesLoaded(() => {
        $('.ads').masonry({
            // options
            itemSelector: '.ad',
            // columnWidth: 180,
            gutter: 0,
            horizontalOrder: true,
            isAnimated: true,
            // transitionDuration: 0.5,
            isFitWidth: true,
            cols: {default: 5, 1000: 4, 700: 3, 400: 1},
        });
    });
    // Infinite scroll
    $(window).scroll(function () { 
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
            $.ajax({
                url :  $('.pagination .next').attr('href'),
                type : 'GET',
                success : function(data) {
                    $('.ads').append($('<div height="100vh" id="fakeDiv"></div>'));
                    let adsNew = $(data).find('.ad');
                    $('.ads').append(adsNew);
                    $('.ads').imagesLoaded(() => {
                        $('.ads').masonry('appended', adsNew, true);
                        $('#fakeDiv').remove();
                    });
                    $('.pagination').empty().append($(data).find('> *'));
                },
            })
        }
     });
});
