
function get_div(result)
{
   /*
    <a href="#" class="list-group-item">
                        <span class="badge">Next Month</span>
                        Appointment 1 with Dr. Dre
                    </a>
     */

   times = [];
   titles = {};
   urls = {};
   sorted_values = [];
   dict = {};

   for(var key in result) {
       object = result[key];
       var d = new Date();
       var now = d.getTime();

       var title = object['title'];
       var notes = object['notes'];
       var end = object['end'];
       var url = object['url'];

       urls[get_time(end - now)[1]] = url;
       titles[get_time(end - now)[1]] = title;
       times.push(get_time(end - now));
   }

   for(var key in times)
   {
     dict[times[key][1]] = times[key][0];
     sorted_values.push(times[key][1]);
   }

   result = "";
   sorted = sorted_values.sort();

   for(var key in sorted) {
       result += "<a class=\"list-group-item appointment_item\" data-value="+ urls[sorted_values[key]] +">" +
           "<span class=\"badge\">" + dict[sorted_values[key]] + "</span>" +
           titles[sorted_values[key]] +
           "</a>";
   }

    //update label
   $('#number_appointments').text(sorted.length);

   return result;
}

function get_time(time)
{
  //calculate month first to see if the event is exactly one month away, then weeks, then day, then hours
  var months = time/2629746000;
  var weeks = time/604800000;
  var days = time/86400000;
  var hours = time/3600000;

  if(months < 1)
  {
    if(weeks < 1)
    {
        if(days < 1)
        {
            return ["In " + Math.round(hours) + " Hours", hours*0.001];
        }
        else
        {
          if(Math.round(days) == 1)
          {
            return ["Tomorrow", days*0.01];
          }
          else
          {
            return ["In " + Math.round(days) + " Days", days*0.01];
          }
        }
    }
    else
    {
      if(Math.round(weeks) == 1)
      {
        return ["Next Week",  weeks*0.1];
      }
      else {
          return ["In " + Math.round(weeks) + " Weeks", weeks * 0.1];
      }
    }
  }
  else
  {
    return ["Next Month", months*1];
  }

}


function reload_appointments(){
  var d = new Date();
    var milli = d.getTime();
    var milli_month = milli + 2629746000;

    $.ajax({
        type: 'GET',
        url: '/accounts/view_apt',
        data: {
            'from': milli,
            'to':milli_month,
        },
        dataType: 'json',
        encode: true
    })
        .done(function(data) {
            if(data['success'] == 1)
            {
                $('#appointmentslist').empty();
                $('#appointmentslist').append(get_div(data['result']));
            }
        });

    $(".form-group strong").text("");
}

function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

$(document).ready(function() {
    reload_appointments();

    $('#createAptButton').click(function() {
      $('#createApptForm').ajaxSubmit({
          url: '/accounts/create_apt/', type: 'POST', success: function (data) {

              if(data.success == 1){
                //close modal and reload appointments and calendar
                calendar.view();
                reload_appointments();
                $('#createAppointment').modal('toggle');
              }
              else {
                if(data.errors.dateTimeStart != undefined)
                  $('#datetime_errors').text(data.errors.dateTimeStart[0]);
                if(data.errors.doctor != undefined)
                  $('#doctor_errors').text(data.errors.doctor[0]);
                if(data.errors.location != undefined)
                  $('#location_errors').text(data.errors.location[0]);
                if(data.errors.notes != undefined)
                  $('#notes_errors').text(data.errors.notes[0]);

              }
          }

      });
    });


    $('#appointmentslist').on('click', '.appointment_item', function(event) {
      var id = $(this).data('value');

      $.ajax({
        type: 'GET',
        url: '/accounts/update_apt',
        data: {
            'id': id,
        },
        dataType: 'json',
        encode: true
      })
        .done(function(data) {
            if(data['success'] == 1)
            {
                var patient = data['patient'];
                var datetime = data['datetime'];

                var date = new Date(datetime);
                date.setHours(date.getHours() - 5);
                datetime = date.toISOString().substr(0, 19);

                var location = data['location'];
                var notes = data['notes'];

                $('#editAppointment').modal('toggle');
                $(".modal-body .doctor_").val( patient );
                $(".modal-body .datetime_").val( datetime );
                $(".modal-body .location_").val( location );
                $(".modal-body .notes_").val( notes );

                $("#cancelAptButton").off("click");
                $('#cancelAptButton').click(function() {
                    $.ajax({
                        type: 'POST',
                        url: '/accounts/update_apt/',
                        data: {
                          'action' : 'delete',
                          'id' : id,
                        },
                        encode: true

                    }).always(function(data_) {
                        $('#editAppointment').modal('toggle');
                        reload_appointments();
                        calendar.view();
                    });
                });


                $("#editAptButton").off("click");
                $('#editAptButton').click(function() {
                    $.ajax({
                        type: 'POST',
                        url: '/accounts/update_apt/',
                        data: {
                            'action': 'update',
                            'id': id,
                            'form': JSON.stringify(getFormData($("#editApptForm"))),
                        },
                        dataType: 'json',
                        encode: true
                    }).always(function(data_){


                      if(data_['success'] == 1){
                        $('#editAppointment').modal('toggle');
                        reload_appointments();
                        calendar.view();
                      }
                      else {
                          if(data_.errors.dateTimeStart != undefined)
                              $('#datetime_errors_').text(data_.errors.dateTimeStart[0]);
                          if(data_.errors.doctor != undefined)
                              $('#doctor_errors_').text(data_.errors.doctor[0]);
                          if(data_.errors.location != undefined)
                              $('#location_errors_').text(data_.errors.location[0]);
                          if(data_.errors.notes != undefined)
                              $('#notes_errors_').text(data_.errors.notes[0]);
                      }

                    });
                });
            }
        });


});


});