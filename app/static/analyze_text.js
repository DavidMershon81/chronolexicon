var loading_text_fader = null;
var cutoff_date = 1000;

$(document).ready(function() {
    loading_text_fader = PulseFader('.loading_text', 500);
    toggle_loading_animation(false);
    toggle_analyzed_text_area(false);

    $("form").on("submit", send_text_to_be_analyzed);
    $("#cutoff_date_range").on("change", on_cutoff_date_range_change);

    
});

function init_tooltips()
{
    $('[data-toggle="tooltip"]').tooltip()
}

function on_cutoff_date_range_change() {
    cutoff_date = $("#cutoff_date_range").val();
    $("#cutoff_date_text").html(cutoff_date);
    color_all_dated_words();
}

function send_text_to_be_analyzed(event) {
    $("#analyzed_text_container").html("");
    toggle_loading_animation(true);
    toggle_analyzed_text_area(false);

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
    toggle_analyzed_text_area(true);
    
    if(data.error) {
        $("#error_alert").text(data.error).show();
        $("#analyzed_text_container").html("");
    }
    else {
        $("#error_alert").hide();
        $("#analyzed_text_container").html(data.analyzed_text_html);
        on_cutoff_date_range_change();
        init_tooltips();

        if($("#api_alert").length){
            $("#api_alert").text("Warning: Exceeded max M-W dictionary queries for today. Some words in your search may lack etymological data! Please try again tomorrow.").show();
        }
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

function toggle_analyzed_text_area(show) {
    if(show)
    {
        $("#analyzed_text_group").show();
    }
    else
    {
        $("#analyzed_text_group").hide();
    }
}

function color_all_dated_words() {
    $(".dated_word").each(color_dated_word_by_first_use);
}

function color_dated_word_by_first_use() {
    var first_use = $(this).attr("first_use");
    var text_color = first_use == "None" ? "violet" : (first_use > cutoff_date ? "#555555" : "orangered");
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