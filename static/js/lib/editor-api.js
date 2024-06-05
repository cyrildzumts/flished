define(['require','ajax_api', 'element_utils', 'editor/editor', 
    'editor/plugins/header.min','editor/plugins/list.min', 'editor/plugins/link.min',
    'editor/plugins/checklist.min', 'editor/plugins/quote.min', 'editor/plugins/table.min',
    'editor/plugins/inline-image','editor/plugins/editor-emoji.min',
    'editor/plugins/code.min','editor/plugins/inline-code.min',
    'editor/plugins/marker.min', 'editor/plugins/image.min'
    ], function(require,ajax_api, element_utils,EditorJS) {
    'use strict';

    const Header = require('editor/plugins/header.min');
    const List = require('editor/plugins/list.min');
    const Link = require('editor/plugins/link.min');
    const Code = require('editor/plugins/code.min');
    const Marker = require('editor/plugins/marker.min');
    const InlineCode = require('editor/plugins/inline-code.min');
    const Checklist = require('editor/plugins/checklist.min');
    const Quote = require('editor/plugins/quote.min');
    const Emoji = require('editor/plugins/editor-emoji.min');
    const Table = require('editor/plugins/table.min');
    const InlineImage = require('editor/plugins/inline-image');
    const ImageTool = require('editor/plugins/image.min');
    
    const EDITOR_CHANGE_TIMEOUT = 1000; // 1s
    const SAVE_DRAFT_INTERVAL = 10000; // 10s
    const POST_STATUS_DRAFT = 0
    const POST_STATUS_PUBLISH = 1
    const POST_STATUS_SCHEDULED = 5
    const BACKEND_IMAGE_UPLOAD_URL = "/api/upload-image/";
    const BACKEND_IMAGE_FROM_URL = "/api/fetch-image-url/";
    const csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
    let AUTO_SAVE_TIMER;
    let editor;
    let post_content;
    let json_input;
    let postManager;
    let headers = [null, "h1","h2", "h3", "h4", "h5", "h6"];
    let LIST_TYPE_MAPPING = {
        ordered: 'ol',
        unordered:'ul',
        checklist: 'ul'
    };

    let BLOCK_MAPPING = {
        'header': render_header,
        'paragraph': render_paragraph,
        'table': render_table,
        'list': render_list,
        'linkTool': render_linkTool,
        'checklist': render_checklist,
        'quote': render_quote,
        'image': render_inlineImage,
        'emoji': render_emoji,
        'image2': render_image,
    };
    function render_emoji(emoji){
        console.log(emoji);
        return emoji.data.text;
    }

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

    function render_image(image){
        let node = element_utils.create_element_api({
            element: "img",
            options : {
                id:image.id,
                src: image.data.file.url,
                title: image.data.caption,
                caption: image.data.caption,
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
        post_content = saved_data;
    }

    function on_editor_change(api, event){
        api.saver.save().then(on_editor_save).catch((error)=>{
            console.log("Error on saving editor content after changes : ", error);
        });
    }

    function fetch_credential(callback){
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if(csrfmiddlewaretoken == null){
            return;
        }
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
        let editor_tag = document.getElementById('editor');
        let init_data = {};
        if(json_input && json_input.value.length){   
            try {
                init_data = JSON.parse(json_input.value);
                post_content = init_data;
            } catch (error) {
                console.warn("error on parsing json data from description_json value : %s", json_input.value);
                console.error(error);
                init_data = {};
            }
        }
        
        editor = new EditorJS({
            holder:'editor',
            tools: {
                header : {
                    class : Header,
                    inlineToolbar : true
                },
                /*
                image: {
                    class : InlineImage,
                    inlineToolbar : true,
                    config: {
                        embed : {
                            display: true
                        },
                        unsplash : unsplash_conf
                    }
                },*/
                image : {
                    class: ImageTool,
                    endpoints: {
                        byFile: BACKEND_IMAGE_UPLOAD_URL,
                        byUrl : BACKEND_IMAGE_FROM_URL,
                        additionalRequestData : {
                            'csrfmiddlewaretoken' : csrfmiddlewaretoken.value
                        }
                    }
                },
                list: {
                    class: List,
                    inlineToolbar: true
                },
                linkTool: {
                    class: Link,
                    inlineToolbar: true,
                    config:{
                        endpoint:"/api/fetchUrl/",
                    }
                },
                code: Code,
                emoji: {
                    class:Emoji,
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
                        quotePlaceholder: editor_tag.dataset.quotePlaceholder,
                        captionPlaceholder: editor_tag.dataset.captionPlaceholder,
                    },
                },
                Marker:{
                    class:Marker,
                    shortcut: 'CMD+SHIFT+M',
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
            autofocus: true,
            data: init_data,
            placeholder: editor_tag.dataset.placeholder,
            onReady: function(){
                console.log("Editor is ready" , editor);
            },
            onChange: (api, event) =>{
                if(AUTO_SAVE_TIMER){
                    clearTimeout(AUTO_SAVE_TIMER);
                }
                AUTO_SAVE_TIMER = setTimeout(on_editor_change, EDITOR_CHANGE_TIMEOUT, api, event);
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
        console.log("Editor loaded", editor);

        return editor;
    }


    function create_editor(){
        let editor_tag = document.getElementById('editor');
        json_input = document.getElementById('content');
        if( !editor_tag ){
            return;
        }
        fetch_credential(editor_init);
    }

    function preview_post(){
        let form = document.getElementById('preview-form');
        let preview_title = document.getElementById('preview-title');
        let title = document.getElementById('title');
        let content = document.getElementById('preview-content');
        if(!title || !title.value.length){
            notify({'content' : preview_title.dataset.missingMessage, 'level': 'info'});
            title.classList.add('warning');
            return;
        }
        title.classList.remove('warning');
        preview_title.value = title.value;
        if(!post_content.blocks.length){
            notify({'content' : content.dataset.missingMessage, 'level': 'info'});
            return;
        }
        content.value = JSON.stringify(post_content);
        form.submit();
    }

    let ImageManager = (function(){
        function ImageManager(form, drag_area_selector){
            this.form = form;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
            this.input_files;
            this.drag_area_selector = drag_area_selector;
        }
        ImageManager.prototype.init = function(){
            let self = this;
            let drag_area_selector = this.drag_area_selector || ".drag-area";
            this.drag_areas = document.querySelectorAll(this.drag_area_selector);
            if(!this.drag_areas){
                return;
            }
            this.input_files = document.querySelectorAll('.files-upload-input');
            if(!this.input_files){
                return;
            }
            $(drag_area_selector).on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                this.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                this.classList.remove('on-drag');
            }).on('drop', function(e){
                let file_input = document.getElementById(this.dataset.input);
                if(file_input){
                    file_input.files = e.originalEvent.dataTransfer.files;
                    this.classList.add('active');
                    self.imagesPreview(this);
                }
            });
            $('.files-upload-input').on('change', function(e){
                let drag_area = document.getElementById(this.dataset.dragarea);
                if(this.files){
                    drag_area.classList.remove('active');
                }
                self.imagesPreview(drag_area);
            });
            $('.js-uploaded-files-clear').on('click', function(event){
                let files_container = document.getElementById(this.dataset.target);
                while(files_container.firstChild){
                    files_container.removeChild(files_container.firstChild);
                }
                let input = document.getElementById(files_container.dataset.input);
                let drag_area = document.getElementById(this.dataset.dragarea);
                input.files = null;
                let li = document.createElement('li');
                let span = document.createElement('span');
                span.innerText = "No images";
                li.appendChild(span);
                files_container.appendChild(li);
                drag_area.classList.remove('active');
            });
        }
        ImageManager.prototype.getFiles = function(){
            return this.input_files;
        }
        ImageManager.prototype.imagesPreview = function(drag_area){
            let li;
            let img;
            let input = document.getElementById(drag_area.dataset.input);
            let files_container = drag_area.querySelector('.file-list');
            while(files_container.firstChild){
                files_container.removeChild(files_container.firstChild);
            }
            let f;
            for(let i = 0; i < input.files.length; i++){
                f = input.files[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                info.classList.add('padding');
                li.appendChild(info);
                files_container.appendChild(li);
            }
            $('.js-uploaded-files-clear', drag_area).show();
        };

        ImageManager.prototype.clearImages = function(drag_area){
            let files_container = document.querySelector('.file-list', drag_area);
            if(!files_container){
                return;
            }
            while(files_container.firstChild){
                files_container.removeChild(files_container.firstChild);
            }
            let input_file = document.getElementById(drag_area.dataset.input);
            input_file.files = null;
            let li = document.createElement('li');
            let span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            files_container.appendChild(li);
            drag_area.classList.remove('active');
        };
        ImageManager.prototype.clear = function(){
            if(this.input_files){
                this.input_files.forEach(function(v,i){
                    v.files = null;
                });
            }
        }

        return ImageManager;
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
            this.post_status = 0;
        };
        PostManager.prototype.init = function(){
            var self = this;
            this.created_product_container = document.querySelector('#created-post-link');
            this.created_product_link = document.querySelector('#created-post-link a');
            this.files_container = document.querySelector('.file-list');

            this.imageManager = new ImageManager(this.form);
            this.imageManager.init();
            let scheduled_at = document.getElementById('scheduled_at');
            if(scheduled_at){
                ["input","keyup","change"].forEach(function(eventName){
                    scheduled_at.addEventListener(eventName,function(event){
                        self.validateSchedule(scheduled_at);
                    });
                });
            }
            $(".js-create-post-btn").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    self.post_status = POST_STATUS_DRAFT;
                    self.upload();
                }
            });
            $(".js-preview-post").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    preview_post();
                }
            });
            $(".js-publish-btn").on('click', function(e){
                e.preventDefault();
                e.stopPropagation();
                if(post_content){
                    let scheduled_at = document.getElementById("scheduled_at");
                    if(scheduled_at && scheduled_at.value.length != 0){
                        self.post_status = POST_STATUS_SCHEDULED;
                    }else{
                        self.post_status = POST_STATUS_PUBLISH;
                    }
                    self.upload();
                }
            });
            console.log("PostManager initialized");
        };

        PostManager.prototype.clear = function(){
            var inputs = [];
            var title = document.querySelector('#title');
            this.input_file.files = null;
            this.images = null;
            this.imageManager.clear();
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

        PostManager.prototype.validateSchedule = function(scheduled_at){
            let is_valid = true;
            if(scheduled_at && scheduled_at.value.length){
                let NOW = Date.now()
                let scheduled_at_Date = new Date(scheduled_at.value);
                if(scheduled_at_Date < NOW){
                    scheduled_at.classList.add("error");
                    is_valid = false;
                }else{
                    scheduled_at.classList.remove("error");
                }
            }
            console.log("Schedule valid : %s", is_valid);
            console.log("scheduled_at value : %s", scheduled_at.value);
            return is_valid;
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
                
                return;
            }
            let editor_element = document.querySelector('#editor');
            let link_container = document.getElementById('post-link-container');
            let link = link_container.querySelector('#post-link');
            link.href = data.url;
            link_container.classList.remove('hidden');
            editor_element.dataset.action = "update";
            editor_element.dataset['post'] = data.post.post_uuid;
            
        };

        PostManager.prototype.upload = function(){
            let self = this;
            let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
            let title = document.getElementById('title');
            let editor_element = document.getElementById('editor');
            let category = document.querySelector("input[type='radio'][name='category']:checked");
            let scheduled_at = document.getElementById('scheduled_at');
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value);
            formData.append('title', title.value);
            formData.append('content', JSON.stringify(post_content));
            formData.append('author', editor_element.dataset.author);
            
            let input_image = document.getElementById('image');
            if(input_image != null && input_image.files != null && input_image.files.length > 0){
                formData.append('image', input_image.files[0]);
            }
            if(category){
                formData.append('category', category.value);
            }
            if(!this.validateSchedule(scheduled_at)){
                return;
            }
            formData.append('post_status', this.post_status);
            formData.append('scheduled_at', scheduled_at.value);
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
                let msg = {
                    content : response.message,
                    level : response.success
                }
                notify(msg);
                self.onUploadResponse(response);
            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                
            });

        };
        return PostManager;

    })();

    $(document).ready(function(){
        postManager = new PostManager();
        postManager.init();
        create_editor();
    });
});