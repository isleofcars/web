$(document).ready(() => {
    $('.ad').on('click', (e) => {
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
    $('.ad__like').on('click', (e) => {
        // TODO: Reduce svg area (click outside of the icon -> open ad)
        // TODO: If not logged in -> open modal to log in/ sing up
        let adId = $(e.target).parents('.ad').data('id');
        console.log('like adId', adId);
        // Change the icon
        // TODO: Add some nice animation here
        let icon = $(e.target).parents('.ad').find('.ad__like svg use');
        if (icon.attr('href') === '#icon--like') {
            icon.attr('href', '#icon--unlike');
            // TODO: Send ajax
        } else {
            icon.attr('href', '#icon--like');
            // TODO: Send ajax
        };
    });
});
