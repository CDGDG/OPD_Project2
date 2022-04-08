function readImage(input) {
    if (input.target.files && input.target.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            $('input[type="file"]').siblings('label').css({'background-image': 'url('+e.target.result+')'})
        }
        reader.readAsDataURL(input.target.files[0]);
    }
}
// 이벤트 리스너
$(document).ready(function () {
    // 썸네일 미리보기 띄우기
    $('#id_thumbnail').change(function (e) {
        readImage(e)
    })

    $('#form_id input[type="checkbox"]').change(function(){
        $(this).siblings('label').toggleClass('label-color').text($(this).siblings('label').text() == '비공개'? "공개" : "비공개")
    })

    // 프로젝트 생성 검증
    $("#create").click(function(){
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

        // 내용
        target = "#id_contents"
        if($(target).val().trim()==""){
            $(target).removeClass('is-valid').addClass('is-invalid').attr({'placeholder': '프로젝트 내용을 입력해주세요.'}).focus()
            ok = false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid')
        }
        
        // 요약
        target = "#id_summary"
        if($(target).val().trim()==""){
            $(target).removeClass('is-valid').addClass('is-invalid').attr({'placeholder': '프로젝트 요약을 입력해주세요.'}).focus()
            ok = false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid')
        }
        
        // 타이틀
        target = "#id_title";
        if($(target).val().trim()==""){
            $(target).removeClass('is-valid').addClass('is-invalid').attr({'placeholder': '프로젝트 타이틀을 입력해주세요.'}).focus()
            ok = false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid')
        }

        // 검사 완료
        ok && $('#form_id').submit()
    })
})