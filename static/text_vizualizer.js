$(document).ready(function() {
    //alert('jQuery is Ready to Go!');

    $(".dated_word").css("color","darkgray");

    $(".dated_word").each(function() {
        var first_use = $(this).attr("first_use");
        var cutoff_date = 1800;
        if(first_use > cutoff_date)
        {
            $(this).css("color", "violet");
        }
        //console.log(first_use);
      });
    
});