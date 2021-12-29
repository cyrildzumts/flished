requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendor'
    },
    waitSeconds: 0
});

requirejs(['accounts','cart_lyshop', 'attributes_api', 'ajax_api', 'components_api', 'checkout','wishlist','scroll', 'commons', 'image_loader', 'activities'], function(account, Cart, AttributeManager ,ajax_api, Component, Checkout, Wishlist, scroll_tools){
    account.init();
    var cart = new Cart();
    var wishlist = new Wishlist();
    var attr_manager = new AttributeManager();
    cart.init();
    wishlist.init();
    attr_manager.init();
    Component.initComponent();
    var checkout = new Checkout(Component.tabs);
    checkout.init();
    scroll_tools.init();
});