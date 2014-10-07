/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

// Register a templates definition set named "default".
CKEDITOR.addTemplates( 'default', {
	// The name of sub folder which hold the shortcut preview images of the
	// templates.
	imagesPath: CKEDITOR.getUrl( CKEDITOR.plugins.getPath( 'templates' ) + 'templates/images/' ),

	// The templates definitions.
	templates: [
		{
		title: 'Utgivelse',
		image: 'template1.gif',
		description: 'Plateutgivelse.',
		html: '<div class="col-md-6">' +
        '    <div class="frosty-inner music-album">' +
        '        <img class="img-responsive space-that-top" src="/static/img/1234.jpg" />' +
        '        <ul>' +
        '            <li><a href="https://play.spotify.com/album/0FPdW5JkkS6I0qUgbnNRNZ?play=true&utm_source=open.spotify.com&utm_medium=open">' +
        '                                    Spotify' +
        '                                </a></li>' +
        '            <li><a href="http://wimp.no/wweb/album/?album=23200174">' +
        '                                    Wimp' +
        '                                </a></li>' +
        '            <li><a href="https://itunes.apple.com/no/album/1-2-3-4-radio-star/id727114433">' +
        '                                    iTunes' +
        '                                </a></li>' +
        '            <li><a href="http://www.platekompaniet.no/Musikk.aspx/CD/Billie_Van/1_2_3_4_Radio_Star/?id=3762038">' +
        '                                    Platekompaniet' +
        '                                </a></li>' +
        '        </ul>' +
        '    </div>' +
        '</div>'
	},

		{
		title: 'Image and Title',
		image: 'template1.gif',
		description: 'One main image with a title and text that surround the image.',
		html: '<h3>' +
			// Use src=" " so image is not filtered out by the editor as incorrect (src is required).
			'<img src=" " alt="" style="margin-right: 10px" height="100" width="100" align="left" />' +
			'Type the title here' +
			'</h3>' +
			'<p>' +
			'Type the text here' +
			'</p>'
	}
	]
});
