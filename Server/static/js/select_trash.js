/**
 * Created by michaelperez on 4/16/17.
 */
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

$(document).ready(function() {
$("#button-mess").click( function() {

    var checkedVals = $('input.mail-checkbox:checkbox:checked').map(function() {
        return $(this).attr("data-id");
    }).get();

    for(var i = 0; i < checkedVals.length; i++)
    {
        $.ajax({
                        headers: { "X-CSRFToken": getCookie("csrftoken") },
                        type: 'POST',
                        url: '/messages/undelete_api/' + checkedVals[i]+"/",
                        dataType: 'json',
                        encode: true
        }).done(function(data) {
            console.log(data);
        });
    }

    location.reload();

})});