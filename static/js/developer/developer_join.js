function readImage(input) {
    if (input.target.files && input.target.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            $("[for=id_pic]").css({'background-image': 'url('+e.target.result+')'})
        }
        reader.readAsDataURL(input.target.files[0]);
    }
}

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
})