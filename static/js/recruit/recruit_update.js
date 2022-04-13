$(document).ready(function(){
    $('[for=id_ing]').addClass('position-static').removeClass('label-color').text('모집 중이 아닙니다.').parent().parent().removeClass('col-6').addClass('col-12')
    if($('#id_ing').is(':checked')){$('[for=id_ing]').text('모집 중입니다.').addClass('label-color')}
    $('#id_ing').change(function(){
        $('[for=id_ing]').toggleClass('label-color').text($('[for=id_ing]').text() == '모집 중입니다.'? "모집 중이 아닙니다." : "모집 중입니다.")
    })

    // 언어 추가
    let num = 0
    $('#add_language').click(function(){
        let newdiv = $('<div></div>').addClass('form-control mb-2').css({'width': '100%'})
        // 언어 선택
        $('#languages').append(newdiv);
        newdiv.append($(`<select id="select${num}" name="select${num}" class="form-control d-inline-block w-50"></select>`))
        // 언어 select에 넣기
        $(`#select${num}`).append($(`<option value="">모집 언어를 선택해주세요.</option>`))
        for(let language of languages){
            $(`#select${num}`).append($(`<option value="${language.id}">${language.language}</option>`))
        }
        // 인원수
        newdiv.append($('<input/>', {type: 'number', id: 'people'+num, name: 'people'+num, class: 'form-control d-inline-block', placeholder: '모집 인원 수'})
            .css({'width': '28%', 'padding-left':'.375rem', 'margin-left': '1%', 'margin-right': '1%'}));
        // 삭제 button
        newdiv.append($('<input/>', {type: 'button', class: 'btn btn-danger col', value: '삭제'}).css({'width': '20%', 'vertical-align':'baseline'})
            .click(function(){newdiv.slideUp("fast", function(){$(this).remove();$('#select'+num).remove()})}))
        num += 1;
    })

    // 모집 수정 검증
    $("#update").click(function(){
        let ok = true

        target = ""

        // 언어
        for(let i=0;i<num;i++){
            if($("#people"+i).length>0 && !$('#people'+i).val()){
                $('#people'+i).addClass('is-invalid').focus();
                console.log("======1")
                ok = false;
                console.log(ok)
            }else{ 
                $("#people"+i).removeClass('is-invalid').addClass('is-valid')
            }
            if($("#select"+i).length>0 && !$("#select"+i).val()){
                $('#select'+i).addClass('is-invalid').focus();
                console.log("======2")
                console.log($('#select'+i))
                ok = false;
            }else{
                $("#select"+i).removeClass('is-invalid').addClass('is-valid')
                console.log(ok)
            }
        }
        
        // 내용
        target = "#id_contents"
        $(target).siblings('label').removeClass('is-valid is-invalid')
        if($(target).val().trim()==""){
            $(target).addClass('is-invalid').attr({'placeholder': '모집 내용을 입력해주세요.'}).focus()
            console.log("======3")
            console.log(ok)
            ok = false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid')
            console.log(ok)
        }
        
        // 타이틀
        target = "#id_title";
        if($(target).val().trim()==""){
            $(target).removeClass('is-valid').addClass('is-invalid').attr({'placeholder': '모집 타이틀을 입력해주세요.'}).focus()
            console.log("======4")
            console.log(ok)
            ok = false;
        }else{
            $(target).removeClass('is-invalid').addClass('is-valid')
            console.log(ok)
        }
        
        // 검사 완료
        console.log(ok)
        if(ok){
            $("#language_num").val(num)
            $("#form_id").submit()
        }

    })
})