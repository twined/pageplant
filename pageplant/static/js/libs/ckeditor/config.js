/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// %REMOVE_START%
	// The configuration options below are needed when running CKEditor from source files.
	//config.plugins = 'dialogui,dialog,about,basicstyles,clipboard,button,toolbar,enterkey,entities,floatingspace,wysiwygarea,indent,indentlist,fakeobjects,link,list,undo,blockquote,templates,resize,lineutils,widget,image2,imagebrowser,image,oembed,pastetext,removeformat,sourcearea,popup,filebrowser';
	config.skin = 'moono';
	// %REMOVE_END%

	// Define changes to default configuration here.
	// For the complete reference:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for a single toolbar row.
	config.toolbarGroups = [
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'forms' },
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'tools' },
		//{ name: 'others' },
		{ name: 'about' }
	];

	// The default plugins included in the basic setup define some buttons that
	// we don't want too have in a basic editor. We remove them here.
	config.removeButtons = 'Cut,Copy,Paste,Undo,Redo,Anchor,Underline,Strike,Subscript,Superscript';

	// Let's have it basic on dialogs as well.
	config.removeDialogTabs = 'link:advanced';

	config.plugins = 'resize,link,wysiwygarea,toolbar,sourcearea,image,imagebrowser,filebrowser,blockquote,basicstyles,stylescombo,pastetext,removeformat,list,oembed';
	config.extraAllowedContent = 'h1 h2 h3 h4 h5 h6';
	config.stylesSet =[
	    { name: 'Overskrift 1', element: 'h1' },
	    { name: 'Overskrift 2', element: 'h2' },
	    { name: 'Overskrift 3', element: 'h3' },
	    { name: 'Overskrift 4', element: 'h4' },
	    { name: 'Overskrift 5', element: 'h5' },
	    { name: 'Overskrift 6', element: 'h6' },
	];
	config.height = '400px';
	config.resize_dir = 'vertical';
	config.filebrowserBrowseUrl = '/admin/postbilder/browser/';
	config.on = {
	    instanceReady: function() {
	        this.dataProcessor.htmlFilter.addRules( {
	            elements: {
	                img: function( el ) {
	                    el.className = 'img-responsive';
	                    el.attributes.class = 'img-responsive';
	                    el.attributes.style = '';
	                }
	            }
	        } );
	    }
	};

};
