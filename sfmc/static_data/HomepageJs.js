$(document).ready(function(){
    $('.ui.pointing.dropdown.link.item')
    .dropdown();

    $('.ui.modal')
    .modal('show');
    
    

    $("#icon_bars_fm").click(function(){

        $('.ui.sidebar')
        .sidebar('setting', 'transition', 'overlay')
        .sidebar('toggle');

    });

    $(".ui.right.sidebar.inverted.vertical.menu .item")
    .click(function(){
        $('.ui.sidebar')
        .sidebar('hide');
    });


    $("#close_modal").click(function(){

        $('.ui.modal')
        .modal('hide');

    });


    $("#a7").click(function(){
        $('.ui.right.pointing.dropdown.link.item')
        .dropdown();
    });


});