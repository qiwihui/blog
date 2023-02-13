/**
 * Created by hzhou on 4/30/17.
 */

$(document).ready(function () {

    var searchInput = $('#tipue_search_input');
    searchInput.tipuesearch({
        'mode': 'json',
        'minimumLength': 2,
        'contentLocation': '/tipuesearch/tipuesearch_content.json',
        highlightEveryTerm: true
    });

    $('#search-form').on('submit', function (e) {
        e.preventDefault();
        $('#tipue_search_content').show();
        $('#content').hide();
    });

    searchInput.keyup(function () {
        var length = $(this).val().length;
        if (length < 1) {
            $('#tipue_search_content').hide();
            $('#content').show();
        }
    });
});