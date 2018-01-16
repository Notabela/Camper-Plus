$(document).ready(function () {

    $('.collapsible').collapsible();
    $('.modal').modal();
    $("#enrollments_drop").addClass("active");
    $("#enrollments_bar").addClass("active");
    $('select').material_select();
    $("#colorPicker").spectrum({
      color: "#00f",
      preferredFormat: "hex",
      showInput: true
    }).val("#00f");
    $('.datepicker').each(function(){
      var pickr = $(this).pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 80, // Creates a dropdown of 15 years to control year
        editable: true
      });
      $(this).click(function(){
          pickr.pickadate('open');
      });
      });
    /*
    $('.datepicker').pickadate({
      selectMonths: true, // Creates a dropdown to control month
      selectYears: 80, // Creates a dropdown of 15 years to control year,
      today: 'Today',
      clear: 'Clear',
      close: 'Ok',
      closeOnSelect: false // Close upon selecting a date,
    });
    */
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
    $("ul.buttonGroup").click(function (event) {
        //Select the selected segment
        $("li", this)
        .removeClass("selected")
        .filter(event.target)
        .addClass("selected");

        //Hide Everything
        $('#campers_data').addClass('hide');
        $('#groups_data').addClass('hide');
        $('#parents_data').addClass('hide');
        //Show the selected one
        $("#" + event.target.id + "_data").removeClass('hide');

        //Set the href attribute to bring up the correct Modal
        $('#menu').attr('href', '#' + $(event.target).attr('data-modal'));
    });
    $(".camper_checkbox").click(function () {
        var answer = confirm("Confirm Status Change");
        if (answer) {
            $.ajax({
                url: '/manage/camper',
                type: 'PATCH',
                contentType: 'application/json',
                data: JSON.stringify({'camper_id': $(this).attr('data-camper-id'), 'status': $(this).is(':checked')}),
                dataType: 'json'
            })
                .done(function (response){
                   console.log(response)
                })

                .fail(function (response) {
                    Materialize.toast('An Error Occurred', 4000)
                    Materialize.toast(response['msg'], 4000)
                })
        } else {
            if ($(this).is(':checked')) { $(this).prop('checked', false) }
            else { $(this).prop('checked', true)}
        }
    })
});

//Functions
function deleteCamper(camper_id) {
    var result = confirm("Are you sure you want to delete? This cannot be undone");
    if (result) {
        //Logic to delete the item
        $.ajax({
            url: "/manage/camper",
            type: "DELETE",
            contentType: "application/json",
            data: JSON.stringify({'camper_id': camper_id}),
            dataType: "json"
        })
            .done(function (response) {
                if (response) {
                    $("#camper_entry" + camper_id).remove()
                }
            })
            .fail(function () {
                Materialize.toast('An Error Occurred', 4000)
            })
    }
}

function editCamper(camper_id) {
     //Logic to delete the item
    $.ajax({
        url: "/manage/camper",
        type: "GET",
        contentType: "application/json",
        data: {'camper_id': camper_id},
    })
        .done(function (response) {
            if (response) {
                // undefined behavior
                var camper_data = response[0];
                $('#campers_modal').modal('open');

                $('#child_first_name').val(camper_data['first_name']);
                $('#child_last_name').val(camper_data['last_name']);
                $('#child_date').val(camper_data['date']);



                Materialize.updateTextFields();
            }
        })
        .fail(function () {
            Materialize.toast('An Error Occurred', 4000)
        })
}

function deleteGroup(group_id)
{
  var result = confirm("Are you sure you want to delete? This cannot be undone");
  if (result)
  {
    $.ajax({
        url: '/manage/campgroup',
        type: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({'group_id': group_id}),
        dataType: 'json'
    })
        .done( function (response) {
         if (response)
         {
           $("#group_entry" + group_id).remove()
         }
        })
        .fail(function () {
          Materialize.toast('An Error Occurred', 4000)
        })
  }
}

function deleteParent(parent_id)
{
  var result = confirm("Are you sure you want to delete? This cannot be undone");
  if (result)
  {
    $.ajax({
        url: '/manage/parent',
        type: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({'parent_id': parent_id}),
        dataType: 'json'
    })
        .done( function (response) {
         if (response)
         {
           $("#parent_entry" + parent_id).remove()
         }
        })
        .fail(function (response) {

            if (response && response.responseJSON.msg)
            {
                Materialize.toast(response.responseJSON.msg, 4000)
            } else {
                Materialize.toast('An Error Occurred', 4000)
            }
        })
  }
}