$(document).ready(function(){
    $('.detailDiv').removeClass('col-6').addClass('col-12').css({backgroundColor:'lightcoral'});
    $('.title').css({'font-family': 'Dongle', color:'white', 'font-size': '3vw'});
    $('.detailDiv label').not(".no").addClass('rounded p-1 mb-3').css({'font-family': 'Noto Sans KR, sans-serif', 'color':'white', 'background-color': 'lightcoral'});
})
$(function() {
    $('textarea.contents').each(function() {
        $(this).height($(this).prop('scrollHeight'));
    });
});