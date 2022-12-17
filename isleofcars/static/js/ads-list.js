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
        // cols: {default: 5, 1000: 4, 700: 3, 400: 1},
    });
});

// Infinite scroll
$(window).scroll(function () { 
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        let url = $('.pagination .next').attr('href');
        if (!url) return;
        console.log('load', url);
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'html',
            success: function(response) {
                addNewAds(response);
            },
        })
    }
});

// Add new loaded ads
function addNewAds(response) {
    // $('.ads').append($('<div height="100vh" id="fakeDiv"></div>'));
    let adsNew = $(response).find('.ad');
    setAdsClickEvents(adsNew);
    $('.ads').append(adsNew);
    // console.log('height', $('.ads').attr('style'));
    $('.ads').imagesLoaded(() => {
        $('.ads').masonry('appended', adsNew, true);
        // $('#fakeDiv').remove();
    });
    // console.log(JSON.stringify($(response).find('.pagination')[0]));
    $('.pagination').replaceWith($(response).filter('.pagination'));
    // console.log(response);
    // $('.pagination').empty().append($(response).find('.pagination > *'));
};

// Ads click events
function setAdsClickEvents(ads=null) {
    ads = ads || $('.ad');
    for (let ad of ads) {
        ad = $(ad);

        // Open an ad
        ad.on('click', (e) => {
            // console.log($(e.target).prop('tagName'));
            e = e || event;
            // Don't open an ad if like/unlike was clicked
            let elements = document.elementsFromPoint(e.clientX, e.clientY);
            for (let element of elements) {
                if ($(element).hasClass('ad__like')) return;
            };
            // Open ad in a new tab
            let url = $(e.target).parents('.ad').data('href');
            window.open(url, '_blank').focus();
        });

        // Ad: like/unlike
        ad.find('.ad__like').on('click', (e) => {
            // TODO: If not logged in -> open modal to log in/ sing up
            let adId = $(e.target).parents('.ad').data('id');
            // TODO: Add some nice animation here
            let icon = $(e.target).parents('.ad').find('.ad__like svg use');
            if (icon.attr('href') === '#icon--like') {
                // Change the icon
                icon.attr('href', '#icon--unlike');
                // TODO: Send ajax
                // console.log('like adId', adId, urlPatterns.like);
                $.ajax({
                    // csrftoken: csrftoken,
                    headers:{'X-CSRFToken': csrftoken},
                    url: urlPatterns.like,
                    method: 'POST',
                    data: {ad_id: adId}
                });
            } else {
                // Change the icon
                icon.attr('href', '#icon--like');
                // TODO: Send ajax
                // console.log('unlike adId', adId, urlPatterns.unlike);
                $.ajax({
                    // csrftoken: csrftoken,
                    headers:{'X-CSRFToken': csrftoken},
                    url: urlPatterns.unlike,
                    method: 'POST',
                    data: {ad_id: adId}
                });
            };
        });
    };
};

// Form filters events
$('input[name="search"]').on('focus blur', (e) => {
    $(e.target).parents('.input-box--search').toggleClass('focused');
});

// Search ads
function applyFormFilters(e) {
    e.preventDefault();
    console.log('applyFormFilters');
    // console.log(e.target);
    document.activeElement.blur();
    // $(e.target).blur();
    let query = new URLSearchParams(new FormData($('#search-filters')[0])).toString();
    let url = '/?' + query;
    $.ajax({
        url: url,
        success : function(response) {
            $('.ads').empty().removeAttr('style');
            addNewAds(response);
            document.location.href = url;
        },
        // TODO: Show loader
    })
};

$(document).ready(() => {
    setAdsClickEvents();
});
