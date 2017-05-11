/**
 * Created by michaelperez on 5/7/17.
 */
/**
 * Created by michaelperez on 4/30/17.
 */

/*
<tr>
    <td>Ibuprofen 200mg</td>
    <td>10</td>
    <td>12/12/2017</td>
</tr>
<tr>
    <td>Notrealitinis 900mg</td>
    <td>0</td>
    <td>6/12/2017</td>
</tr>
<tr>
    <td>HIV Medication 200mg</td>
    <td>Infinite</td>
    <td>Never</td>
</tr>
*/

function get_presc_div(list) {
    $("#presc_n").text(list.length);
    var output = "";
    for(var i = 0; i < list.length; i++) {
        output += "<tr>\
                    <td>" + list[i].medication +"</td>\
                    <td>" + list[i].refills +"</td>\
                    <td>"+list[i].expiration_date+"</td>\
                    </tr>"
    }
    return output;
}

$(document).ready(function() {

        $.ajax({
            type: 'GET',
            url: '/get_presc/',
            dataType: 'json',
            encode: true
        })
            .done(function (data) {
                if (data['success'] == 1) {
                    $('#presc_body').empty();
                    $('#presc_body').append(get_presc_div(data.objects));
                }
            }).
        fail(function (data) {
            console.log("Error");
        });

    });