$(document).ready(function () {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listMonth'
        },
        themeSystem: 'jquery-ui',
        defaultView: 'agendaWeek',
        nowIndicator: true,
        navLinks: true, // can click day/week names to navigate views
        eventLimit: true, // allow "more" link when too many events
        height: $(window).height()*0.915
    });

    $(".button-collapse").sideNav();
    $('.dropdown-button').dropdown({
          inDuration: 300,
          outDuration: 225,
          constrainWidth: false, // Does not change width of dropdown to that of the activator
          hover: true, // Activate on hover
          gutter: 0, // Spacing from edge
          belowOrigin: false, // Displays dropdown below the button
          alignment: 'left', // Displays dropdown with edge aligned to the left of button
          stopPropagation: false // Stops event propagation
    });

    $("#schedule_drop").addClass("active");
    $("#schedule_bar").addClass("active");
    $("#logout_drop").addClass("active");
});