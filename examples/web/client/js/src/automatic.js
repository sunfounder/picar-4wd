var Automatic = {};

Automatic.id = "automatic";

Automatic.show = function () {
    document.querySelector('#automaticContent').style.display = 'block';
    document.querySelector('#header').style.display = 'block';
    Manual.setRange();
}

Automatic.hide = function () {
    document.querySelector('#automaticContent').style.display = 'none';
    document.querySelector('#header').style.display = 'none';
}

Automatic.resize = function () {
    var automaticContentHeight = $(window).height() - $('#header').height()
    $('#automaticContent').height(automaticContentHeight);
}