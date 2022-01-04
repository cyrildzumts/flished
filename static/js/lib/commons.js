define(['require','ajax_api', 'element_utils', 'editor/editor', 
    'editor/plugins/header.min','editor/plugins/list.min', 'editor/plugins/link.min',
    'editor/plugins/checklist.min', 'editor/plugins/quote.min', 'editor/plugins/table.min',
    'editor/plugins/inline-image'
    ], function(require,ajax_api, element_utils,EditorJS) {
    'use strict';

    const Header = require('editor/plugins/header.min');
    const List = require('editor/plugins/list.min');
    const Link = require('editor/plugins/link.min');
    const Checklist = require('editor/plugins/checklist.min');
    const Quote = require('editor/plugins/quote.min');
    const Table = require('editor/plugins/table.min');
    const InlineImage = require('editor/plugins/inline-image');
    
    let fileUpload;
    let postManager;
    let messages;
    let notification_wrapper;
    let fadeDelay = 10000; // 10s
    let filter_form;
    let editor;
    let post_content;
    let headers = [null, "h1","h2", "h3", "h4", "h5", "h6"];
    let LIST_TYPE_MAPPING = {
        ordered: 'ol',
        checklist: 'ul'

    };
    let unsplash_config = {
        appName: "",
        clientId: ""
    };
    let BLOCK_MAPPING = {
        'header': render_header,
        'paragraph': render_paragraph,
        'table': render_table,
        'list': render_list,
        'linkTool': render_linkTool,
        'checklist': render_checklist,
        'quote': render_quote,
        'image': render_inlineImage
    };

    function render_header(header){
        let node = element_utils.create_element_api({
            element:headers[header.data.level],
            options : {
                id:header.id,
                innerHTML: header.data.text
            }
        });
        return node;
    }

    function render_linkTool(linkTool){
        let node = element_utils.create_element_api({
            element: "a",
            options : {
                id:linkTool.id,
                cls:'mat-button mat-button-text',
                href : linkTool.data.link,
                innerText: linkTool.data.link
            }
        });
        return node;
    }

    function render_inlineImage(inlineImage){
        let node = element_utils.create_element_api({
            element: "img",
            options : {
                id:inlineImage.id,
                src: inlineImage.data.url,
                title: inlineImage.data.caption,
                cls:'img-responsive',
            }
        });
        return node;
    }

    function render_paragraph(paragraph){
        let node = element_utils.create_element_api({
            element: "p",
            options : {
                id:paragraph.id,
                innerHTML : paragraph.data.text
            }
        });
        return node;
    }

    function render_table(table){
        let items = [];
        let startIndex = 0;
        let content;

        if(table.data.withHeadings){
            
            let ths = [];
            table.data.content[startIndex].forEach((h)=>{
                ths.push(element_utils.create_element_api({
                    element:'th',
                    options:{
                        innerHTML:h
                    }
                }));
            });
            let tr = element_utils.create_element_api({
                element: 'tr',
                options:{
                    children: ths
                }
            });
            items.push(element_utils.create_element_api({
                element: 'thead',
                options:{
                    children: [tr]
                }
            }));

            startIndex = 1;
            content = table.data.content.slice(startIndex);
        }else{
            content = table.data.content;
        }

        let trs = [];
        content.forEach((item)=>{
            let tds = [];
            item.forEach((value) => tds.push(element_utils.create_element_api({
                element: "td",
                options : {
                    innerText : value
                }
            })));
            trs.push(element_utils.create_element_api({
                element: "tr",
                options : {
                    children : tds
                }
            }));
        });
        items.push(element_utils.create_element_api({
            element: "tbody",
            options : {
                children: trs
            }
        }));
        let node = element_utils.create_element_api({
            element: table.type,
            options : {
                id:table.id,
                children : items
            }
        });
        return node;
    }

    function render_list(list){
        let items = []
        list.data.items.forEach((item)=>{
            items.push(element_utils.create_element_api({
                element: "li",
                options : {
                    innerHTML : item
                }
            })
            );
        });
        let node = element_utils.create_element_api({
            element: LIST_TYPE_MAPPING[list.data.style],
            options : {
                id:list.id,
                children : items
            }
        });
        return node;
    }

    function render_checklist(checklist){
        let items = []
        checklist.data.items.forEach((item)=>{
            let input = element_utils.create_element_api({
                element : "input",
                options : {
                    'type': 'checkbox',
                    'checked': item.checked
                }
            });
            let span = element_utils.create_element_api({
                element: "span",
                options : {
                    innerHTML : item.text
                }
            });
            let div = element_utils.create_element_api({
                element: "div",
                options : {
                    children : [input, span]
                }
            });
            items.push(element_utils.create_element_api({
                element: "li",
                options : {
                    children : [div]
                }
            })
            );
        });
        let node = element_utils.create_element_api({
            element: LIST_TYPE_MAPPING[checklist.type],
            options : {
                id:checklist.id,
                children : items
            }
        });
        return node;
    }

    function render_quote(quote){
        let span = element_utils.create_element_api({
            element: "span",
            options : {
                innerHTML : quote.data.text
            }
        });
        let cite = element_utils.create_element_api({
            element: "cite",
            options : {
                innerHTML : quote.data.caption
            }
        });
        let node = element_utils.create_element_api({
            element: "blockquote",
            options : {
                id:quote.id,
                innerHTML : quote.data.text,
                children: [cite]
            }
        });
        return node;
    }

    
    function editor_content_clear(container){
        let editor_content = container || document.querySelector('#editor-content');
        if (editor_content){
            while(editor_content.firstChild){
                editor_content.removeChild(editor_content.firstChild);
            }
        }
    }

    function render_content(blocks){
        let elements = [];
        blocks.forEach((block)=>{
            elements.push(BLOCK_MAPPING[block.type](block));
        });
        return elements;
    }

    function on_editor_save(saved_data){
        console.log("Saving editor data : ", saved_data);
        post_content = saved_data;
        let editor_content = document.querySelector('#editor-content');
        if (editor_content){
            try {
                let content = element_utils.create_element_api({
                    element:"div",
                    options : {
                        cls:"content full",
                        children : render_content(saved_data.blocks)
                    }
                });
                if(content){
                    editor_content_clear(editor_content);
                    editor_content.appendChild(content);
                    console.log("Saved editor data : ");
                    
                }
            } catch (error) {
                console.log("Content data not saved",error);
            }
            let content_object = document.querySelector('#content-object');
            if(content_object){
                let content = element_utils.create_element_api({
                    element:"div",
                    options : {
                        cls:"object full",
                        innerHTML: JSON.stringify(saved_data)
                    }
                });
                content_object.appendChild(content);
            }
        }
    }

    function fetch_credential(callback){
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        let url = '/api/fetch-credentials/';
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
        let fetch_options = {
            method : 'POST',
            body: formData
        };
        ajax_api.fetch_api(url, fetch_options).then((response)=>{
            editor = callback({appName : response.appName, clientId : response.access_key});
        }, function(reason){
            console.error("Error on fetching unsplash credentials.");
            console.error(reason);
            
        });
    }

    function editor_init(unsplash_conf){
        editor = new EditorJS({
            holder:'editor',
            tools: {
                header : {
                    class : Header,
                    inlineToolbar : true
                },
                image: {
                    class : InlineImage,
                    inlineToolbar : true,
                    config: {
                        embed : {
                            display: true
                        },
                        unsplash : unsplash_conf
                    }
                },
                list: {
                    class: List,
                    inlineToolbar: true
                },
                linkTool: {
                    class: Link,
                    inlineToolbar: true
                },
                checklist: {
                    class:Checklist,
                    inlineToolbar:true
                },
                quote: {
                    class:Quote,
                    inlineToolbar:true,
                    shortcut: 'CMD+SHIFT+Q',
                    config: {
                        quotePlaceholder: 'Enter a quote',
                        captionPlaceholder: 'Quote\'s author',
                    },
                },
                table: {
                    class: Table,
                    inlineToolbar: true,
                    config: {
                      rows: 2,
                      cols: 3,
                    },
                  },
            },
            placeholder: 'Start typing here ...',
            onReady: function(){
                console.log("Editor is ready" , editor);
            },
            onChange: () =>{
                console.log("Editor has changed");
            }
        });
        $(".js-save-btn").on('click', function(event){
            editor.save().then(on_editor_save).catch((error)=>{
                console.log("Error on saving editor content : ", error);
            });
        });
        $(".js-clear-btn").on('click', (event)=>{
            console.log("Clearing editor content not implemented yet ");
        });
        console.log("Editor loaded");

        return editor;
    }


    function create_editor(){
        fetch_credential(editor_init);
    }

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
        var $input = $(input);
        var max_len = parseInt($input.data('max-length'));
        var len = $input.val().length;
        var target = $($input.data('target'));
        var max_len_reached = len > max_len;
        $input.toggleClass("warning", max_len_reached);
        target.toggleClass("danger", max_len_reached).text(len);
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
            this.init();
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

    var PostManager = (function(){
        function PostManager() {
            this.images = null;
            this.form = undefined;
            this.formData = undefined;
            this.input_file = undefined;
            this.drag_area = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;
            this.clear_uploaded_files_btn = undefined;
            this.created_post_container = undefined;
            this.created_post_link = undefined;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
        };
        PostManager.prototype.init = function(){
            var self = this;
            this.created_product_container = document.querySelector('#created-post-link');
            this.created_product_link = document.querySelector('#created-post-link a');
            this.files_container = document.querySelector('.file-list');
            
            $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                self.drag_area.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                self.drag_area.classList.remove('on-drag');
            }).on('drop', function(e){
                self.images = e.originalEvent.dataTransfer.files;
                self.input_file.files = self.images;
                self.onImagesChanged();
                self.imagesPreview();

            });
            $('#files').on('change', function(e){
                self.images = self.input_file.files;
                self.onImagesChanged();
                self.imagesPreview();
            });
            
            $('.js-uploaded-files-clear').on('click', this.clearImages.bind(this));
            
            $(".js-create-post-btn").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    self.upload();
                }
            });

            console.log("PostManager initialized");
        };

        PostManager.prototype.imagesPreview = function(){
            var li;
            var img;
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            var f;
            for(var i = 0; i < this.images.length; i++){
                f = this.images[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                this.files_container.appendChild(li);
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                li.appendChild(info);
            }
            $('.js-uploaded-files-clear').show();
        };

        PostManager.prototype.clearImages = function(){
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            this.images = null;
            this.input_file.files = null;
            var li = document.createElement('li');
            var span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            this.files_container.appendChild(li);
            this.onImagesChanged();
        };

        PostManager.prototype.clear = function(){
            var inputs = [];
            var title = document.querySelector('#title');
            this.input_file.files = null;
            this.images = null;
            this.onImagesChanged();
        }

        PostManager.prototype.is_update_form = function(){
            let element = document.querySelector('#editor');
            return element != null && element.dataset.action === "update";
        }

        PostManager.prototype.validate = function(){
            // if(this.validators){
            //     return this.validators.every((f)=>f());
            // }
            return true;
        };

        PostManager.prototype.validateTitle = function(){
            var name = document.querySelector('#name');
            var display_name = document.querySelector('#display-name');
            // if(!name || !display_name || !name.value.lenght || !display_name.value.length){
            //     console.log("name & display name errors");
            //     return false;
            // }
            return true;
        };

        PostManager.prototype.onImagesChanged = function(){
            this.drag_area.classList.toggle('active', this.images && (this.images.length > 0));
        };

        PostManager.prototype.validateImages = function(){
            
            if(!this.images  || !this.input_file.files.length){
                console.log(" images errors");
                return false;
            }
            return true;
        };

        PostManager.prototype.onUploadResponse = function(data){
            
            if(!data.success){
                var msg = {
                    content : data.message,
                    level : data.success
                }
                notify(msg);
                return;
            }
            let editor_element = document.querySelector('#editor');
            editor_element.dataset.action = "update";
            editor_element.dataset['post'] = data.post.post_uuid;
            
        };

        PostManager.prototype.upload = function(){
            let self = this;
            let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
            let title = document.querySelector('input[name="title"]');
            let editor_element = document.querySelector('#editor');
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            formData.append('title', title.value);
            formData.append('content', JSON.stringify(post_content));
            formData.append('author', editor_element.dataset.author);
            let url = this.is_update_form() ? '/api/update-post/' + editor_element.dataset.post + '/' : '/api/create-post/';
            var options = {
                //url : url,
                type: 'POST',
                method: 'POST',
                enctype : 'multipart/form-data',
                data : formData,
                dataType : 'json',
            };
            let fetch_options = {
                method : 'POST',
                body: formData
            };
            ajax_api.fetch_api(url, fetch_options).then(function(response){
                var msg = {
                    content : response.message,
                    level : response.success
                }
                self.onUploadResponse(response);
                notify(msg);
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                
            });
            /*
            ajax_api.ajax(options).then(function(response){
                var msg = {
                    content : response.message,
                    level : response.success
                }
                notify(msg);
                self.onUploadResponse(response);
                
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                
            });
            */
        };

        return PostManager;

    })();

    function kiosk_update(event){
        document.getElementById('main-image').src = event.target.src;
        $(".kiosk-image").removeClass('active').filter(event.target).addClass("active");
    }

    $(document).ready(function(){
        if(window){
            window.notify = notify;
        }
        create_editor();
        notification_wrapper = $('#notifications-wrapper');
        messages = $('#messages', notification_wrapper);
        //onDragInit();
        notify_init(notification_wrapper, messages);
        var listfilter = new ListFilter();
        fileUpload = new FileUpload();
        postManager = new PostManager();
        postManager.init();
        
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