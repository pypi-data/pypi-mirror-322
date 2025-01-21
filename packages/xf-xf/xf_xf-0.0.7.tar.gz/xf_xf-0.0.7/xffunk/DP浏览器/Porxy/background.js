clear_proxy()

function set_proxy(host, port) {
    var proxyServer = {
        host: host,
        port: port
    }
    console.log(proxyServer)
    var proxyConfig = {
        mode: "fixed_servers",
        rules: {
            singleProxy: proxyServer,
        },
    }
    chrome.proxy.settings.set({value: proxyConfig, scope: "regular"}, function () {
        console.log('已经设置代理')
    })
}

function clear_proxy() {
    chrome.proxy.settings.clear({scope: "regular"}, function () {
        console.log('已经清空代理')
    })
}