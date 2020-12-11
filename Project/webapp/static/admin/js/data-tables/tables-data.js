//------------- tables-data.js -------------//
$(document).ready(function () {


    //------------- Data tables -------------//
    //basic datatables
    $('#basic-datatables').dataTable({
        "oLanguage": {
            "sSearch": "<span style='margin-right:5px '> Search</span>",
            "sLengthMenu": "<span>_MENU_</span>",
            'sLengthSelect' : null ,
            "scrollCollapse": true,

        },
        "sDom": "<'row'<'col-md-6 col-xs-12 'l><'col-md-6 col-xs-12'f>r>t<'row'<'col-md-4 col-xs-12'i><'col-md-8 col-xs-12'p>>"
    });

});