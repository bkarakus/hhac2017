tinyMCE.init({
		// General options
		mode : "specific_textareas",
		editor_deselector : "mceNoEditor",
		theme : "advanced",
		skin : "o2k7",
	    height : "400",
	    width: "800",
	    tab_focus : ":prev,:next",
	    content_css : "/media/default/css/default.css",
	    button_tile_map : true,
	    plugins : "advimage, safari, fullscreen,media,table,contextmenu",
	    convert_urls : false,
	    theme_advanced_buttons1 : "bold, italic, underline, |, justifyleft," +
	                              "justifycenter, justifyright, justifyfull, |," +
	                              "bullist,numlist, |, outdent, indent, |, image, |, undo," +
	                              "redo, |, code, link, unlink, |," +
	                              "removeformat, fullscreen,media," +
	    						  "styleselect, formatselect, fontsizeselect ,fontselect, ",
	    theme_advanced_buttons2: "forecolor, backcolor,|,insertdate,inserttime,preview,|,tablecontrols",
	    theme_advanced_buttons3: "",
	    theme_advanced_buttons4: "",
	    theme_advanced_toolbar_location : "top",
	    theme_advanced_toolbar_align : "left",
	    file_browser_callback: "mce_filebrowser",
	});