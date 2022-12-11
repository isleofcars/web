$(document).ready(() => {
    $('.ads').imagesLoaded(() => {
        $('.ads').masonry({
            // options
            itemSelector: '.ad',
            columnWidth: 200,
            gutter: 0,
            horizontalOrder: true
        });
    });
    $(window).scroll(function () { 
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
            console.log('end');
            $.ajax({
                url :  $('.pagination .next').attr('href'),
                type : 'GET',
                success : function(data) {     
                    let adsNew = $(data).find('.ad');
                    $('.ads').append(adsNew).masonry("appended", adsNew, true);
                    $('.pagination').empty().append($(data).find('> *'));
                },
            })
        }
     });
});
