var Home = {};

Home.id = 'home';

Home.show = function () {
    document.querySelector('#homeContent').style.display = 'block';
}

Home.hide = function () {
    document.querySelector('#homeContent').style.display = 'none';
}

Home.resize = function () {
    var homeContentHeight = document.documentElement.clientHeight;
    $('#homeContent').height(homeContentHeight);
}