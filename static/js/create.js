$(document).ready(function(){
    $('form').addClass('row')
    $('.form-group').attr('class', 'form-group');
    $('input').css({'box-shadow': 'none'});
    $('label').attr('class', 'form-control text-center py-4');
    $('input[type="text"]').attr('class', 'form-control py-4');
    $('input[type="text"], textarea').attr({'placeholder': null});
    $('textarea').siblings('label').css({'height':'100%', 'padding': '8% 0 !important'})
    $('input[type="text"], textarea, input[type="date"]').siblings('label').css({'background-color':'lightcoral', 'color': 'white'});
    // 파일 업로드
    $('input[type="file"]').siblings('label').css({'background-color':'rgba(0,0,0,0)', 'border': '2px solid lightcoral', 'position': 'static', 'color': 'lightcoral',
     'padding': '10%', 'background-repeat':'no-repeat', 'background-position': 'center', 'background-size':'contain'}).removeClass('py-4')
    .hover(function(){$(this).css({'background-color': 'rgba(200,0,0,0.2)'})}, function(){$(this).css({'background-color': 'rgba(0,0,0,0)'})});

    // 날짜
    $('input[type="date"]').css({'padding': '2vh', 'display': 'none', 'border': '1px solid lightcoral'}).siblings('label').removeClass('py-4')
        .css({'position': 'static','padding':'3vh'}).parent().addClass('col-6').css({'display': 'inline-block'})

    // 비공개
    $('.form-check').css({'height': '100%'}).parent().addClass('col-6').css({'display': 'inline-block'})
    $('input[type="checkbox"]').hide().siblings('label').removeClass('py-4').addClass('labelP5').css({'height': '100%'})

    // 언어
    $("#id_language").removeClass('col-6').addClass('col-12').siblings('label').addClass('label-color py-2').removeClass('py-4').parent().find('label').css({'position':'static'})
    $("#id_language>.form-check").css({'padding': '0', 'display':'inline-block'}).addClass('col-1')

    $('input[type="text"]~label, textarea~label').click(function(){
        $(this).removeClass('nofocusLabel').addClass('focusLabel')
        $('#'+$(this).attr('for')).css({'padding-left': '16%', 'border': '1px solid salmon'})
    })
    
    $('input[type="text"], textarea').focus(function(){
        label = $('label[for="'+ $(this).attr('id') +'"]')
        label.removeClass('nofocusLabel').removeClass('okLabel').addClass('focusLabel')
        $(this).css({'padding-left': '16%', 'border': '1px solid salmon'})
    })
    $('input[type="text"], textarea').focusout(function(){
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
    $('input[type="date"]').siblings("label").click(function(){
        $(this).siblings('input').slideToggle(300)
        $('input[type="checkbox"]').siblings('label').toggleClass('labelP10')
    })

    $('input[type="checkbox"]').change(function(){
        $(this).siblings('label').toggleClass('label-color').text($(this).siblings('label').text() == '비공개'? "공개" : "비공개")
    })

    // 언어
    $('.form-check-input').change(function(){
        $(this).parent('label').toggleClass('label-color')
    })

})