/* globals require, define */
require(['jquery', 'mockup-patterns-modal'], function($, Modal) {
    'use strict';

    $('.action').css('display', 'inline');

    // clone type form
    $('#crud-edit-form-buttons-clone').click(function(e) {
        var selected = $('input[id$=-widgets-select-0]:checked');
        if (selected.length === 1) {
            e.preventDefault();
            $(this).removeClass('submitting');
            var type_link = $('a', selected.closest('tr'));
            var $el = $(
                '<' + 'a href="' + type_link.attr('href') + '/@@clone"><' + '/a>'
            ).appendTo('body');
            var modal = new Modal($el, {
                actionOptions: {
                    displayInModal: false
                }
            });
            $el.click();
        }
    });

    // delete type confirmation
    $('#crud-edit-form-buttons-delete').click(function(e) {
        var items = 0,
            msg;
        $('td.count').closest('tr').has('input:checked').each(function() {
            items += parseInt($('td.count .int-field', this).html().trim());
        });
        if (items) {
            msg =
                'WARNING: There are existing instances of these content types which will break.\n\nAre you sure you want to delete these types?';
        } else {
            msg = 'Are you sure you want to delete these types?';
        }
        if (!window.confirm(msg)) {
            $(this).removeClass('submitting');
            e.preventDefault();
        }
    });

    // set id from title
    $('body').on('change', '#form-widgets-title', function() {
        var id = $.plone_schemaeditor_normalize_string($(this).val());
        $('#form-widgets-id').val(id);
    });

});
