Main = {};

/**
 * Bind a function to a button's click event.
 * On touch enabled browsers, ontouchend is treated as equivalent to onclick.
 * @param {!Element|string} el Button element or ID thereof.
 * @param {!Function} func Event handler to bind.
 */
Main.bindClick = function (el, func) {
	if (typeof el == 'string') {
		el = document.getElementById(el);
	}
	el.addEventListener('click', func, true);
	el.addEventListener('touchend', func, true);
};

Main.PAGES = {
	'home': Home,
	'manual': Manual,
	'automatic': Automatic,
	'setting': Setting
}


// Main.lastPage = {} //记录上次打开页面
Main.lastPage = [] //记录上次打开页面
/**
 * get the height of MainContent and blockly element
 */
Main.resize = function () {
	console.log('resize!')
	var mainContentHeight = $(window).height();
	$('.mainContent').height(mainContentHeight)
	Home.resize();
	Manual.resize();
	Automatic.resize();
	Setting.resize();
}

Main.initResize = function () {

}


/**
 * 选编程渲染页面
 * @param {string} page 要渲染的页面
 */

Main.renderPage = function (page) {
	if (Main.page) {
		Main.lastPage.push(Main.page);
		Main.lastPage[Main.lastPage.length - 1].hide();
	}
	Main.page = Main.PAGES[page];
	if (window.sessionStorage) {
		window.sessionStorage.setItem('page', Main.page.id)
	}
	Main.page.show();
}

//返回上一页
Main.back = function () {
    // Main.page = Main.PAGES[(Main.lastPage[Main.lastPage.length - 1].id)];
    // if (window.sessionStorage) {
    //     window.sessionStorage.setItem('page', Main.page.id);
    // }
    if (Main.page.id == 'manual') {
        Main.renderPage('home');
    } else {
        Main.renderPage(Main.lastPage[Main.lastPage.length - 1].id);
    }
    
}

//the init of Main object
Main.init = function () {
	Main.renderPage('home');
    Main.resize();
    Setting.init();
    // Main.fullScreen(document.documentElement);
    Manual.init()
    requireWebsocket.connect();
    responseWebsocket.connect();
};

Main.fullScreen = function (element) {
    if (element.requestFullScreen) {
        element.requestFullScreen();
    }else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    }else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
    }else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}

Main.connectModal = function () {
    $('#connectModal_block').show();
}

Main.connectSocketRetry = function () {
    requireWebsocket.connect();
    responseWebsocket.connect();
}



$(function (){
    $('.connectModal_content_back_btn').click(function () {
        Main.renderPage('home');
        $('#connectModal_block').hide();
    })

    $('.connectModal_content_retry_btn').click(function () {
        Main.connectSocketRetry();
        $('#connectModal_block').hide();
    })

    // alert(window.navigator.standalone)
})

window.addEventListener('load', Main.init);