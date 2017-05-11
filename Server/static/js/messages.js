/**
 * Created by michaelperez on 4/16/17.
 */

function get_time_next(time)
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
            return [Math.round(hours) + " Hours Ago!", hours*0.001];
        }
        else
        {
          if(Math.round(days) == 1)
          {
            return ["Yesterday", days*0.01];
          }
          else
          {
            return [Math.round(days) + " Days Ago!", days*0.01];
          }
        }
    }
    else
    {
      if(Math.round(weeks) == 1)
      {
        return ["Last Week",  weeks*0.1];
      }
      else {
          return [Math.round(weeks) + " Weeks Ago!", weeks * 0.1];
      }
    }
  }
  else
  {
    return [Math.round(months) + "Months ago!", months*1];
  }

}


$(document).ready(function() {
$.ajax({
        type: 'GET',
        url: '/messages/get_messages',
        data: {
            'type': 'messages',
            'n': 10,
        },
        dataType: 'json',
        encode: true
      })
        .done(function(data) {
            if(data.success == 1) {
                $('#messages_count').text(data.count);

                $("#messages_drop").empty();

                for(var i = 0; i < data.count && i < 5; i++)
                {
                    var person = data.message_list[i];
                    var name = person.person;
                    var content = person.body;
                    var d = new Date();
                    var time = get_time_next(d.getTime() - person.sent_at)[0];

                    var str ='<li class="message-preview">\
                            <a href="/messages/view/'+ person.id +'">\
                                <div class="media">\
                                    <span class="pull-left">\
                                        <img class="media-object" src="http://placehold.it/50x50" alt="">\
                                    </span>\
                                    <div class="media-body">\
                                        <h5 class="media-heading"><strong>' + name  + '</strong>\
                                        </h5>\
                                        <p class="small text-muted"><i class="fa fa-clock-o"></i>'+ time +'</p>\
                                        <p>'+content+'</p>\
                                    </div>\
                                </div>\
                            </a>\
                        </li>'

                    $("#messages_drop").append(str);
                }

                    $("#messages_drop").append('<li class="message-footer">\
                            <a href="/messages/inbox">Read All New Messages</a>\
                        </li>');


            }
        });
});