$('#toggleSidebar').on('click', function (e) {
    var sidebar = $('.sidebar-wrap');
    var mainContent = $('.main-wrap');

    if (sidebar.hasClass('hidden')) {
        sidebar.removeClass('hidden');
        mainContent.removeClass('withHiddenSidebar');
    } else {
        sidebar.addClass('hidden');
        mainContent.addClass('withHiddenSidebar');
    }
});


