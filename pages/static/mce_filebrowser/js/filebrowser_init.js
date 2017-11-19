function mce_filebrowser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        url: "/filebrowser/" + type + "/",
        width: 800,
        height: 600,
        movable: true,
        inline: true,
        close_previous: "yes"
    }, {
        window : win,
        input : field_name
    });  
}
