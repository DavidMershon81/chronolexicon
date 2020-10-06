$(document).ready(function() {

    $("form").on("submit", function(event) {
        $.ajax({
            data : {
                name : $("#name_input").val(),
                email : $("#email_input").val()
            },
            type : "POST",
            url : "/process_ajax_test"
        }).done(function(data) {

            if(data.error) {
                $("#error_alert").text(data.error).show();
                $("#success_alert").hide();

                $("#test_insert_here").html("Oh Snap, no processed HTML to insert!");
            }
            else {
                $("#success_alert").text("name:" + data.name + " email:" + data.email).show();
                $("#error_alert").hide();

                $("#test_insert_here").html(data.processed_html);
                
            }
        });

        event.preventDefault();
    });
});