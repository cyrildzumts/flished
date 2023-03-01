define(['require','filters','ajax_api', 'element_utils'
    ], function(require,Filter,ajax_api, element_utils,EditorJS) {
    'use strict';
    
    const SAVE_DRAFT_INTERVAL = 10000; // 10s
    const EDITOR_CHANGE_TIMEOUT = 1000; // 1s
    const COMMENT_FETCH_INTERVAL = 30000; // 30s
    const COOKIE_CONSENT_MODAL_SELECTOR = 'cookie-consent-modal';
    const COOKIE_CONTENT_BTN_SELECTOR = 'cookie-content-btn';
    const POST_STATUS_PUBLISH = 1
    const CAROUSEL_INTERVAL = 5000;
    const MIN_LEN_WARNING = 20;
    const MAX_COMMENT_TEXT_LEN = 256;
    const LOGIN_REQUIRED_KEY = "login_required";
    const UI_TOGGLE_OPEN_CSS = "fa-bars";
    const UI_TOGGLE_CLOSE_CSS = "fa-times";
    let AUTO_SAVE_TIMER;
    let fileUpload;
    let postManager;
    let commentManager;
    let messages;
    let notification_wrapper;
    let fadeDelay = 10000; // 10s
    let filter_form;
    let editor;
    let post_content;
    let json_input;
    

    
    function clean_form_before_submit(form){
        let filter_inputs = $('.filter-input', form);
        filter_inputs.each(function(){
            this.disabled = this.value == "";
        });
        $('.no-submit', form).each(function(){
            this.disabled = true;
        });
        let valid_inputs = filter_inputs.filter(function(){
            return this.value != "";
        });
        return valid_inputs.length == 0;
    }
    function notify(message){
        if( typeof notification_wrapper === 'undefined' || typeof messages === 'undefined'){
            console.warn("Notify call for message %s. But There is no messages container", message);
            return;
        }
        let li = $('<li />', {
            "class" : message.level,
        });
        let div = $('<div />', {
            "class" : "notification flex"
        });
        div.append($('<i />', {
            "class" : "fas fa-info-circle icon"
        })).append($('<span />', {
            'text': message.content
        })).appendTo(li);
        li.appendTo(messages);
        notification_wrapper.fadeIn().delay(fadeDelay).fadeOut('slow', function () {
            messages.empty();
        });
    }

    function notify_init(wrapper, message_container){
    
        if(typeof wrapper === 'undefined'){
            console.log("notification_wrapper undefined");
            return;
        }

        if(typeof message_container === 'undefined' || $('li', message_container).length == 0){
            return;
        }

        wrapper.fadeIn().delay(fadeDelay).fadeOut('slow', function () {
            message_container.empty();
            console.log("messages container emptied on init");
        });
    }

    function input_check_max_limit(input){
        //let max_len = parseInt(input.dataset.maxLength);
        let len = input.value.length;
        let target = document.getElementById(input.dataset.target);
        let max_len_reached = len == MAX_COMMENT_TEXT_LEN;
        //$input.toggleClass("warning", max_len_reached);
        if((MAX_COMMENT_TEXT_LEN - len) <= MIN_LEN_WARNING){
            target.innerText = MAX_COMMENT_TEXT_LEN - len;
        }else{
            target.innerText = "";
        }
        target.classList.toggle("danger", (MAX_COMMENT_TEXT_LEN - len) <= 0);
        target.classList.toggle("warning", ((MAX_COMMENT_TEXT_LEN - len) > 0 && (MAX_COMMENT_TEXT_LEN - len) <= MIN_LEN_WARNING));
    }

    function track_action(track_element){
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        let url = '/api/track-actions/';
        let action = parseInt(track_element.dataset.action);
        let options = {
            url : url,
            type: 'POST',
            data : {'action': action, 'csrfmiddlewaretoken': csrfmiddlewaretoken.value},
            dataType : 'json',
            async:false,
            cache : false,

        };
        ajax_api.ajax(options).then(function(response){
            
        }, function(reason){
            console.error(reason);
        });
    }

    var ListFilter = (function(){
        function ListFilter(){
            //this.init();
            console.log("ListFilter instance created");
        };

        ListFilter.prototype.init = function(){
            console.log("ListFilter instance initializing");
            var self;
            $('.js-list-filter').on('keyup', function(event){
                event.stopPropagation();
                var value = this.value.trim().toLowerCase();
                var fieldname = $(this).data('field');
                var target = $("#" + $(this).data('target'));
                
                target.children().filter(function(){
                    self = $(this)
                    self.toggle(self.data(fieldname).toLowerCase().includes(value));
                });
            });

            console.log("ListFilter instance initialized");
        };

        ListFilter.prototype.filter = function(ctx, filter_field, value_list){
            if(!ctx || !filter_field || !value_list || value_list.length == 0){
                console.log("Filter called with missing argumtent");
                return;
            }
            console.log("Filtering started");
            $(".filterable", ctx).each(function(index, element){
                let filter_value = this.getAttribute(filter_field);
                console.log(" Filter Field = \"%s\" - Filter Value = \"%s\" - Value List = [\"%s\"]", filter_field ,filter_value, value_list)
                $(this).toggle(value_list.includes(filter_value));
            });
            console.log("Listfilter : filter run with success");
        };

        ListFilter.prototype.reset_filter = function(ctx, container){
            if(!ctx || !container){
                console.log(" Reset Filter called with missing context");
                return;
            }
            $("input:checkbox", ctx).each(function(){
                this.checked = false;
            });
            $(".filterable", container).each(function(index, element){
                $(this).show();
            });
            console.log("Listfilter : reset run with success");
        };

        return ListFilter;
    })();

    var FileUpload = (function(){
        function FileUpload(){
            this.files = [];
            this.form = undefined;
            this.formData = undefined;
            this.clean = true;
            this.drag_area = $('.drag-area');
            this.file_list_container = $('.file-list');
            this.file_entries = {};
            this.empty_element = $('.no-data', this.file_list_container);
            this.send_btn = $('.js-send-file-upload-btn');
            this.clear_btn = $('.js-file-list-clear-btn');
            //this.init();
        };

        FileUpload.prototype.init = function(){
            var that = this;
            this.clear_btn.on('click', this.clear.bind(this));

            $('.drag-area')
                .on('drop', onDropHandler)
                .on('dragover', onDragOverHandler)
                .on('dragenter', onDragStartHandler)
                .on('dragleave', onDragEndHandler)
        };

        FileUpload.prototype.clear = function() {
            this.files = [];
            this.formData = undefined;
            this.form = undefined;
            this.clean = true;
            //$('.file-entry', this.file_list_container).remove();
            this.file_list_container.empty().append(this.empty_element);
            this.drag_area.removeClass('non-empty');
            this.send_btn.addClass('disabled').prop('disabled',true);
            this.clear_btn.addClass('hidden');
        };

        FileUpload.prototype.isClean = function() {
            return this.clean;
        };

        FileUpload.prototype.setForm = function(form){
            this.form = form;
            this.clean = false;
            return this;
        };

        FileUpload.prototype.setFiles = function(files){
            this.files = files;
            this.clean = false;
            return this;
        };

        FileUpload.prototype.addFile = function(file){
            if(this.files.some(f => f.name == file.name)){
                console.warn("A file with the same name already exists.")
                return this;
            }
            var that = this;
            this.files.push(file);
            var li = $('<li />',{
                id:"file-" + that.files.length,
                'class' : 'file-entry',
                'title': file.name,
            });
            var entry_text = $('<span />', {
                text: file.name
            });
            var entry_remove_btn = $('<button />', {
                class: 'mat-button mat-button-text',
                type: 'button'
            }).append($('<i />', {
                class: 'fas fa-times icon'
            }));
            entry_remove_btn.on('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                that.removeFile([file.name]);
                li.remove();
            });
            li.append(entry_text, entry_remove_btn).appendTo(that.file_list_container);
            $('.no-data', that.file_list_container).remove();
            this.drag_area.addClass('non-empty');
            this.send_btn.removeClass('disabled').prop('disabled',false);
            this.clear_btn.removeClass('hidden');
            this.clean = false;
            return this;
        };

        FileUpload.prototype.removeFile = function(fileNames){
            var old_length = this.files.length;
            this.files = this.files.filter(f => !fileNames.includes(f.name));
            if(this.files.length != old_length && this.files.length < old_length){

                if(this.files.length == 0){
                    this.file_list_container.append(this.empty_element);
                    this.drag_area.removeClass('non-empty');
                    this.send_btn.addClass('disabled').prop('disabled',true);
                    this.clear_btn.addClass('hidden');
                }
                this.clean = false;
            }else{
                console.log("files : %s not removed", fileNames);
                
            }
            
            return this;
        };
        FileUpload.prototype.update = function(){
            if(this.isClean()){
                console.warn("FileUpload can not be updated. formData is already clean.");
                return;
            }
            if(!this.form || !this.files || this.files.length == 0){
                console.warn("FileUpload can not be updated. form or files are missing.");
                return;
            }
            this.formData = new FormData(this.form);
            var that = this;
            this.files.forEach(function(file, index){
                that.formData.append("file_" + index, file, file.name);
            });
            this.clean = true;
            /*
            $(form).serializeArray().forEach(function(input, index){
                formData.append(input.name, input.value);
            });
            */
        };

        FileUpload.prototype.canSend = function(){
            let formValid = typeof this.form != 'undefined';
            let filesValid = typeof this.files != 'undefined';

            return formValid && filesValid && this.files.length > 0;
        };

        FileUpload.prototype.getForm = function() {
            return this.form;
        };

        FileUpload.prototype.getFiles = function() {
            return this.files;
        }

        FileUpload.prototype.getFormDate = function() {
            return this.formData;
        }

        FileUpload.prototype.upload = function(){
            if(!this.canSend()){
                console.error("Files can not be sent. Please check your files form. Files or form are missing.");
                return;
            }
            if(typeof ajax_api.ajax_lang === 'undefined'){
                var errorMsg = "can not upload files. ajax funtion is not defined";
                console.error(errorMsg);
                throw new Error(errorMsg);
            }
            var that = this;
            var options = {
                url : $(this.form).attr('action'),
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                var msg = {
                    content : response.message,
                    level : response.status === 'OK'
                }
                notify(msg);
                fileUpload.clear();
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                fileUpload.clear();
            });

        };

        return FileUpload;
    })();

    var CommentManager = (function(){
        function CommentManager() {
            this.form = undefined;
            this.formData = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;

            this.post_status = 0;
        };
        CommentManager.prototype.init = function(){
            var self = this;
            $('.js-post-like').on('click', function(e){
                e.stopPropagation();
                let post = this.dataset.post;
                let liked = this.dataset.liked;
                self.add_like(liked, post);
            });
            console.log("CommentManager initialized");
        };
        CommentManager.prototype.onAddLikeResponse = function(data){
            let post_like = document.querySelector('.post-like');
            let post_like_count = document.querySelector('.post-like-count');
            if(!post_like || !post_like_count){
                return;
            }
            if(data.success){
                post_like_count.innerText = data.likes > 0 ? data.likes : '';
                post_like.dataset.liked = data.liked ? "true" : 'false';
                post_like.dataset.likes = data.likes;
                post_like.title = data.title;
                post_like.classList.toggle('liked', data.liked);
                post_like.classList.toggle('unliked', data.liked);
            }
        };

        CommentManager.prototype.add_like = function(liked, post_id){
            let self = this;
            let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            let url = (liked == "false" ? '/api/add-like/': '/api/remove-like/') + post_id + '/';
            let fetch_options = {
                method : 'POST',
                body: formData
            };
            ajax_api.fetch_api(url, fetch_options).then(function(response){
                self.onAddLikeResponse(response);
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
            });
        };

        return CommentManager;

    })();

    var Modal = (function(){
        function Modal(options){
            this.modal = {};
            this.init();
        }
        Modal.prototype.init = function(){
            let that = this;

            $(".js-open-modal").click(function(event){
                if((LOGIN_REQUIRED_KEY in this.dataset) && this.dataset[LOGIN_REQUIRED_KEY] == "1" ){
                    event.stopPropagation();
                    event.preventDefault();
                    notify({"level": "info", "content": this.dataset.message});
                    return false;
                }
                let modal = document.getElementById(this.dataset.target);
                that.modal = modal;
                
                modal.style.display = "flex";
                if(window){
                    $(window).click(function(eventModal){
                        if(eventModal.target == modal){
                            modal.style.display = "none";
                            that.modal = undefined;
                            let inputs = modal.querySelectorAll("input:not([name='csrfmiddlewaretoken']):not([type='hidden']), textarea");
                            let clearables = modal.querySelectorAll('.clearable');
                            if(clearables){
                                clearables.forEach((el) =>{
                                    el.innerText = "";
                                    el.classList.remove('warning', 'danger');
                                });
                            }
                            if(inputs){
                                inputs.forEach(function(el,index){
                                    el.value = "";
                                    el.dataset.update = "";
                                    if(el.type =="file"){
                                        el.files = null;
                                    }
                                    if(el.type == "checkbox" || el.type == "radio"){
                                        el.checked = false;
                                    }
                                });
                            }
                        }
                    });
                }
            });
    
            $(".js-close-modal").click(function(event){
                event.stopPropagation();
                let modal = document.getElementById(this.dataset.target);
                modal.style.display = "none";
                that.modal = undefined;
                let inputs = modal.querySelectorAll("input:not([name='csrfmiddlewaretoken']):not([type='hidden']), textarea");
                let clearables = modal.querySelectorAll('.clearable');
                if(clearables){
                    clearables.forEach((el) =>{
                        el.innerText = "";
                        el.classList.remove('warning', 'danger');
                    });
                }
                if(inputs){
                    inputs.forEach(function(el,index){
                        el.value = "";
                        el.dataset.update = "";
                        if(el.type =="file"){
                            el.files = null;
                        }
                        if(el.type == "checkbox" || el.type == "radio"){
                            el.checked = false;
                        }
                    });
                }
            });
        }
        return Modal;
    })();

    function kiosk_update(event){
        document.getElementById('main-image').src = event.target.src;
        $(".kiosk-image").removeClass('active').filter(event.target).addClass("active");
    }

    function parseHTML(html){
        let template = document.createElement('template');
        template.innerHTML = html;
        return template.content;
    }
    function create_comment(data){
        let author = data.username;
        let created_at = data.date;
        let comment = data.comment;
        let comment_tag = 
    `<li class="margin-bottom">
        <div class="comment">
            <div class="post-header">
                <span class="bold">${author}</span>|<span><i class="fas fa-comment icon"></i> ${created_at}</span>|<span class="js-report-comment" title="report"><i class="far fa-flag icon"></i></span>
            </div>
            <div>
                <p>${comment}</p>
            </div>
        </div>
    </li>`;
    return parseHTML(comment_tag);
    }

    function auto_fetch_comments(post_id, comments_container){
        let post_comment_count = document.getElementById('post-comment-count');
        let post_like_count = document.getElementById('post-like-count');
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        function fetch_comments(){
            let last = comments_container.dataset.latest;
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            formData.append('created_at', last);
            let url = '/api/fetch-comments/' + post_id + '/';
            let fetch_options = {
                method : 'POST',
                body: formData
            };
            ajax_api.fetch_api(url, fetch_options).then(function(response){
                if(!response.success || !response.comments){
                    return;
                }
                comments_container.dataset.latest = response.latest;
                post_comment_count.innerText = parseInt(post_comment_count.innerText) + response.comment_count;
                post_like_count.innerText = response.likes;
                response.comments.forEach((c)=>{comments_container.appendChild(create_comment(c))});
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
            });
        }
        return setInterval(fetch_comments, COMMENT_FETCH_INTERVAL);
    }

    function init_accordion(){
        let toggle_list = document.querySelectorAll('.accordion-toggle');
        if( toggle_list == 0){
            return;
        }
        toggle_list.forEach((t,i)=>{
            t.addEventListener('click', function(event){
                event.stopPropagation();
                event.preventDefault();
                let activate = !this.classList.contains('active');
                toggle_list.forEach((e,i)=>{
                    e.classList.remove('active');
                    if(e.dataset.target){
                        document.getElementById(e.dataset.target).style.display = 'none';
                    }else{
                        e.parentElement.nextElementSibling.style.display = 'none';
                    }
                });
                this.classList.toggle('active', activate);
                if(this.dataset.target){
                    //document.getElementById(this.dataset.target).classList.toggle('hidden', !activate);
                    document.getElementById(this.dataset.target).style.display = activate ? 'block': '';
                }else{
                    //this.parentElement.nextElementSibling.classList.toggle('hidden', !activate);
                    this.parentElement.nextElementSibling.style.display = activate ? 'block': '';
                }
            });
        });
    }
    function init_dropdown(){
        let toggle_list = document.querySelectorAll('.dropdown-toggle');
        if( toggle_list.length == 0){
            return;
        }
        
        toggle_list.forEach((t,i)=>{
            t.addEventListener('click', function(event){
                event.stopPropagation();
                event.preventDefault();
                toggle_list.forEach((e,i)=>{
                    if((e != t) && (e.dataset.target != t.dataset.target)){
                        if(e.dataset.target){
                            document.getElementById(e.dataset.target).classList.remove('show');
                        }else{
                            e.nextElementSibling.classList.remove('show');
                        }
                    }
                });
                if(this.dataset.target){
                    document.getElementById(this.dataset.target).classList.toggle('show');
                }else{
                    this.nextElementSibling.classList.toggle('show');
                }
            });
        });
    }

    function notification_listener(){
        let url;
        let user_notification_list = document.getElementById("user-notification-list");
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        let options = {
            url : null,
            type: 'POST',
            data : {'csrfmiddlewaretoken': csrfmiddlewaretoken.value},
            dataType : 'json',
            async:false,
            cache : false,
            
        };
        
        let read_btn_list = document.querySelectorAll('.js-notify-read');
        read_btn_list.forEach((btn, i)=>{
            btn.addEventListener('click', (event)=>{
                event.stopPropagation();
                event.preventDefault();
                let notification_id = btn.dataset.notification;
                options['url'] = `/api/notifications/${notification_id}/mark-read`;
                ajax_api.ajax(options).then(function(response){
                    if(response.success){
                        let target = document.getElementById(btn.dataset.target);
                        user_notification_list.removeChild(target);
                    }

                }, function(reason){
                    console.error(reason);
                });
            });
        });
    }

    $(document).ready(function(){
        if(window){
            window.notify = notify;
        }
        let modal = new Modal();
        //load_cookie_consent();
        commentManager = new CommentManager();
        commentManager.init();
        init_accordion();
        init_dropdown();
        //notification_listener();
        notification_wrapper = $('#notifications-wrapper');
        messages = $('#messages', notification_wrapper);
        //onDragInit();
        notify_init(notification_wrapper, messages);
        var listfilter = new ListFilter();
        Filter.init();
        fileUpload = new FileUpload();

        let comments = document.getElementById('comments');
        if(comments){
            auto_fetch_comments(comments.dataset.post, comments);
        }
        document.querySelectorAll("button[data-ui-toggle='collapse']").forEach((button)=>{
            if(!button.dataset.uiTarget){
                return;
            }
            button.addEventListener('click',(event)=>{
                let target = document.getElementById(button.dataset.uiTarget);
                target.classList.toggle('show');
                let i = button.querySelector("i");
                i.classList.toggle(UI_TOGGLE_OPEN_CSS);
                i.classList.toggle(UI_TOGGLE_CLOSE_CSS);
            });

        });
        $('.collapsible .toggle').on('click', function(event){
            var parent = $(this).parent();
            var target = $('.' + this.getAttribute('data-toggle'), parent);
            $('input', parent).val('');
            
            target.toggle();
        });
        $('.js-filter-btn').on('click', function(event){
            var ctx = $('#' + this.getAttribute('data-context'));
            var input_name = this.getAttribute('data-input-name');
            var container = $('#' + this.getAttribute('data-container'));
            var filter_field = this.getAttribute("data-filter-field");
            var value_list = [];
            $("input:checked[name=\"" + input_name + "\"]", ctx).each(function(){
                value_list.push(this.getAttribute("data-value"));
            });
            listfilter.filter(container, filter_field, value_list);
        });

        $('.js-filter-reset-btn').on('click', function(event){
            var ctx = $('#' + this.getAttribute('data-context'));
            var container = $('#' + this.getAttribute('data-container'));
            listfilter.reset_filter(ctx, container);
        });

        $('#file-upload-form').on('submit', function(event){
            event.preventDefault();
            event.stopPropagation();
            fileUpload.setForm(this);
            fileUpload.update();
            fileUpload.upload();
            //return false;
            
        });
        $('.js-select-image').on('click', kiosk_update);
        $('.js-select-image').first().click();
        $(".limited-input").on("keyup", function(event){
            event.stopPropagation();
            input_check_max_limit(this);
        });
        $('.js-dialog-open').on('click', function(){
            var target = $('#' + $(this).data('target'));
            target.show();
        });

        
        $('.js-dialog-close').on('click', function(){
            var target = $("#" + $(this).data('target'));
            target.hide();
            //var parent = $(this).parents('.dialog').hide();
            $('input[type!="hidden"]', target).val('');
        });
        $('.js-reveal-btn, .js-revealable-hide').on('click', function(){
            var target = $($(this).data('target')).parent();
            $('.js-revealable', target).toggleClass('hidden');
        });
        $('.js-clear-input').on('click', function(){
            
            var target = $('#' + $(this).data('target'));
            $('input[type!=checkbox]', target).val('');
            $('input:checkbox', target).val('').prop('checked', '');
        });
        var selectable_list = $(".js-selectable");
        var activable_list = $(".js-activable");
        var select_all = $('.js-select-all');
        selectable_list.on('click', function(){
            var is_selected = selectable_list.is(function (el) {
                return this.checked;
            });
            
            var selected_all = selectable_list.is(function (el) {
                return !this.checked;
            });
            select_all.prop('checked', !selected_all);
            activable_list.prop('disabled', !is_selected);
        });

        select_all.on('click', function(){
            selectable_list.prop('checked', this.checked);
            activable_list.prop('disabled', !this.checked);
        });

        filter_form = $('#filter-form');
        $('#filter-form').on('submit', function(event){
            $('input[name="csrfmiddlewaretoken"]').prop('disabled', true);
            let reload = clean_form_before_submit(this);
            if(reload){
                event.stopPropagation();
                event.preventDefault();
                window.location.search = "";
                window.location = location.pathname;
            }
        });
        $('.js-pagination').on('click', function(event){
            
            if(filter_form.length != 0){
                event.preventDefault();
                event.stopPropagation();
                
                var page = $(event.target).data('page');
                let input = element_utils.create_element_api({'element': 'input', 'options': {'cls': 'filter-input', 'name': 'page', 'value': page,'type':'text','id':'page'}});
                //input.appendTo(filter_form);
                filter_form.append(input)
                filter_form.submit();
            }
            

        });
        
        $('.js-custom-input .input-value').on('click', function(event){
            $(this).toggle();
            $('.input-edit-wrapper', $(this).parent()).toggle();
        });
        
        $('.js-custom-input input').on('keyup change', function(event){
            var $el = $(this);
            $el.parent().siblings('.input-value').html($el.val());
        });
        
        $('.js-custom-input .js-edit-close').on('click', function(event){
            var $el = $(this).siblings('input');
            $el.parent().siblings('.input-value').html($el.val());
            $(this).parent().toggle();
        });
        $('.js-menu').on('click', function(){
            $('#menu-overlay-label').click();
            $('.js-menu-close').show();
            $(this).hide();
    
        });
        $('.js-menu-close').on('click', function(){

            $('#menu-overlay-label').click();
            $('.js-menu').show();
            $(this).hide();
        });
        /*
        $('.js-action-abtest').on('click', function(e){
            track_action(this);
        });
        */
       console.log("Commons module loaded");
    });
});