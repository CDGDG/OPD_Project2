$( document ).ready(function() {
    $("#menu").val(selected_menu).prop("selected", true);
});

function search(){
    var searchtxt = document.getElementById('searchtxt')
    var menu = document.getElementById('menu')
    console.log(menu.options[menu.selectedIndex].value);
    console.log(searchtxt.value)
    location.href=list_url+"?s="+searchtxt.value+"&m="+menu.options[menu.selectedIndex].value
}