(function () {
    var userLang = navigator.language || navigator.userLanguage;
    var lang = userLang.split('-')[0]; // 获取主语言代码，例如 'en', 'zh'

    // 定义支持的语言映射表（可选）
    var supportedLangs = ['en', 'zh'];

    // 如果没有对应的语言版本，默认跳转到英文
    if (supportedLangs.indexOf(lang) === -1) {
        lang = 'en';
    }

    // 跳转到对应语言的首页
    var currentPath = window.location.pathname;
    if (currentPath === '/' || currentPath.endsWith('/index.html')) {
        window.location.href = '/' + lang + '/';
    }
})();