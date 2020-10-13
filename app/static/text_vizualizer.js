$(document).ready(function() {
    //alert('jQuery is Ready to Go!');

    $(".dated_word").each(function() {
        var first_use = $(this).attr("first_use");
        var cutoff_date = 1800;
        var text_color = first_use > cutoff_date ? "violet" : "darkgray";
        $(this).css("color", text_color);
    });
    
});