//Spoiler Handling
$(".spoiler-trigger").click(function() {
    $(this).parent().next().collapse('toggle');
});

//Footer only showing if scrolled down at least 95%
$(window).scroll(function() {              
    ($(document).scrollTop() + $(window).height()) / $(document).height() > 0.95 ? $('#footer').fadeIn() : $('#footer').fadeOut();
});