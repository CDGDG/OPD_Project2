$(document).ready(function(){
    
    $("#form_id").addClass('row border border-4 rounded p-4')
    $('#form_id input,#form_id textarea, #form_id input[type=password]').css({'box-shadow': 'none'});
    $('#form_id label').attr('class', 'form-control text-center py-4');
    $('#form_id input[type="text"], #form_id input[type=password]').not(".noani").addClass('form-control py-4');
    $('#form_id input[type="text"],#form_id textarea,  #form_id input[type=password]').not('.noani').attr({'placeholder': null});
    $('#form_id textarea').siblings('label').removeClass('py-4').css({'padding-top': '9%'});
    $('#form_id input[type="text"],#form_id textarea,#form_id input[type="date"], #form_id input[type=password], #form_id input[type=email], #form_id input[type=number], #form_id input[type=url], #form_id select, .registnumdiv, #id_resume').siblings('label').css({'background-color':'lightcoral', 'color': 'white'});

    $('[id^=check]').addClass('checkDiv')
    // 파일 업로드
    $('#form_id input[type="file"]').not('#id_resume').siblings('label').css({'background-color':'rgba(0,0,0,0)', 'border': '2px solid lightcoral', 'position': 'static', 'color': 'lightcoral',
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

    // 전화번호
    $("[for=id_resume], [for=id_tel], [for=id_phonenum], [for=id_email], [for=id_address], [for=id_people], [for=id_url], [for=id_category]").removeClass('py-4').addClass('position-static mb-1 noani').css({'height': 'auto'})
    $('[id^="id_tel"], [id^=id_phonenum]').removeClass('py-4').addClass('noani col py-1 text-center').parent(".form-group").addClass("row col-6 pe-2").css({'margin-right':0,'margin-left':0})
    $('#id_email').removeClass('py-4').addClass('noani col py-1 text-center').parent().css({'margin-bottom': 0}).parent(".form-group").addClass("row col-6 ps-2").css({'margin-right':0,'margin-left':0})
    // 개발자 전화번호
    $("[id^=id_phonenum]").parent().toggleClass('pe-2 ps-2')

    // 주소
    $("#id_address, [id^=sample6]").removeClass('py-4').addClass('noani mb-1').css({width: 'auto', 'height':'fit-content'}).parent('.form-group').addClass('col-6 row pe-2 mx-0')
    $("#sample6_postcode").css({width: '41%', 'margin-right':'1%'})
    $("#address_btn").css({width:'58%'})
    $("#sample6_address").css({width: '100%'})
    $("#sample6_detailAddress").css({width: '50%', 'margin-right': '1%'}).attr({placeholder: '상세 주소'})
    $("#sample6_extraAddress").css({width: '49%'})

    // 직원 수
    $("#id_people").removeClass('py-4').addClass('noani').css({width: '100%'}).parent('.form-group').addClass('mb-0').parent('.form-group').addClass('mb-1 mx-0 peourl')
    
    // URL
    $("#id_url").removeClass('py-4').addClass('noani').css({width: '100%'}).parent('.form-group').parent('.form-group').addClass('mb-0 mx-0 peourl')

    // 직원 수 URL 언어 row
    $("[for=id_address]").parent('.form-group').after($('<div></div>').addClass('col-6 ps-2 pe-0 peourlrow').css({'margin-bottom':'2%'}).append($('.peourl')))

    // 회사 규모
    $('[for=id_category]').parent('.form-group').parent('.form-group').addClass('col-6 ps-2 pe-0')
    $("#id_category").addClass('py-1')
    $('#id_name').parent().parent().addClass('col-6 pe-2 ps-0')

    // 주민등록번호
    $("[for=id_registnum]").addClass('noani position-static h-auto').removeClass('py-4').parent('.form-group').addClass('col-6')
    $("[id^=id_registnum]").removeClass('py-4')

    // 프로필
    $('#id_pic').addClass('form-control-file')

    // --------------이벤트-------------
    
    $('#form_id input[type="text"],#form_id textarea, #form_id input[type="password"]').siblings('label').not('.noani').click(function(){
        $(this).removeClass('nofocusLabel').addClass('focusLabel')
        $('#'+$(this).attr('for')).css({'padding-left': '16%', 'border': '1px solid salmon'})
    })
    
    $('#form_id input[type="text"], #form_id textarea, #form_id input[type="password"]').not(".noani").focus(function(){
        label = $('label[for="'+ $(this).attr('id') +'"]')
        label.removeClass('nofocusLabel').removeClass('okLabel').addClass('focusLabel')
        $(this).css({'padding-left': '16%', 'border': '1px solid salmon'})
    })
    $('#form_id input[type="text"], #form_id textarea, #form_id input[type="password"]').not('.noani').focusout(function(){
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
    $("#form_id.update input[type='text'], #form_id.update textarea, #form_id.update input[type=password]").css({'padding-left': '31%', 'border': '1px solid #ced4da'}).siblings('label').addClass('okLabel')
})