/**
 * Created by michaelperez on 4/2/17.
 */

function updateLogs(name, response, number){
            $(name).empty();
            for(var i = 0; (number==-1 || i<number) && i<response.objects.length; i++){
                $(name).append("<tr>" +
                            "<td>"+ response.objects[i]['user__username']+"</td>" +
                            "<td>"+ response.objects[i]['date']+"</td>" +
                            "<td>"+ response.objects[i]['typeChange']+"</td>" +
                        "</tr>");
            }
}

$(document).ready(function() {

    $('#see_all_logs').click(function()
    {
        $('#logsModal').modal('show');
        search = $('#search_modal').val();
         $.ajax({
        type: 'GET',
        url: '/log/',
        dataType: 'json',
        data: {
          'search':search,
        },
        encode: true,

    }).done(function(response){
        if(response.success == 1){
            console.log('success');
            updateLogs('#actions_body_modal',response, -1);
        }
    });

    });


    $('#search').keyup(function(){
        var search = $('#search').val();

        $.ajax({
        type: 'GET',
        url: '/log/',
        dataType: 'json',
        data: {
          'search':search,
        },
        encode: true,

    }).done(function(response){
        if(response.success == 1){
            console.log('success');
            updateLogs('#actions_body',response, 10);
        }
    }
    );

    });

    $('#search_modal').keyup(function(){
        var search = $('#search_modal').val();

        $.ajax({
        type: 'GET',
        url: '/log/',
        dataType: 'json',
        data: {
          'search':search,
        },
        encode: true,

    }).done(function(response){
        if(response.success == 1){
            console.log('success');
            updateLogs('#actions_body_modal',response, -1);
        }
    }
    );

    });

    $.ajax({
        type: 'GET',
        url: '/log/',
        dataType: 'json',
        data: {
          'search':''
        },
        encode: true,

    }).done(function(response){
        if(response.success == 1){
            console.log('success');
            updateLogs('#actions_body',response, 10);
        }
    }
    );

    $.ajax({
        type: 'GET',
        url: 'stats',
        dataType: 'json',
        encode: true,
    }).done(function (response) {
        if(response.success == 1) {
            new Morris.Line({
                // ID of the element in which to draw the chart.
                element: 'myfirstchart',
                // Chart data records -- each entry in this array corresponds to a point on
                // the chart.
                data:  response.date,
                xkey: response.xkeys,
                // A list of names of data record attributes that contain y-values.
                ykeys: response.ykeys,
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: response.labels
            });
        }

    });
});

