$( document ).ready(function() {
    $("#menu").val("{{ menu }}").prop("selected", true);
});

function search(){
    var searchtxt = document.getElementById('searchtxt')
    var menu = document.getElementById('menu')
    console.log(menu.options[menu.selectedIndex].value);
    console.log(searchtxt.value)
    location.href="{% url 'Developer:list' %}?s="+searchtxt.value+"&m="+menu.options[menu.selectedIndex].value
}