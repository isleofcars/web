const maxGallerySize = 300;

function buildMasonryGrid() {
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
};

// Infinite scroll
$(window).scroll(function () { 
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 300) {
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
    let adsNew = $(response).find('.ad');
    setAdsClickEvents(adsNew);
    $('.ads').append(adsNew);
    $('.ads').masonry('appended', adsNew, true);
    // buildMasonryGrid();
    $('.pagination').replaceWith($(response).filter('.pagination'));
};

// Ads click events
function setAdsClickEvents(ads=null) {
    ads = ads || $('.ad');
    for (let ad of ads) {
        ad = $(ad);

        // Open an ad
        ad.on('click', (e) => {
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
                $.ajax({
                    headers: {'X-CSRFToken': csrftoken},
                    url: urlPatterns.like,
                    method: 'POST',
                    data: {ad_id: adId}
                });
            } else {
                // Change the icon
                icon.attr('href', '#icon--like');
                $.ajax({
                    headers: {'X-CSRFToken': csrftoken},
                    url: urlPatterns.unlike,
                    method: 'POST',
                    data: {ad_id: adId}
                });
            };
        });

        // Image gallery on hover
        for (let adButton of ad.find('.ad__gallery__button')) {
            $(adButton).unbind().on('mouseenter', (e) => {
                let number = $(e.target).data('number');
                let image = $(e.target).parent().find(`img[data-number="${number}"]`)
                .clone().removeClass('hidden');
                $(e.target).parents('.ad__gallery').find('.ad__gallery__image')
                .empty().append(image);
            });
        };
        for (let gallery of ad.find('.ad__gallery')) {
            $(gallery).unbind().on('mouseleave', (e) => {
                let image = $(e.target).parent().find('img[data-number="1"]')
                .clone().removeClass('hidden');
                $(e.target).parents('.ad__gallery').find('.ad__gallery__image')
                .empty().append(image);
            });
        };

        // Refresh masonry grid when the title image is loaded
        // TODO: Trigger this when EACH image is loaded (not all)
        ad.find('img[data-number="0"]').imagesLoaded((e) => {
            let img = e.elements[0];
            // Fit a gallery size to the title image width/height ratio
            let newHeight = img.clientWidth / (img.naturalWidth / img.naturalHeight);
            newHeight = Math.min(maxGallerySize, newHeight);
            $(img).parents('.ad__gallery__image').css({height: `${newHeight}px`});
            buildMasonryGrid();
        });
    };
};

// Search ads
function applyFormFilters(e) {
    e.preventDefault();
    document.activeElement.blur();
    let query = new URLSearchParams(new FormData($('#search-filters')[0])).toString();
    let url = '/?' + query;
    $.ajax({
        url: url,
        success : function(response) {
            $('.ads').empty().removeAttr('style');
            addNewAds(response);
            $('#search-filters').replaceWith($(response).filter('#search-filters'));
            // TODO: Remove empty ?search=
            document.location.href = url;
        },
        // TODO: Show loader
    })
};

$(document).ready(() => {
    buildMasonryGrid();
    setAdsClickEvents();
});
