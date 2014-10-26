//

(function($){
    $.fn.outerHTML = function(s) {
        return s
            ? this.before(s).remove()
            : jQuery("<p>").append(this.eq(0).clone()).html();
    };
    $.fn.getStyleObject = function(){
        var dom = this.get(0);
        var style;
        var returns = {};
        if(window.getComputedStyle){
            var camelize = function(a,b){
                return b.toUpperCase();
            };
            style = window.getComputedStyle(dom, null);
            for(var i = 0, l = style.length; i < l; i++){
                var prop = style[i];
                var camel = prop.replace(/\-([a-z])/g, camelize);
                var val = style.getPropertyValue(prop);
                returns[camel] = val;
            }
            return returns;
        }
        if((style = dom.currentStyle)) {
            for(var props in style) {
                returns[props] = style[props];
            }
            return returns;
        }
        return this.css();
    };
})(jQuery);

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}

$(document).ready(function() {
    // froala editor
    $('#id_body').editable({
        theme: 'gray',
        language: 'nb',
        inlineMode: false,
        // Set the load images request URL.
        imagesLoadURL: "/admin/sider/imgs/browser/",
        imageUploadURL: "/admin/sider/imgs/froala-upload/",
        /* uses an Image model so no upload parameters are needed */
        imageUploadParams: {
            "upload_to": ""
        },

        defaultImageWidth: 0,
        defaultBlockStyle: {
            'f-test': 'Test'
        },
        minHeight: 300,
        height: 500,
        plainPaste: true
    }).on('editable.imagesLoadError', function (e, editor, error) {
        // Custom error message returned from the server.
        if (error.code == 0) {
            console.log('Custom error message returned from the server.');
        }

        // Bad link. One of the returned image links cannot be loaded.
        else if (error.code == 1) {
            console.log('Bad link. One of the returned image links cannot be loaded.');
        }

        // Error during HTTP request to load images.
        else if (error.code == 2) {
            console.log('Error during HTTP request to load images.');
        }

        // Missing imagesLoadURL option.
        else if (error.code == 3) {
            console.log('Missing imagesLoadURL option.');
        }

        // Parsing response failed.
        else if (error.code == 4) {
            console.log('Parsing response failed');
        }
    });

    // backbone
    new app.Posts.MainView();

    // autocomplete tags
    $('#id_tags').autocomplete({
        serviceUrl: 'autocomplete-tags/',
        deferRequestBy: 500,
        tabDisabled: true,
        delimiter: ', '
    });
});

/* backbone */

//TODO: fix header slug generation when receiving pasted material.

var app = app || {};
    app.vent = app.vent || _.extend({}, Backbone.Events);
    //app.Images = app.Images || {};
    app.Posts = app.Posts || {};

    /*
    app.Images.UploadModalView = Backbone.View.extend({
        tagName: 'div',
        className: 'modal large',
        id: 'uploadmodal',

        events: {
            'click #modalClose': 'closeModal',
            'click #modalCloseCorner': 'closeModal'
        },

        initialize: function(options) {
            this.render();
            this.populate();
        },

        render: function() {
            this.$el.html(window.JST['modal/img_base']({'header': 'Last opp bilde'}));
            this.$el.modal({'show': true});
            return this;
        },

        populate: function() {
            compiled = JST['modal/upload']();
            $('.modal-body', this.$el).html(compiled);
            $('#imgUpload', this.$el).remove();
            this.createUploader();
        },

        createUploader: function() {
            that = this;
            this.uploader = new qq.FileUploaderBasic({
                button: $('#uploadspan')[0],
                action: '/admin/bilder/last-opp/upload/',
                maxConnections: 1,
                onComplete: function(id, fileName, responseJSON) {
                    console.log(responseJSON);
                    that.createImage(id, responseJSON);
                     if (that.uploader.getInProgress() === 0) {
                        // all files have been uploaded, send us back
                        // to the imgModal picker!

                     }
                },
                onProgress: function(id, fileName, loaded, total) {
                    pct = Math.ceil(loaded / total * 100);
                    $(".fileitem[data-id='"+id+"'] .fileprogress").val(pct).trigger('change');
                    $(".fileitem[data-id='"+id+"'] .filesize").text(that._formatSize(loaded) + ' / ' + that._formatSize(total));
                    console.log(id);
                },
                onSubmit: function(id, fileName) {
                    that.addUpload(id, fileName);
                },
                onError: function(id, fileName, xhr) {
                    $(".fileitem[data-id='"+id+"'] .filestatus").text(xhr.error);
                },
                onUpload: function(id, fileName, xhr){

                },
                debug: true
            });
        },

        addUpload: function(id, fileName) {
            console.log(id + ' - ' + fileName);
            $('#fileuploader').prepend(
                '<div class="row-fluid fileitem-row">' +
                    '<div class="fileitem span12" data-id="' + id + '">' +
                        '<input type="text" class="fileprogress" value="0" />' +
                        '<div class="filename">' + fileName + '</div>' +
                        '<div class="filesize">' + '</div>' +
                        '<div class="filestatus">' + '</div>' +
                    '</div>' +
                '</div>'
            );
            $(".fileitem[data-id='"+id+"'] .fileprogress").knob({
                'width': 30,
                'height': 30,
                'displayInput': false,
                'skin': 'tron',
                'thickness': 0.5
            });

        },

        createImage: function (id, data) {
            if (data.success) {
                // make the progress indicator green
                $('.fileitem[data-id="'+id+'"] .fileprogress').trigger(
                    'configure', {"fgColor":"#51A351"}
                );
                $(".fileitem[data-id='"+id+"'] .filestatus").html(
                    '<i class="icon-ok-sign"> </i>' + ' Lastet opp OK.'
                );
                // make sure we can see the uploaded images container
                $('#uploaded-images').show();
                // append the thumb and fade in
                $('<div class="upthumb"><img id="image-' + data.id + '" class="upimg" src="' + data.thumbnail_url + '" /></div>').hide().appendTo('#uploaded-images').fadeIn();
            } else {
                $('.fileitem[data-id="'+id+'"] .fileprogress').trigger('configure', {"fgColor":"#AA0000"});
                $(".fileitem[data-id='"+id+"'] .filestatus").html('<i class="icon-minus-sign"> </i> ' + data.error);
            }
        },

        _formatFileName: function(name){
            if (name.length > 33){
                name = name.slice(0, 19) + '...' + name.slice(-13);
            }
            return name;
        },

        _formatSize: function(bytes) {
            var i = -1;
            do {
                bytes = bytes / 1024;
                i++;
            } while (bytes > 99);
            return Math.max(bytes, 0.1).toFixed(1) + ['kB', 'MB', 'GB', 'TB', 'PB', 'EB'][i];
        },

        closeModal: function(e) {
            if (this.$el.length !== 0) {
                this.$el.modal('hide');
                this.$el.remove();
            }
        }
    }),

    app.Images.ImagePickerModalView = Backbone.View.extend({
        tagName: 'div',
        className: 'modal large',
        id: 'imgpickermodal',

        events: {
            'click #modalClose': 'closeModal',
            'click #modalCloseCorner': 'closeModal'
        },

        initialize: function(options) {
            this.render();
            this.populate();
            app.vent.on('modal:images:pickedimage', this.pickedImage, this);
        },

        render: function() {
            this.$el.html(window.JST['modal/img_base']({'header': 'Velg bilde'}));
            this.$el.modal({'show': true});
            $('#imgUpload', this.$el).remove();
            $('#imgMainBtn', this.$el).remove();
            return this;
        },

        populate: function() {
            that = this;
            compiled = JST['modal/pickimage']();
            $('.modal-body', this.$el).html(compiled);
            $('.modal-body', this.$el).append('<div id="imgModalPick"></div>');
            $('.modal-body #imgModalPick', this.$el).load('/imgin/get-images/', that.setImageClickCallback);
        },

        pickedImage: function(e) {
            // an image was clicked in the select image portion of the
            // modal. parse data, and return the populated form.
            attrs_dict = {
                'url': $(".imgin-url", e.currentTarget).text(),
                'format': 'large left',
                'link': '',
                'title': '',
                'credits': '',
                'caption': ''
            };

            imagemodal = new app.Images.ImageModalView(attrs_dict);
            this.closeModal();
        },

        // set the callback. this gets called after ajax.load() is finished.
        setImageClickCallback: function() {
            $(document).off('click.imgmodalpick', '#imgModalPick .imgin-img');
            $(document).on('click.imgmodalpick', '#imgModalPick .imgin-img', function(e) {
                app.vent.trigger('modal:images:pickedimage', e);
            });
        },

        closeModal: function(e) {
            $(document).off('click.imgmodalpick', '#imgModalPick .imgin-img');
            if (this.$el.length !== 0) {
                this.$el.modal('hide');
                this.$el.remove();
            }
        }
    }),

    // imagemodal
    app.Images.ImageModalView = Backbone.View.extend({
        tagName: 'div',
        className: 'modal large',
        id: 'imgmodal',

        events: {
            'click #modalClose': 'closeModal',
            'click #modalCloseCorner': 'closeModal',
            'click #imgUpload': 'upload',
            'click #imgPickBtn': 'pickImage'
        },

        initialize: function(options) {
            this.render();
            this.populate(options);
            app.vent.on('modal:images:close', this.closeModal, this);
            app.vent.on('modal:images:sizechange', this.changeSize, this);
            app.vent.off('modal:images:parse');
            app.vent.on('modal:images:parse', this.parseImageForm, this);
        },

        pickImage: function(e) {
            // clicked the pick image button. show modal.
            imagepicker = new app.Images.ImagePickerModalView();
            this.closeModal();
            e.preventDefault();
        },

        upload: function(e) {
            uploadmodal = new app.Images.UploadModalView();
            this.closeModal();
            e.preventDefault();
        },

        closeModal: function(e) {
            $(document).off('click.imgmainbtn', '#imgMainBtn');

            if (this.$el.length !== 0) {
                this.$el.modal('hide');
                this.$el.remove();
            }
        },

        onSizeChange: function(e) {
            // size radio has changed
            app.vent.trigger('modal:images:sizechange', e);
        },

        changeSize: function(e) {
            // changes the size radios, and img url
            url = $('#imgin-edit-url').val();
            if (url.length === 0) {
                return;
            }
            // first find out what we are changing to
            newSize = $('input[name=size]:checked').val().charAt(0);
            // find the old value
            if (url.indexOf('\/s\/') != -1) {
                oldSize = 's';
            } else if (url.indexOf('\/m\/') != -1) {
                oldSize = 'm';
            } else if (url.indexOf('\/l\/') != -1) {
                oldSize = 'l';
            } else {
                alert('not from our server!');
            }
            url = url.replace('/' + oldSize + '/', '/' + newSize + '/');
            $('#imgin-edit-url').val(url);
        },

        populate: function(attrs) {
            that = this;
            // format
            checked_left = (attrs['format'].indexOf("left") != -1) ? ' checked' : '';
            checked_right = (attrs['format'].indexOf("right") != -1) ? ' checked' : '';
            checked_large = (attrs['format'].indexOf("large") != -1) ? ' checked' : '';
            checked_medium = (attrs['format'].indexOf("medium") != -1) ? ' checked' : '';
            checked_small = (attrs['format'].indexOf("small") != -1) ? ' checked' : '';

            // sane defaults for attrs dict
            attrs['title'] = attrs['title'] || '';
            attrs['caption'] = attrs['caption'] || '';
            attrs['credits'] = attrs['credits'] || '';
            attrs['link'] = attrs['link'] || '';

            compiled = JST['modal/img'](attrs);

            $('#imgmodal .modal-body').html(compiled);

            $(document).off('click.imgmainbtn', '#imgMainBtn');
            $(document).on('click.imgmainbtn', '#imgMainBtn', function(e) {
                app.vent.trigger('modal:images:parse', e);
            });

            $('input[name=size]').change(this.onSizeChange);
        },

        parseImageForm: function(e) {
            justifyArray = $('#imgEditJustifyForm').serializeArray();
            sizeArray = $('#imgEditSizeForm').serializeArray();
            console.log(justifyArray);
            console.log(sizeArray);
            formatString = sizeArray[0].value + ' ' + justifyArray[0].value;

            longest = 0;
            newline = "\n";
            title = credits = caption = link = '';
            if ($('#imgin-edit-title').val()) {
                title = '| title: ' + $('#imgin-edit-title').val() + newline;
                longest = (title.length > longest) ? title.length : longest;
            }
            if ($('#imgin-edit-credits').val()) {
                credits = '| credits: ' + $('#imgin-edit-credits').val() + newline;
                longest = (credits.length > longest) ? credits.length : longest;
            }
            if ($('#imgin-edit-caption').val()) {
                caption = '| caption: ' + $('#imgin-edit-caption').val() + newline;
                longest = (caption.length > longest) ? caption.length : longest;
            }
            format = '| format: ' + formatString + newline;
            longest = (format.length > longest) ? format.length : longest;
            url = '| url: ' + $('#imgin-edit-url').val() + newline;
            longest = (url.length > longest) ? url.length : longest;
            if ($('#imgin-edit-link').val()) {
                link = '| link: ' + $('#imgin-edit-link').val() + newline;
                longest = (link.length > longest) ? link.length : longest;
            }

            text = '|-[image]' + Array(longest - 7).join("-") + newline +
                   title +
                   credits +
                   caption +
                   format +
                   url +
                   link +
                   '|' + Array(longest).join("-") + newline;

            var editor = ace.edit("ace");
            editor.session.doc.replace(editor.getSelection().getRange(), text);

            app.vent.trigger('modal:images:close', e);
        },

        render: function() {
            this.$el.html(window.JST['modal/img_base']({'header': 'Sett inn bilde'}));
            this.$el.modal({'show': true});
            return this;
        }
    }),
    */

    app.Posts.MainView = Backbone.View.extend({

        el: 'body',

        events: {
            'submit form': 'clickSubmit',
        },

        initialize: function() {
            that = this;

            new app.Posts.LeadView();
            new app.Posts.HeaderView();
            new app.Posts.KeywordsView();
            new app.Posts.ToggleTemplateLockView();

            this.isDirty = false;
            app.vent.on('posts:change', this.markDirty, this);

            window.onbeforeunload = function() {
                if (that.isDirty) {
                    return 'Du har foretatt endringer på denne siden ' +
                           'uten å lagre disse. Ved å navigere bort ' +
                           'vil disse endringene gå tapt.';
                }
            };
        },

        clickSubmit: function(e) {
            form = this.checkForm();
            if (form['valid'] === false) {
                e.preventDefault();
            }
            window.onbeforeunload = $.noop();
            editor_html = '<div>' + $("#id_body").editable("getHTML") + '</div>';
            var elements = $(editor_html);
            elements.find('*').removeAttr('contenteditable');
            $("#id_body").editable("setHTML", elements.html(), true);
        },

        checkForm: function() {
            var form = {
                'valid': true,
                'errors': []
            };
            if ($('#id_header').val() === '') {
                form['errors'].push('Overskrift kan ikke være blank.');
                form['valid'] = false;
                $('#id_header').parent().parent().addClass('error');
                $('.controls', $('#div_id_header')).append('<span class="help-inline"><strong><i class="icon-hand-up"></i> Feltet er påkrevet.</strong></span>');
                $('html, body').animate({
                    scrollTop: 0
                }, 5);
            }

            // get the body from froala!
            console.log('clean bodytext here.');
            app.vent.trigger('redactor:clean');

            return form;
        },

        markDirty: function() {
            this.isDirty = true;
        }
    }),

    app.Posts.ToggleTemplateLockView = Backbone.View.extend({
        el: '#toggleTemplateLock',
        sourceEl: '.froala-element',

        locked: true,

        events: {
            'click': 'toggleTemplateLock'
        },

        initialize: function() {
            this.lockTemplate(this.sourceEl);
        },

        lockTemplate: function(el) {
            $('.locked', el).each(function() {
                $(this).attr('contenteditable', 'false');
            });
            this.locked = true;
        },

        unlockTemplate: function(el) {
            $('.locked', el).each(function() {
                $(this).attr('contenteditable', 'true');
            });
            this.locked = false;
        },

        toggleTemplateLock: function(e) {
            if (this.locked) {
                this.unlockTemplate(this.sourceEl);
                this.$el.html('<i class="fa fa-lock"> </i> Lås mal');

            } else {
                this.lockTemplate(this.sourceEl);
                this.$el.html('<i class="fa fa-lock"> </i> Lås opp mal');
            }
            e.preventDefault();
        }
    }),

    app.Posts.KeywordsView = Backbone.View.extend({
        el: '#btnGetKeywords',
        keywordsEl: '#id_meta_keywords',
        sourceEl: '#id_body',
        buttonEl: '#btnGetKeywords',
        url: 'get-keywords/',

        events: {
            'click': 'getKeywords'
        },

        initialize: function() {

        },

        getKeywords: function(e) {
            $.get(
                this.url,
                {text: $(this.sourceEl).val()},
                function(result) {
                    $('#id_meta_keywords').text(result['keywords']);
            });
            e.preventDefault();
        }
    }),

    app.Posts.LeadView = Backbone.View.extend({
        el: '#id_lead',

        events: {
            'keydown': 'change',
            'keyup': 'change'
        },

        change: function(e) {
            app.vent.trigger('posts:lead:change');
            app.vent.trigger('posts:change');
        }
    }),

    app.Posts.HeaderView = Backbone.View.extend({
        el: '#id_header',
        slugEl: '#id_slug',
        statusEl: '.slug-status',
        url: 'check-slug/',

        events: {
            'keydown': 'change',
            'keyup': 'change'
        },

        initialize: function() {
            this.$statusEl = $(this.statusEl);
            this.$slugEl = $(this.slugEl);
            this.$el.slugIt({
                output: this.slugEl,
                map: { 'æ': 'ae', 'ø': 'oe', 'å': 'aa' },
                space: '-'
            });
            app.vent.on('posts:header:change', $.debounce(this.checkSlug, 400), this);
        },

        checkSlug: function() {
            that = this;
            slug = this.$el.val();

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

            $.ajax({
                type: 'GET',
                url: this.url,
                data: {'slug': slug},
                success: function(data) {that.onSuccess(data, that);},
                dataType: 'json'
            });
        },

        onSuccess: function(data, that) {
            if (data.status == 200) {
                app.vent.trigger('posts:header:success', data);
                that.slugSuccess();
            } else if (data.status == 400) {
                app.vent.trigger('posts:header:error', data);
                that.slugError();
            } else {
                app.vent.trigger('posts:header:exists', data);
                that.slugExists();
            }
        },

        showTooltip: function(title) {
            $('#id_header').tooltip({
                'title': title,
                'trigger': 'manual',
                'placement': 'bottom'
            });
            $('#id_header').tooltip('show');
        },

        hideTooltip: function() {
            $('#id_header').tooltip('destroy');
        },

        slugExists: function() {
            $('#id_header').parent().parent().removeClass('has-success');
            $('#id_header').parent().parent().addClass('has-error');
            this.showTooltip('Denne overskriften eksisterer allerede.');
            this.disableSubmitButton();
        },

        slugError: function() {
            $('#id_header').parent().parent().removeClass('has-success');
            $('#id_header').parent().parent().addClass('has-error');
            this.showTooltip('Ugyldig overskrift.');
            this.disableSubmitButton();
        },

        slugSuccess: function() {
            $('#id_header').parent().parent().removeClass('has-error');
            $('#id_header').parent().parent().addClass('has-success');
            this.hideTooltip();
            this.enableSubmitButton();
        },

        disableSubmitButton: function() {
            $("input[type=submit]").attr('disabled', 'disabled');
            $("input[type=submit]").removeClass('btn-primary').addClass('btn-error');

        },

        enableSubmitButton: function() {
            $("input[type=submit]").removeAttr("disabled");
            $("input[type=submit]").removeClass('btn-error').addClass('btn-primary');
        },

        change: function(e) {
            app.vent.trigger('posts:header:change');
            app.vent.trigger('posts:change');
        }
    });