

(function () {
    var taggle,tagValueList,tags;

    //hide original tag input field.
    $("#id_tags").hide();


    //call taggle.js for the tags field.    
    taggle = new Taggle('tag_container');

    $("#save-btn").click(function(e){

        tagValueList = taggle.getTagValues();
        if (tagValueList.length > 0) {
            tags = tagValueList.join(",");
            console.log(tags);
            $("#id_tags").val(tags);
            return true;
        }
        //todo: if tag list is empty display error message.
        return false;
    });


})();


