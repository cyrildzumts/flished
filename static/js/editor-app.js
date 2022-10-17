requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendor',
        editor: '../vendor/editor'

    },
    waitSeconds: 0
});

requirejs(['ajax_api', 'commons', 'editor-api'], function(ajax_api){
    console.log("flished app ready");
});