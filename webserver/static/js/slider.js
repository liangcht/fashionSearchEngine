$(function() {
  $( "#slider-range-max" ).slider({
    range: "max",
    min: 0,
    max: 10,
    value: 5,
    lide: function( event, ui ) {
      $( "#amount" ).val( ui.value );
      $.ajax({
            url: '/test',
            data: {'factor': ui.value},
            type: 'POST',
          success: function(rawData) {
            data = $.parseJSON(rawData);
            console.log("success");
            var field = 'name';
            console.log(data[field]);
          },
          error: function(error) {
            console.log("error");
          }
        });
      }
    });
  $( "#amount" ).val( $( "#slider-range-max" ).slider( "value" ) );
});