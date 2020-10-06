$(document).ready(function() {

    $("form").on("submit", function(event) {
        $.ajax({
            data : {
                analysis_text : $("#analysis_text").val(),
            },
            type : "POST",
            url : "/analyze_text_first_use"
        }).done(on_recieve_text_analysis);

        event.preventDefault();
    });
});

function on_recieve_text_analysis(data)
{
    if(data.error) {
        $("#error_alert").text(data.error).show();
        $("#success_alert").hide();
        $("#test_insert_here").html("Oh Snap, no processed HTML to insert!");
    }
    else {
        $("#success_alert").text("success! processed the text!").show();
        $("#error_alert").hide();
        $("#test_insert_here").html(data.analyzed_text_html);
        $(".dated_word").each(color_text_by_first_use);   
    }   
}

function color_text_by_first_use()
{
    var first_use = $(this).attr("first_use");
    var cutoff_date = 1800;
    var text_color = first_use > cutoff_date ? "violet" : "darkgray";
    $(this).css("color", text_color);
}