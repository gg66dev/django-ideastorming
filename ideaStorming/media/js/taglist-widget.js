

(function () {
    var taggle,tagValueList,tags;

    //hide original tag input field.
    $("#id_tags").hide();

    var strValues = $("#id_tags").val();
    if (strValues.length > 0 ) {
        var input_tags = strValues.split(',');
        taggle = new Taggle('tag_container', {
            tags: input_tags
        });
    } else {
        taggle = new Taggle('tag_container');
    }


    //call taggle.js for the tags field.    

    $("#save-btn").click(function(e){

        tagValueList = taggle.getTagValues();
        if (tagValueList.length > 0) {
            tags = tagValueList.join(",");
            $("#id_tags").val(tags);
            return true;
        }
        //todo: if tag list is empty display error message.
        return false;
    });


})();


