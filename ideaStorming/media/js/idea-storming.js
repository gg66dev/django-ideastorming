var app = (function ($) {
    var app = {},
        pageLogic = {
            home: function () {
                //display login errors like alerts
                $("input[name='error']").each(function() {
                    alert($( this ).val());
                });
            },
            new_user: function () {

            },
            new_project: function () {
              /*  //use taggle to catch tags {https://sean.is/poppin/tags}.
                var $tag_input = $("#id_tags");
                $tag_input.hide();
                $tag_input.val("algo");
                $tag_input.parent().html("<div id='tag_container'></div>");
                new Taggle('tag_container');

                //when press save, move tags to hiden input.
                $("#save-btn").click(function () {
                    console.log();
                });*/

            }

        };
        
    app.init = function(args){
        //setup the page
        var page = (args.page !== undefined && args.page !== null) ? args.page : "";
        if (page === "") {
            console.error("var page not defined");
            return;
        }
        //call the page loggic according to the loaded page.
        if (page === 'home')
            pageLogic.home();
        else if (page === 'new-user')
            pageLogic.new_user();
        else if (page === 'new-project')
            pageLogic.new_project();
    }
    return app;
}(jQuery));



$(document).ready(function () {
    var page = $("#current_page").val();
    app.init({ 'page': page });
});


