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
        // TODO: If not logged in -> open modal to log in/ sing up
        let adId = $(e.target).parents('.ad').data('id');
        // TODO: Add some nice animation here
        let icon = $(e.target).parents('.ad').find('.ad__like svg use');
        if (icon.attr('href') === '#icon--like') {
            // Change the icon
            icon.attr('href', '#icon--unlike');
            // TODO: Send ajax
            console.log('like adId', adId, urlPatterns.like);
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
            console.log('unlike adId', adId, urlPatterns.unlike);
            $.ajax({
                // csrftoken: csrftoken,
                headers:{'X-CSRFToken': csrftoken},
                url: urlPatterns.unlike,
                method: 'POST',
                data: {ad_id: adId}
            });
        };
    });
});
