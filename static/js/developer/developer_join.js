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


    // 회원가입 유효성 검사
    $('#join').click(function(){
        var joinfrm = document.forms['joinfrm']
		var reg_pass = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
		var reg_id = /^[a-z]+[a-z0-9]{5,19}$/g; 
        var check_cnt = $('input[name=language]:checkbox:checked').length;

        let first = null;
        let target = "";
        
        // 아이디
        target='userid'
        if(joinfrm['userid'].value.trim()==""){
            // joinfrm['userid'].focus();
            $('#check_userid').html('<p style="color:red">아이디를 입력해주세요</p>');
            // return false;
            first = first?first:target
        }
        
        if(!reg_id.test(joinfrm['userid'].value.trim())){
            // joinfrm['userid'].focus();
            $('#check_userid').html('<p style="color:red">유효한 아이디가 아닙니다</p>');
            first = first?first:target
            // return false;
        }
        if(!id_button){
            // joinfrm['userid'].focus();
            $('#check_userid').html('<p style="color:red">아이디 중복검사를 해주세요</p>');
            first = first?first:target
            // return false;
        }
        // 비밀번호
        if(joinfrm['password'].value.trim()==""){
            joinfrm['password'].focus();
            $('#check_password').html('<p style="color:red">비밀번호를 입력해주세요</p>');
            return false;
            
        }
        
        if(!reg_pass.test(joinfrm['password'].value.trim())){
            joinfrm['password'].focus();
            $('#check_password').html('<p style="color:red">유효한 비밀번호가 아닙니다</p>');
            return false;
        }
        
        if(joinfrm['password'].value.trim() != joinfrm['re_password'].value.trim()){
            joinfrm['re_password'].focus();
            $('#check_re_password').html('<p style="color:red">비밀번호가 다릅니다</p>');
            return false;
        }
        
        if(joinfrm['nickname'].value.trim()==""){
            joinfrm['nickname'].focus();
            $('#check_nickname').html('<p style="color:red">닉네임을 입력해주세요</p>');
            return false;
        }
        
        if(joinfrm['nickname'].value.trim().length < 3){
            joinfrm['nickname'].focus();
            $('#check_nickname').html('<p style="color:red">닉네임을 세자리 이상입력해주세요</p>');
            return false;

        }

        if(!nick_button){
            joinfrm['nickname'].focus();
            $('#check_nickname').html('<p style="color:red">닉네임 중복검사를 해주세요</p>');
            return false;
            
        }
        if($('#id_registnum1').val() == "" || $('#id_registnum2').val() == ""){
            $('#id_registnum1').focus();
            $('#check_registnum').html('<p style="color:red">주민등록번호를 모두 입력해주세요</p>');
            return false;
        }else{
            joinfrm['registnum'].value= $('#id_registnum1').val()+$('#id_registnum2').val();
        }


        if($('#id_phonenum1').val() == "" || $('#id_phonenum2').val() == "" || $('#id_phonenum3').val() == ""){
            $('#id_phonenum1').focus();
            $('#check_phonenum').html('<p style="color:red">휴대폰번호를 모두 입력해주세요</p>');
            return false;
            
        }else{
            joinfrm['phonenum'].value = $('#id_phonenum1').val()+"-"+$('#id_phonenum2').val()+"-"+$('#id_phonenum3').val();
        }
        
        if($('#email_id').val() == "" || $('#email_option').val() == ""){
            $('#email_id').focus();
            $('#check_email_id').html('<p style="color:red">이메일을 모두 입력해주세요</p>');
            return false;

        }

        if(!send_email){
            joinfrm['send_email'].focus();
            $('#check_email_option').html('<p style="color:red">이메일 인증을 해주세요</p>');
            return false;
        }
        
        if(check_cnt<1){
            $('#check_language').focus();
            $('#check_language').html('<p style="color:red">한개 이상의 언어를 선택해주세요 ')
            return false;
        }
       
        console.log(check_cnt)

        console.log(joinfrm['phonenum'].value);
        console.log(joinfrm['registnum'].value);
        // joinfrm.submit();
    })
})