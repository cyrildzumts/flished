requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendors',
        editor: '../vendors/editor'

    },
    waitSeconds: 0
});

requirejs(['ajax_api', 'commons'], function(ajax_api){
    console.log("flished app ready");
});