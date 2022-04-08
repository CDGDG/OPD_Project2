$(document).ready(function(){
    $('[for=id_ing]').addClass('position-static').removeClass('label-color').text('모집 중이 아닙니다.').parent().parent().removeClass('col-6').addClass('col-12')
    if($('#id_ing').is(':checked')){$('[for=id_ing]').text('모집 중입니다.').addClass('label-color')}
    $('#id_ing').change(function(){
        $('[for=id_ing]').toggleClass('label-color').text($('[for=id_ing]').text() == '모집 중입니다.'? "모집 중이 아닙니다." : "모집 중입니다.")
    })

    // 모집 수정 검증
    $("#update").click(function(){
        let ok = true;

        let target = "";

        // 내용
        target = "#id_contents"
        $(target).siblings('label').removeClass('is-valid is-invalid')
        if($(target).val().trim()==""){
            $(target).addClass('is-invalid').attr({'placeholder': '모집 내용을 입력해주세요.'}).focus()
            ok = false;
        }else{
            $(target).addClass('is-valid')
        }

        // 타이틀
        target = "#id_title";
        if($(target).val().trim()==""){
            $(target).removeClass('is-valid').addClass('is-invalid').attr({'placeholder': '모집 타이틀을 입력해주세요.'}).focus()
            ok = false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid')
        }

        // 검사 완료
        ok && $("#form_id").submit()

    })
})