$(document).ready(function(){
    // 시작일 종료일 col-4
    $('#form_id input[type="date"]').parent().removeClass('col-6').addClass('col-4')
    // 비공개 col-4
    $('#form_id .form-check').parent().removeClass('col-6').addClass('col-4')
    // 언어 체크
    $("input[name='language']:checked").parent('label').addClass('label-color')

    // 문서 추가
    let num = 0
    $('#add_doc').click(function(){
        let newdiv = $('<div></div>').addClass('form-control mb-2').css({'width': '100%'})
        // 문서 유형 input
        newdiv.append($('<input/>', {type: 'text', name: 'doctype'+num, class: 'form-control d-inline-block', placeholder: '문서 유형'})
            .css({'width': '41%', 'padding-left':'.375rem'}));
        // 문서 파일 input
        newdiv.append($('<input/>', {type: 'file', name: 'doc'+num, class: 'form-control d-inline-block my-0'})
            .css({'width': '50%', 'margin-left': '0.5%', 'margin-right': '0.5%'}));
        // 삭제 button
        newdiv.append($('<input/>', {type: 'button', class: 'btn btn-danger col', value: '삭제'}).css({'width': '8%', 'vertical-align':'baseline'})
            .click(function(){newdiv.slideUp("fast", function(){$(this).remove()})}))
        $('#docs').append(newdiv);
        num += 1;
    })

    $('#form_id input[type="checkbox"]').change(function(){
        $(this).siblings('label').toggleClass('label-color').text($(this).siblings('label').text() == '비공개'? "공개" : "비공개")
    })

    // 프로젝트 업데이트 검증
    $('#update').click(function(){
        let ok = true;

        let target = "";

        // 언어
        target = "[name='language']"
        $(target).parent('label').removeClass('is-valid is-invalid')
        if($(target+":checked").length == 0){
            $(target).parent('label').addClass('is-invalid').focus()
            ok = false;
        }else{
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
        
        // 문서 개수
        $('#docnum').val(num);

        // 검사 완료
        ok && $('#form_id').submit()        
    })
})

