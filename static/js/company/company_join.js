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

    // 아이디 중복검사 디자인
    $("[for=id_companyid]").before($("#duple_companyid").css({'right': 0})).addClass('align-self-center')
    $("#id_companyid").css({'padding-right': '8%'})

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

})