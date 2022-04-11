function readImage(input) {
    if (input.target.files && input.target.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            $('input[type="file"]').siblings('label').css({'background-image': 'url('+e.target.result+')'})
        }
        reader.readAsDataURL(input.target.files[0]);
    }
}

$(document).ready(function(){
    $(".form-group").children('.form-group').addClass('mb-0')


    // 회사 사진 미리보기 띄우기
    $('#id_pic').change(function (e) {
        readImage(e)
    })

    $("#submitbtn").click(function(){
        let ok = true;

        let target = "";

        // 언어
        target = "[name='language']"
        if($(target+":checked").length == 0){
            $(target).parent('label').removeClass('is-valid').addClass('is-invalid').focus()
            ok = false;
        }else{
            $(target).parent('label').removeClass('is-invalid')
            $(target+":checked").parent('label').addClass('is-valid')
        }

    })


    // 정보 수정 유효성 검사
    $('#updatebtn').click(function(){
        var updatefrm = document.forms['updateForm']
		
        var reg_url = /(http(s)?:\/\/)([a-z0-9\w]+\.*)+[a-z0-9]{2,4}/gi
        var check_cnt = $('input[name=language]:checkbox:checked').length;

        let first = null;
        let target = "";

        // 비밀번호
        // target="#id_password"
        // if(joinfrm['id_password'].value.trim()==""){
        //     // joinfrm['password'].focus();
        //     $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
        //     first = first?first:target
        //     $('#check_password').html('<p style="color:red">비밀번호를 입력해주세요</p>');
        //     // return false;
        // }
        // else if(!reg_pass.test(joinfrm['id_password'].value.trim())){
        //     // joinfrm['password'].focus();
        //     $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
        //     first = first?first:target
        //     $('#check_password').html('<p style="color:red">유효한 비밀번호가 아닙니다</p>');
        //     // return false;
        // }
        // else{
        //     $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        //     $('#check_password').html('');
        // }

        // target = "#id_re_password"
        // if(joinfrm['id_password'].value.trim()=="" || joinfrm['id_password'].value.trim() != joinfrm['id_re_password'].value.trim()){
        //     // joinfrm['re_password'].focus();
        //     $(target).addClass('is-invalid').siblings('label').addClass('wrongLabel')
        //     first = first?first:target
        //     $('#check_re_password').html('<p style="color:red">비밀번호가 다릅니다</p>');
        //     // return false;
        // }
        // else{
        //     $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
        //     $('#check_re_password').html('');
        // }
        
        // 회사이름
        target = "#id_name"
        if(updatefrm['id_name'].value.trim()==""){
            // updatefrm['nickname'].focus();
            $(target).closest('div').siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_name').html('<p style="color:red">회사 이름을 입력해주세요</p>');
            // return false;
        }
        else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_name').html('');
        }

        // 전화번호
        target = "#id_tel"
        if($('#id_tel1').val() == "" || $('#id_tel2').val() == "" || $('#id_tel3').val() == ""){
            // $('#id_tel1').focus();
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_tel').html('<p style="color:red">휴대폰번호를 모두 입력해주세요</p>');
            // return false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_tel').html('')
            updatefrm['tel'].value = $('#id_tel1').val()+"-"+$('#id_tel2').val()+"-"+$('#id_tel3').val();
        }

        // 회사소개
        target = "#id_summary"
        if($(target).val() == ''){
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_summary').html('<p style="color:red">소개를 입력해주세요</p>');
        }else {
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_summary').html('')
        }

        // 직원 수
        target = "#id_people"
        if($(target).val() == ''){
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_people').html('<p style="color:red">직원수를 입력해주세요</p>')
        }else {
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_people').html('')
        }

        // 주소
        target = "#sample6_address"
        if(($.trim($('#sample6_address').val())) == "" || ($.trim($('#sample6_detailAddress').val())) == ""){
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_address').html('<p style="color:red">주소를 입력해주세요</p>')
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_address').html('')
            updatefrm['address'].value += " "+$('#sample6_detailAddress').val()
        }

        // URL 
        target = "#id_url"
        if($.trim($(target).val()) == ''){
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_url').html('<p style="color:red">URL을 입력해주세요</p>')
        }else if(!reg_url.test($.trim($(target).val()))){
            $(target).siblings('label').addClass('wrongLabel')
            first = first?first:target
            $('#check_url').html('<p style="color:red">URL형식이 아닙니다</p>')
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid').siblings('label').removeClass('wrongLabel')
            $('#check_url').html('')
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

        if(first){
            $(first).focus()
        }else{
            updatefrm.submit();
            alert("회원가입되었습니다. 감사합니다~")
        }
    })
})