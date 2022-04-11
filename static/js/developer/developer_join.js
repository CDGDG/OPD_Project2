function readImage(input) {
    if (input.target.files && input.target.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            $("[for=id_pic]").css({'background-image': 'url('+e.target.result+')'})
        }
        reader.readAsDataURL(input.target.files[0]);
    }
}
//enter -> submit 방지
document.addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
    event.preventDefault();
    };
}, true);

$(document).ready(function(){
    // 프로필 미리보기 띄우기
    $('#id_pic').change(function (e) {
        readImage(e)
    })
    // 아이디 중복검사 디자인
    $("[for=id_userid]").before($("#duple_userid").css({'right': 0})).addClass('align-self-center')
    $("#id_userid").css({'padding-right': '8%'})

    // 닉네임 중복검사 디자인
    $("[for=id_nickname]").before($("#duple_nickname").css({'right': 0})).addClass('align-self-center')
    $("#id_nickname").css({'padding-right': '8%'})

    // 주민등록번호 디자인
    $("[id^=id_registnum]").focus(function(){$('.registnumdiv').css({border: '1px solid lightcoral'})}).focusout(function(){$('.registnumdiv').css({border: '1px solid #ced4da'})})

    // 프로필 디자인
    $("[for=id_pic]").addClass('h-100').css({'padding': '50.5% 0'}).parent().addClass('col-3').after($('<div></div>').addClass('col-9 px-0 ps-2 mb-4').append($("#id_userid, #id_password, #id_re_password, #id_nickname").parent()))
    $("#id_nickname").parent().addClass('mb-0')

    // 값 변경시 다시 유효성 검사
    $('#id_userid').change(function(){ 
        id_button = false;
        $("#duple_userid").removeClass('btn-success btn-danger').addClass('btn-secondary').attr({'data-bs-original-title': '중복검사를 해주세요.'}).tooltip("show");
    })
    $('#id_nickname').change(function(){
        nick_button = false;
        $("#duple_nickname").removeClass('btn-success btn-danger').addClass('btn-secondary').attr({'data-bs-original-title': '중복검사를 해주세요.'}).tooltip("show");
    })
    $('#email_id').change(function(){
        send_email = false;
    })
    $('#email_option').change(function(){
        send_email = false;
    })


    $('#email_select').change(function(){
        $("#email_option").val($('#email_select').val());
    })

    id_button = false; 
    nick_button = false;
    send_email = false;

    // 아이디 중복검사
    $('#duple_userid').tooltip({trigger: 'focus'}).click(function(){
        var userid=$('#id_userid').val()
        $.ajax({
            url: check_id_url,
            data: {'userid': userid},
            datatype:'json',
    
            success : function(response){
                if(response.blank){
                    //$('#dupleId_result').html('<p>아이디를 입력해주세요</p>')
                    id_button = false;
                }else{
                    if(response.data == 'not exist'){
                        //$('#dupleId_result').html('<p style="color:green">사용가능한 아이디입니다</p>')
                        $("#duple_userid").removeClass('btn-secondary btn-danger').addClass('btn-success').attr({'data-bs-original-title': '사용 가능한 아이디입니다.'}).tooltip("show");
                        id_button = true
                        return;
                    }else{
                        //$('#dupleId_result').html('<p style="color:red">중복된 아이디입니다</p>')
                        $("#duple_userid").removeClass('btn-secondary btn-success').addClass('btn-danger').attr({'data-bs-original-title': '중복된 아이디입니다.'}).tooltip("show");
                        id_button = false
                        return;
                        
                    }
                    
                }
                
            }
            
        })
    })

    //닉네임 중복검사
    $('#duple_nickname').tooltip({trigger: 'focus'}).click(function(){
        var nickname=$('#id_nickname').val()
        $.ajax({
            url:check_nick_url,
            data:{'nickname':nickname},
            datatype:'json',
            
            success : function(response){
                if(response.blank){
                    //$('#dupleNick_result').html('<p>닉네임을 입력해주세요</p>')
                    nick_button = false;
                }else{
                    if(response.data == 'not exist'){
                        //$('#dupleNick_result').html('<p style="color:green">사용가능한 닉네임입니다</p>')
                        $("#duple_nickname").removeClass('btn-secondary btn-danger').addClass('btn-success').attr({'data-bs-original-title': '사용 가능한 닉네임입니다.'}).tooltip("show");
                        nick_button=true;
                        return;
                    }else{
                        //$('#dupleNick_result').html('<p style="color:red">중복된 닉네임입니다</p>')
                        $("#duple_nickname").removeClass('btn-secondary btn-success').addClass('btn-danger').attr({'data-bs-original-title': '중복된 아이디입니다.'}).tooltip("show");
                        return;
                        
                    }
                    
                }
                
            }
        })
    })

    //이메일 인증
    $('#send_email').click(function(){
        var joinfrm = document.forms['joinfrm']
        var email = joinfrm['email'].value.trim()
        
        //이메일 인증번호
        var num_list = []
        for(var i=0;i<4;i++){num_list.push(Math.floor(Math.random() * 10)+"")}
        var emailnum = num_list.join("")
        
        $.ajax({
            url:send_email_url,
            data : {'email':email,'emailnum':emailnum},
            datatype:'json',
            success:function(response){
                if(response.fail){
                    $('#check_email').html('<p style="color:red">이메일 인증에 실패 했습니다 다시 시도해주세요</p>')
                }
                if(response.blank){
                    $('#check_email').html('<p style="color:red">이메일을 입력해주세요</p>')
                }else{
                    $('#check_email').html('<p style="color:green">인증번호를 입력해주세요</p>')
                    $('#emailnum').css('display','block') 
                    $('#check_emailnum').css('display','block') //이메일 인증번호 입력란
                    $('#check_emailnum').click(function(){
                        $('#send_email').attr('value','다시 인증하기')
                        if(joinfrm['emailnum'].value.trim() == ""){
                            $('#check_email_result').html('<p style="color:red">인증번호를 입력해주세요</p>')
                            
                        }else if(joinfrm['emailnum'].value.trim() != emailnum){
                            $('#check_email_result').html('<p style="color:red">인증번호를 다시 확인해주세요</p>') //인증번호가 맞지 않을 때
                            
                        }else{
                            $('#check_email_result').html('<p style="color:green">인증되었습니다</p>')
                            send_email=true;
                            
                        }
                    })
                }
            }
        })
    })












    // 회원가입 유효성 검사
    $('#join').click(function(){
        var joinfrm = document.forms['joinfrm']
		var reg_pass = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
		var reg_id = /^[a-z]+[a-z0-9]{5,19}$/g; 
        var check_cnt = $('input[name=language]:checkbox:checked').length;
        

        let first = null;
        let target = "";

        

        
        // 아이디
        target="#id_userid"
        if(joinfrm['userid'].value.trim()==""){
            // joinfrm['userid'].focus();
            $(target).siblings('label').addClass('wrongLabel')
            $('#check_userid').html('<p style="color:red">아이디를 입력해주세요</p>');
            // return false;
            first = first?first:target
        }
        else if(!reg_id.test(joinfrm['userid'].value.trim())){
            // joinfrm['userid'].focus();
            $(target).siblings('label').addClass('wrongLabel')
            $('#check_userid').html('<p style="color:red">유효한 아이디가 아닙니다</p>');
            first = first?first:target
            // return false;
        }
        else if(!id_button){
            // joinfrm['userid'].focus();
            $(target).siblings('label').addClass('wrongLabel')
            $('#check_userid').html('<p style="color:red">아이디 중복검사를 해주세요</p>');
            first = first?first:target
            // return false;
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_userid').html('');
        }

        // 비밀번호
        target="#id_password"
        if(joinfrm['password'].value.trim()==""){
            // joinfrm['password'].focus();
            $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_password').html('<p style="color:red">비밀번호를 입력해주세요</p>');
            // return false;
        }
        else if(!reg_pass.test(joinfrm['password'].value.trim())){
            // joinfrm['password'].focus();
            $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_password').html('<p style="color:red">유효한 비밀번호가 아닙니다</p>');
            // return false;
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        }

        target = "#id_re_password"
        if(joinfrm['password'].value.trim()=="" || joinfrm['password'].value.trim() != joinfrm['re_password'].value.trim()){
            // joinfrm['re_password'].focus();
            $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_re_password').html('<p style="color:red">비밀번호가 다릅니다</p>');
            // return false;
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        }
        
        // 닉네임
        target = "#id_nickname"
        if(joinfrm['nickname'].value.trim()==""){
            // joinfrm['nickname'].focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_nickname').html('<p style="color:red">닉네임을 입력해주세요</p>');
            // return false;
        }
        else if(joinfrm['nickname'].value.trim().length < 3){
            // joinfrm['nickname'].focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_nickname').html('<p style="color:red">닉네임을 세자리 이상입력해주세요</p>');
            // return false;

        }
        else if(!nick_button){
            // joinfrm['nickname'].focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_nickname').html('<p style="color:red">닉네임 중복검사를 해주세요</p>');
            // return false;
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        }

        //주민등록번호
        target = "#id_registnum"
        if($('#id_registnum1').val() == "" || $('#id_registnum2').val() == ""){
            // $('#id_registnum1').focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_registnum').html('<p style="color:red">주민등록번호를 모두 입력해주세요</p>');
            // return false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            joinfrm['registnum'].value= $('#id_registnum1').val()+$('#id_registnum2').val();
        }

        // 전화번호
        target = "#id_phonenum"
        if($('#id_phonenum1').val() == "" || $('#id_phonenum2').val() == "" || $('#id_phonenum3').val() == ""){
            // $('#id_phonenum1').focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_phonenum').html('<p style="color:red">휴대폰번호를 모두 입력해주세요</p>');
            // return false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            joinfrm['phonenum'].value = $('#id_phonenum1').val()+"-"+$('#id_phonenum2').val()+"-"+$('#id_phonenum3').val();
        }
        
        // 이메일
        target = "#email"
        if($('#email').val() == "" ){
            // $('#email_id').focus();
            $('#check_email').html('<p style="color:red">이메일을 입력해주세요</p>');
            // return false;
        }


        if(!send_email){
            // joinfrm['send_email'].focus();
            $('#check_email_option').html('<p style="color:red">이메일 인증을 해주세요</p>');
            // return false;
        }
        
        // 언어
        target = "#id_language"
        if(check_cnt<1){
            // $('#check_language').focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_language').html('<p style="color:red">한개 이상의 언어를 선택해주세요 ')
            // return false;
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        }
       
        // console.log(check_cnt)

        // console.log(joinfrm['phonenum'].value);
        // console.log(joinfrm['registnum'].value);
        if(first){
            $(first).focus()
        }else{
            joinfrm.submit();
            alert("회원가입되었습니다. 감사합니다~")
        }
    })
})