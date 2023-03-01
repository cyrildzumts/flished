define([],function() {
    'use strict';
    let list_filter = {
        init : function(){
            $('.js-list-filter').on('keyup', function(event){
                event.stopPropagation();
                let value = this.value.trim().toLowerCase();
                let fields = this.dataset.fields.split(' ');
                let target = document.getElementById(this.dataset.target);
                let node;
                let collection = target.children;
                let included = false;
                for(let index = 0; index < collection.length; index++){
                    node = collection[index];
                    for(let f of fields){
                        included = node.dataset[f].toLowerCase().includes(value);
                        if(included) break;
                    }
                    node.classList.toggle('hidden', !included); 
                }
            });
            console.log("Custome filter installed");
        }
    };
    return list_filter;
});