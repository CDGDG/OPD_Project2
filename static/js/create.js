$(document).ready(function(){
    
    $("#form_id").addClass('row border border-4 rounded p-4')
    $('#form_id .form-group').attr('class', 'form-group');
    $('#form_id input,#form_id textarea').css({'box-shadow': 'none'});
    $('#form_id label').attr('class', 'form-control text-center py-4');
    $('#form_id input[type="text"]').attr('class', 'form-control py-4');
    $('#form_id input[type="text"],#form_id textarea').attr({'placeholder': null});
    $('#form_id textarea').siblings('label').removeClass('py-4').css({'padding-top': '9%'});
    $('#form_id input[type="text"],#form_id textarea,#form_id input[type="date"]').siblings('label').css({'background-color':'lightcoral', 'color': 'white'});
    // 파일 업로드
    $('#form_id input[type="file"]').siblings('label').css({'background-color':'rgba(0,0,0,0)', 'border': '2px solid lightcoral', 'position': 'static', 'color': 'lightcoral',
    'padding': '10%', 'background-repeat':'no-repeat', 'background-position': 'center', 'background-size':'contain', 'height': 'auto'}).removeClass('py-4')
    .hover(function(){$(this).css({'background-color': 'rgba(200,0,0,0.2)'})}, function(){$(this).css({'background-color': 'rgba(0,0,0,0)'})});
    
    // 날짜
    $('#form_id input[type="date"]').css({'padding': '2vh', 'display': 'none', 'border': '1px solid lightcoral'}).siblings('label').removeClass('py-4')
    .css({'position': 'static','padding':'3vh', 'height':'auto'}).parent().addClass('col-6 pe-2').css({'display': 'inline-block'})
    
    // 비공개
    $('#form_id .form-check').css({'height': '100%'}).addClass('px-0').parent().addClass('col-6').css({'display': 'inline-block'})
    $('#form_id input[type="checkbox"]').hide().siblings('label').removeClass('py-4').addClass('labelP5')
    
    // 언어
    $("#form_id #id_language").removeClass('col-6').addClass('col-12').siblings('label').addClass('label-color py-2 mb-1').removeClass('py-4').parent()
    .find('label').css({'position':'static', 'height':'auto', 'font-size': '0.8vw'})
    $("#form_id #id_language>.form-check").css({'padding': '0', 'display':'inline-block'}).addClass('col-1')
    
    $('#form_id input[type="text"]~label, textarea~label').click(function(){
        $(this).removeClass('nofocusLabel').addClass('focusLabel')
        $('#'+$(this).attr('for')).css({'padding-left': '16%', 'border': '1px solid salmon'})
    })
    
    $('#form_id input[type="text"], textarea').focus(function(){
        label = $('label[for="'+ $(this).attr('id') +'"]')
        label.removeClass('nofocusLabel').removeClass('okLabel').addClass('focusLabel')
        $(this).css({'padding-left': '16%', 'border': '1px solid salmon'})
    })
    $('#form_id input[type="text"], textarea').focusout(function(){
        label = $('label[for="'+ $(this).attr('id') +'"]')
        label.removeClass('focusLabel').removeClass('nofocusLabel').removeClass('okLabel')
        if($(this).val().trim()==""){
            label.addClass("nofocusLabel")
            $(this).css({'padding-left': '0', 'border': '1px solid #ced4da'})
        }else{
            label.addClass('okLabel')
            $(this).css({'padding-left': '31%', 'border': '1px solid #ced4da'})
        }
    })
    
    // 날짜
    $('#form_id input[type="date"]').siblings("label").click(function(){
        $(this).siblings('input').slideToggle(300)
        $('#form_id input[type="checkbox"]').siblings('label')
        // .toggleClass('labelP10')
    })
    
    // 언어
    $('#form_id .form-check-input').change(function(){
        $(this).parent('label').toggleClass('label-color')
    })
    

    // 업데이트 설정
    $("#form_id.update input[type='text'], #form_id.update textarea").css({'padding-left': '31%', 'border': '1px solid #ced4da'}).siblings('label').addClass('okLabel')
})