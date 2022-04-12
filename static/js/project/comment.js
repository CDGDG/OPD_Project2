$(document).ready(function(){
    $('#create_comment_btn').click(function(){
        contents = $("#id_comment").val()
        if(contents.trim() == ""){
            $(this).tooltip("show")
        }
        
        $.ajax({
            url: commenturl,
            type: 'POST',
            data: {contents: contents, parentcomment: parentcomment, 'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()},
            dataType: 'json',
            success: function(response){
                if(response['data']=="success"){
                    console.log('댓글 작성 성공')
                }
            }
        })
    })
})