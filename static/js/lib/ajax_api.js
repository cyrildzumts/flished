define(['lang'], function(Locale) {
    'use strict';
    /**
       * 
       * @param {*} options is a JSON defining the following data :
       * type - string
       * url - string
       * data - json
       * dataType - string
       * Example : 
       * type: 'POST',
         url : '/cart/add_to_cart/',
        data: {product_id: 102, quantity: 4},
        dataType: 'json'
  
        A future object is returned
    */

      function ajax_lang(options, debug){
        if(debug){
          console.debug("ajax_api options - ", options);
        }
        options.url = '/' + Locale.get_lang() + options.url;
        return new Promise(function(resolve, reject){
            $.ajax(options).done(resolve).fail(reject);
        });
      };

      function ajax(options, debug){
        if(debug){
          console.debug("ajax_api options - ", options);
        }
        return new Promise(function(resolve, reject){
            $.ajax(options).done(resolve).fail(reject);
        });
      };

      async function fetch_api(url='', init_option={}){
        const response = await fetch(url, init_option);
        return response.json();
      }

    return {'ajax_lang':ajax_lang, 'ajax' : ajax, 'fetch_api': fetch_api};
  });