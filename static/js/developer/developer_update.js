function readPic(input) {
    if (input.target.files && input.target.files[0]) {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            //$('#pic_preview').attr('src',e.target.result)
            $("[for=id_pic]").css({'background-image': 'url('+e.target.result+')'})
        }
        reader.readAsDataURL(input.target.files[0]);
    }
}
$(document).ready(function(){

    // 언어 체크
    $("input[name='language']:checked").parent('label').addClass('label-color')

    $('#form_id input[type="checkbox"]').not('.noani').change(function(){
        $(this).siblings('label').toggleClass('label-color').text($(this).siblings('label').text() == '비공개'? "공개" : "비공개")
    })

    $('#fileinput').removeClass('form-control-file').parent().addClass('form-control px-2 pb-2')
    

    $('[for=resume-clear_id],#id_resume, #resume-clear_id').addClass('noani')

    $('#id_pic').change(function(e){
        readPic(e)
    }).siblings('label').css({'background-image': `url(${$('#pic_url').val()})`})
    $('#id_pic').parent().addClass('my-0')

    $('#id_resume').addClass('form-control mb-2')
    $('[for=resume-clear_id]').css({'background-color':'white', 'color': 'black', 'font-family':'none','font-size':'none','height':'auto'})

    $('#basic').click(function(){
        $('#id_pic').change(function(e){
            readPic(e)
        }).siblings('label').css({'background-image': "url(/media/user_icon.png/)"})
        $('#pic_default').val("true")
        console.log($('#pic_default').val())
    })
    
    $('#update').click(function(){
        var updatefrm = document.forms['updatefrm']
        var reg_pass = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
        var check_cnt = $('input[name=language]:checkbox:checked').length;
        var password = $('#id_password').val();
        var check = "update";

        let first = null;
        let target = "";

        target = "#id_password"
        if(password != ""){
            $.ajax({
                url: checkPassword_url,
                type:"POST",
                data : {'csrfmiddlewaretoken': $('#csrf_token').val(),'password':password,'check':check},
                datatype:'json',
                async: false,
                success:function(response){
                    if(response.data == "fail"){
                        //updatefrm['password'].focus();
                        $(target).siblings('label').addClass('wrongLabel')
                        $('#check_password').html('<p style="color:red">현재 사용중인 비밀번호입니다</p>');
                        first = first?first:target;
                        console.log(first)
                        //return false;
                    }else if(!reg_pass.test(updatefrm['password'].value.trim())){
                        //updatefrm['password'].focus();
                        $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
                        $('#check_password').html('<p style="color:red">유효한 비밀번호가 아닙니다</p>');
                        //return false;
                        first = first?first:target;
                        
                    } else{
                        $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
                    }
                }
            })
            target="#id_re_password"
            if(updatefrm['re_password'].value.trim()==""){
                //updatefrm['re_password'].focus();
            $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
            $('#check_re_password').html('<p style="color:red">비밀번호 확인을 입력해주세요</p>');
            //return false;
            first = first?first:target
        }else if(updatefrm['password'].value.trim() != updatefrm['re_password'].value.trim()){
            //updatefrm['re_password'].focus();
            $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
            $('#check_re_password').html('<p style="color:red">비밀번호가 다릅니다</p>');
            //return false;
            first = first?first:target
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        }
    }
    
        
        target = "#id_language"
        if(check_cnt<1){
            //$('#id_language').focus();
            $(target).siblings('label').addClass('wrongLabel')
            $('#check_language').html('<p style="color:red">한개 이상의 언어를 선택해주세요</p> ')
            //return false;
            first = first?first:target
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        }

        if(first){
            $(first).focus()
        }else{
            var con = confirm("수정하시겠습니까?")
            if(con){
                updatefrm.submit()
                alert("수정되었습니다")
            }
        }
    })

    $('#leave').click(function(){
        var con = confirm("정말 탈퇴하시겠습니까?")
        if(con){
            document.forms['leavefrm'].submit();
            alert("탈퇴되었습니다")
        }
    })


})

