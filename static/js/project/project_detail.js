$(document).ready(function(){
    // 좋아요
    $("#like").click(function(){
        $.ajax({
            url: $("#like").is('.like')?unlikeurl:likeurl,
            type: "POST",
            data: {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()},
            dataType: 'json',
            success: function(response){
                if(response['data']=="success"){
                    $("#like").toggleClass('unlike like text-danger text-secondary');
                }else{
                    console.log('좋아요 실패')
                }
            }
        })
    })
})