//Some global Variables to process data

//The current calendar event being manipulated
var currentCalEvent = null;

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
				editable: true,
				eventLimit: true, // allow "more" link when too many events
                height: $(window).height()*0.915,
                selectable: true,
                selectHelper: true,

                //Click on Existing Event
                eventClick: function(calEvent, jsEvent, view)
                {
                    ClearPopupFormValues();
                    $('#eventModal').modal('open');
                    $('#event-form').attr('action', 'javascript:updateEvent()');
                    $("#eventTitle").val(calEvent.title);
                    $('#deleteEvent').removeClass("disabled");
                    $("#eventStartDate").val(calEvent.start.format('YYYY-MM-DD'));
                    $("#eventStartTime").val(calEvent.start.format('HH:mm:ss'));
                    $('#eventEndDate').val(calEvent.end.format('YYYY-MM-DD'));
                    $('#eventEndTime').val(calEvent.end.format('HH:mm:ss'));
                    console.log(calEvent.group_id);
                    $('#sched-groups').val(calEvent.group_id);
                    $('select').material_select();

                    currentCalEvent = calEvent
                    //var startTime = $.fullCalendar.moment(calEvent.start);
                    //alert('Event: ' + calEvent.title);
                    //alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
                    //alert('View: ' + view.name);

                    // change the border color just for fun
                    //$(this).css('border-color', 'red');

                },

                //Create New Event
                select: function (start, end)
                {
                    ClearPopupFormValues();
                    $('#event-form').attr('action', 'javascript:submitEvent()');

                    $('#eventModal').modal('open');
                    $("#eventTitle").val('');
                    $('#deleteEvent').addClass("disabled");
                    $("#eventStartDate").val(start.format('YYYY-MM-DD'));
                    $("#eventStartTime").val(start.format('HH:mm:ss'));
                    $('#eventEndDate').val(end.format('YYYY-MM-DD'));
                    $('#eventEndTime').val(end.format('HH:mm:ss'))

                    //var title = prompt("Enter event title")
				    // var eventData;
				    // if (title)
                    // {
                    //
                    // //event data produced here should be stored in database
					//     eventData = {
					// 	    title: title,
					// 	    start: start,
					// 	    end: end
					//         };
                    //
					// $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
				    // }
                    //
                },

                //Move an Event Around
                eventDrop: function (event, delta, revertFunc, jsEvent, ui, view)
                {
                    if (confirm("Confirm move?")) {
                        //UpdateEvent(event.id, event.start);
                    }
                    else {
                        revertFunc();
                    }
                },

                //Resive an event
                eventResize: function (event, delta, revertFunc, jsEvent, ui, view)
                {
                    if (confirm("Confirm change event length?"))
                    {
                        //UpdateEvent(event.id, event.start, event.end);
                    }
                    else {
                        revertFunc();
                    }
                },

                events: '/getCampEvents'
		});

        // Resize calendar perfectly
        if(calendar)
        {
          $(window).resize(function() {
            var calHeight = $(window).height()*0.915;
            $('#calendar').fullCalendar('option', 'height', calHeight);
          });
        }

        // Enable material select tags and modal tags
        $('select').material_select();
        $('.modal').modal();
        $('.trigger-modal').modal();
        $(".button-collapse").sideNav();
        $('.dropdown-button').dropdown({
              inDuration: 300,
              outDuration: 225,
              constrainWidth: true, // Does not change width of dropdown to that of the activator
              hover: true, // Activate on hover
              gutter: 0, // Spacing from edge
              belowOrigin: true, // Displays dropdown below the button
              alignment: 'left', // Displays dropdown with edge aligned to the left of button
              stopPropagation: false // Stops event propagation
        });

        $("#schedule_drop").addClass("active");
        $("#schedule_bar").addClass("active");

        //attach some functions
        $('#deleteEvent').click(deleteEvent);

        // Attach a run setup on each group
        var groups = $("#groups")[0];
        for (var i=0; i<groups.childElementCount; i++)
        {
          	if (groups.children[i].classList.contains("group"))
            {
          		var group = groups.children[i];
        		setup(group);
        	}
        }
});

// Attach an onclick function to all groups
var setup = function(group)
{
	group.onclick = function()
    {
        var groups = $("#groups")[0];
        var isHighlighted = 0;
        for (var i=0; i<groups.childElementCount; i++)
        {

          	if (groups.children[i].classList.contains("highlight-group") )
            {
                isHighlighted++
            }
            else groups.children[i].classList.add("dim-group")

        }

		console.log(group.id);

        if (group.classList.contains("highlight-group"))
        {
            group.classList.remove("highlight-group");
            group.classList.add("dim-group")
        }
        else if (group.classList.contains("dim-group"))
        {
            group.classList.add("highlight-group");
            group.classList.remove("dim-group")
        }
        else
        {
            group.classList.add("highlight-group")
        }
	}
};

//Update event and update the back-end when an event is moved
function deleteEvent()
{
    if (currentCalEvent === null) return;

    console.log("Updating");
    console.log(currentCalEvent);

    $('#eventModal').modal('close');

    var dataRow = {
        'title':$('#eventTitle').val(),
        'eventStartDate': $('#eventStartDate').val(),
        'eventStartTime': $('#eventStartTime').val(),
        'eventEndDate': $('#eventEndDate').val(),
        'eventEndTime': $('#eventEndTime').val(),
        'group_id': $('#sched-groups').val()
    };

    var ISOStartDate = dataRow['eventStartDate'] + 'T' + dataRow['eventStartTime'];
    var ISOEndDate = dataRow['eventEndDate'] + 'T' + dataRow['eventEndTime'];

    var eventData = {
        id: currentCalEvent['id'],
        title: dataRow['title'],
        start: ISOStartDate,
        end: ISOEndDate,
        group_id: $('#sched-groups').val()
    };

    $.ajax({
        url: "/saveEvent",
        type: "DELETE",
        contentType: "application/json",
        data: JSON.stringify(eventData),
        dataType: "json"
    })

    .done( function (response) {

        if (response)
        {
            $('#calendar').fullCalendar('refetchEvents');
            Materialize.toast('Event Was Deleted', 4000)
        }

     })

     .fail ( function() {
        Materialize.toast('Error: Check Your Internet Connection', 4000)
     })

     .always (function() {

        $('#calendar').fullCalendar('unselect');
     })

    currentCalEvent = null
}

function updateEvent()
{
    if (currentCalEvent === null) return;
    console.log("Updating");
    console.log(currentCalEvent);

    $('#eventModal').modal('close');

    var dataRow = {
        'title':$('#eventTitle').val(),
        'eventStartDate': $('#eventStartDate').val(),
        'eventStartTime': $('#eventStartTime').val(),
        'eventEndDate': $('#eventEndDate').val(),
        'eventEndTime': $('#eventEndTime').val(),
        'group_id': $('#sched-groups').val()
    };


    var ISOStartDate = dataRow['eventStartDate'] + 'T' + dataRow['eventStartTime'];
    var ISOEndDate = dataRow['eventEndDate'] + 'T' + dataRow['eventEndTime'];

    var eventData = {
        id: currentCalEvent['id'],
        title: dataRow['title'],
        start: ISOStartDate,
        end: ISOEndDate,
        group_id: $('#sched-groups').val()
    };

    console.log(eventData);

    $.ajax({
        url: "/saveEvent",
        type: "PUT",
        contentType: "application/json",
        data: JSON.stringify(eventData),
        dataType: "json"
    })

    .done( function (response) {

        if (response)
        {
            $('#calendar').fullCalendar('refetchEvents')
        }

     })

     .fail ( function() {
        Materialize.toast('Error: Check Your Internet Connection', 4000)
     })

     .always (function() {

        $('#calendar').fullCalendar('unselect');
     })

    currentCalEvent = null
}

//Add New events to Calendar by clicking the Save button
function submitEvent()
{

    console.log("running");
    $('#eventModal').modal('close');

    var dataRow = {
        'title':$('#eventTitle').val(),
        'eventStartDate': $('#eventStartDate').val(),
        'eventStartTime': $('#eventStartTime').val(),
        'eventEndDate': $('#eventEndDate').val(),
        'eventEndTime': $('#eventEndTime').val(),
        'group_id': $('#sched-groups').val()
    };


    var ISOStartDate = dataRow['eventStartDate'] + 'T' + dataRow['eventStartTime'];
    var ISOEndDate = dataRow['eventEndDate'] + 'T' + dataRow['eventEndTime'];

    var eventData = {
        title: dataRow['title'],
        start: ISOStartDate,
        end: ISOEndDate,
        group_id: $('#sched-groups').val()
    };

    console.log(eventData);

    $.ajax({
        url: "/saveEvent",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(eventData),
        dataType: "json"
    })

    .done( function (response) {

        if (response)
        {
            color = response['color'];
            eventId = response['id'];
            eventData['color'] = color;
            eventData['id'] = eventId;
            $('#calendar').fullCalendar('renderEvent', eventData, true)
        }

     })

     .fail ( function() {
        Materialize.toast('Error: Check Your Internet Connection', 4000)
     })

     .always (function() {

        $('#calendar').fullCalendar('unselect');
     })

}

//Clear the Values of the Pop Up Form
function ClearPopupFormValues()
{
    $('#eventTitle').val("");
    $("#eventStartDate").val("");
    $("#eventStartTime").val("");
    $('#eventEndDate').val("");
    $('#eventEndTime').val("");
    $('#sched-groups').val("");
    $('select').material_select()
}
