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
    $editorEl = $('#id_body');
    $leadEl = $('#id_lead');
    $slugEl = $('#id_slug');
    $tagsEl = $('#id_tags');
    $titleEl = $('#id_header');

    froalaLoadURL = "/admin/sider/imgs/browser/";
    froalaUploadURL = "/admin/sider/imgs/froala-upload/";

    // set that pesky token!
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    // backbone
    new app.Posts.MainView();
    new app.Posts.HeaderView({header: $titleEl, slug: $slugEl});
    // no lead on this page
    // new app.Posts.LeadView({lead: $leadEl});
    new app.Posts.ToggleTemplateLockView();

    // autocomplete tags
    $tagsEl.autocomplete({
        serviceUrl: 'autocomplete-tags/',
        deferRequestBy: 500,
        tabDisabled: true,
        delimiter: ', '
    });
    // froala editor
    $editorEl.editable({
        theme: 'gray',
        language: 'nb',
        inlineMode: false,
        // Set the load images request URL.
        imagesLoadURL: froalaLoadURL,
        imageUploadURL: froalaUploadURL,
        imageUploadParams: {
            "upload_to": "testing/path"
        },

        defaultImageWidth: 0,
        defaultBlockStyle: {
            'f-test': 'Test'
        },
        minHeight: 300,
        height: 500,
        plainPaste: true
    }).on('editable.imageError', function (e, editor, error) {
        // Custom error message returned from the server.
        alert(error.message);
    });

    // backbone
    new app.Posts.MainView();
});