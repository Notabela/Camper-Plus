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
    });
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
      constrainWidth: false, // Does not change width of dropdown to that of the activator
      hover: true, // Activate on hover
      gutter: 0, // Spacing from edge
      belowOrigin: false, // Displays dropdown below the button
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

        //Set custom value for color picker
        $("#colorPicker").val("#00f");
    });

});