/**
 * Created by PyCharm.
 * User: d1ffuz0r
 * Date: 08.12.11
 * Time: 21:46
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function() {
    $("#add").click(function(){
        $(".add").show();
    });

    $(".close").click(function(){
        $(".popup, .bg").hide();
        $(".bg").css('background-image','');
    });

    $("#addvacancy").validate({
        onkeyup: false,
        onblur : false,
        submitHandler: function() {
            $("#addvacancy").ajaxSubmit(function(res) {
                if (res.success)
                {
                    $(".error.true").show('slow');
                }
                else
                {
                    $(".error.false").show('slow');
                }
                $("#addvacancy").hide('slow');
            });
        }
    });

    $(".readmore").live('click', function(){
        var id = this.id;
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        $.post('/ajax/full/',{id:id, csrfmiddlewaretoken: csrf}, function(res){
            var v = res.vacancy;
            var HTML = '';
            console.log(v);
            if(res.success)
            {
                HTML += '<h3>'+v.name+'</h3>';
                HTML += '<p>'+v.desc+'</p>';
                $(".bg").css('background', 'url(/media/' + v.cat_image + ')');
                console.log('/media/'+v.cat_image);
                $("#full, .bg").show();
                $("#full .desc").html(HTML);
            }
            {
                $("#full").show();
            }
        });
    });
});
