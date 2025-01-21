var proxyServer = {
    host: arguments[0],
    port: arguments[1]
};
var proxyConfig = {
    mode: "fixed_servers",
    rules: {
        singleProxy: proxyServer
    }
};

chrome.proxy.settings.set({value: proxyConfig, scope: "regular"}, function() {
    console.log('代理设置完成');
});
