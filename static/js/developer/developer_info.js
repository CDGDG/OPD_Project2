$(document).ready(function(){
    $('#check_password').click(function(){
            var password = $("#current_password").val();
            var check = "check"
            console.log(password)
            $.ajax({
                url: checkPassword_url,
                type:"POST",
                data : {'csrfmiddlewaretoken': $('#csrf_token').val(),'password':password,'check':check},
                datatype:'json',
                success:function(response){
                    if(response.blank){
                        $('#check').html('<p style="color:red">비밀번호를 입력해주세요</p>')
                        return;
                    }else if(response.data == "fail"){
                        $('#check').html('<p style="color:red">비밀번호가 틀립니다</p>')
                        return;
                    }else{
                        location.href = update_url
                    }
                }
            })
    })

    $('#follow').click(function(){
        var developer_id = $('#developer_id').val()
        var check_follow = $('#follow').val()
        $.ajax({
            url: follow_url,
            type:"POST",
            data:{'csrfmiddlewaretoken': $('#csrf_token').val(), 'developer_id':developer_id,'check_follow':check_follow},
            datatype:"json",
            success:function(response){
                location.href = "/developer/info/"+developer_id+"/"
            }
        })
    })


})