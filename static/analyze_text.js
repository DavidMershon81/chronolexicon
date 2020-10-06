var loading_text_fader = null;
var cutoff_date = 1000;

$(document).ready(function() {
    loading_text_fader = PulseFader('.loading_text', 500);
    toggle_loading_animation(false);

    $("form").on("submit", send_text_to_be_analyzed);

    $("#cutoff_date_range").on("change", function() {
        cutoff_date = $("#cutoff_date_range").val();
        $("#cutoff_date_range_label").html("Cutoff Date: " + cutoff_date);
        color_all_dated_words();
    });
});

function send_text_to_be_analyzed(event) {
    $("#analyzed_text_container").html("");
    toggle_loading_animation(true);

    $.ajax({
        data : {
            analysis_text : $("#analysis_text").val(),
        },
        type : "POST",
        url : "/analyze_text_first_use"
    }).done(on_recieve_text_analysis);

    event.preventDefault();
}

function on_recieve_text_analysis(data)
{
    toggle_loading_animation(false);
    if(data.error) {
        $("#error_alert").text(data.error).show();
        $("#analyzed_text_container").html("");
    }
    else {
        $("#error_alert").hide();
        $("#analyzed_text_container").html(data.analyzed_text_html);
        color_all_dated_words();
    }   
}

function toggle_loading_animation(show) {
    if(show)
    {
        $("#loading_text_group").show();
        loading_text_fader.start_pulse();
    }
    else
    {
        $("#loading_text_group").hide();
        loading_text_fader.stop_pulse();
    }
}

function color_all_dated_words() {
    $(".dated_word").each(color_dated_word_by_first_use);
}

function color_dated_word_by_first_use() {
    var first_use = $(this).attr("first_use");
    var text_color = first_use > cutoff_date ? "violet" : "darkgray";
    $(this).css("color", text_color);
}

var PulseFader = function(target, pulse_speed) {
    var obj =  {
        loop_id: null,
        fade_in: true,
        pulse_loop: function() {
            if(obj.fade_in)
                $(target).fadeIn(pulse_speed);
            else
                $(target).fadeOut(pulse_speed);

            obj.fade_in = !obj.fade_in;
        },
        start_pulse: function() {
            if(obj.loop_id != null)
                obj.stop_pulse();
            obj.loop_id = window.setInterval(obj.pulse_loop, pulse_speed);
            obj.pulse_loop();        
        },
        stop_pulse: function() {
            window.clearInterval(obj.loop_id);
            $(target).fadeIn(0);
        }
    };
    return obj;
}