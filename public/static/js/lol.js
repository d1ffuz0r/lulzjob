/**
 * Created by PyCharm.
 * User: d1ffuz0r
 * Date: 08.12.11
 * Time: 21:46
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function()
{
    var csrf = $("input[name=csrfmiddlewaretoken]").val();

    $("#full .like").live('click', function()
    {
        var id = $("#full .counter");
        var type = $(this).attr('type');

        $.post('/ajax/like/', {id: id.attr('id'), type: type, csrfmiddlewaretoken: csrf}, function(res)
        {
            if(res.success)
            {
                id.html(res.likes);
            }
            else
            {
                alert("Уже голосовали!")
            }
        }, "json");
    });


    $(".more").live('click', function()
    {
        var hidden = $("#main .hidden");

        for(i=0; i<=hidden.length; i++)
        {
            $(hidden[i]).removeClass("hidden");

            if(!hidden.length)
            {
                $(".morebut").remove();
            }

            if(i == 9)
            {
                break;
            }
        }
    });

    $("#nav ul li").click(function()
    {
        $.each($("#nav ul li"), function(index, elem)
        {
            elem.id = '';
        });

        this.id = "current";
        var id = $(this).find('a').attr('id');
        var total = 0;

        $.post("/ajax/fetch/", {cat: id, csrfmiddlewaretoken: csrf}, function(res)
        {
            $("#main").empty();
            total = 0;

            $.each(res.jobs, function(index, job)
            {
                var JOB = '';
                var d = new Date(job.date);
                var m = parseInt(d.getMonth());
                if(total > 9)
                {
                    JOB += '<div class="cat_' + job.category + ' ' + total + ' hidden">';
                }
                else
                {
                    JOB += '<div class="cat_' + job.category + ' ' + total + '">';
                }
                JOB += '<h1>' + job.name + '</h1>';
                JOB += '<p>' + job.desc + '</p>';
                JOB += '<p class="post-footer">';
                JOB += '<a href="#full" class="readmore" id="' + job.id + '">Полностью</a> | ';
                JOB += 'Комментарии (' + job.comments + ') | ';
                JOB += '<span class="date">' + d.getDate() + ':' + (m+1) + ':' + d.getFullYear() + '</span> | ';
                JOB += '<span class="date">' + job.likes + '</span>';
                JOB += '</p>';
                JOB += '</div>';

                $("#main").append(JOB);

                total += 1;
            });

            if(total > 10)
            {
                var HTML = '<p class="post-footer morebut" style="float: right;"><a href="#more" class="more">Больше</a></p>';
                $("#main").append(HTML);
            }
        }, "json");
    });

    // show create vacancy form
    $("#add").click(function()
    {
        $(".add").show();
    });

    $(".close").click(function()
    {
        $(".popup, .bg").hide();
        $(".bg").css('background-image','');
    });

    $("#addvacancy").validate({
        onkeyup: false,
        onblur : false,
        submitHandler: function()
        {
            $("#addvacancy").ajaxSubmit(function(res)
            {
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

    $("#addcomment").validate({
        onkeyup: false,
        onblur : false,
        submitHandler: function()
        {
            $("#addcomment").ajaxSubmit(function(res)
            {
                var COMMENT = '';

                if (res.success)
                {
                    COMMENT += '<li>';
                    COMMENT += '<p>' + res.text + '</p>';
                    COMMENT += '</li>';

                    $("textarea[name=text]").val('');
                    $("#full .comments h1").remove();
                    $("#full .comments").append(COMMENT);
                }
                else
                {
                    $(".error.false").show('slow');
                }
            });
        }
    });

    $(".readmore").live('click', function()
    {
        var id = this.id;

        $.post('/ajax/full/',{id:id, csrfmiddlewaretoken: csrf}, function(res)
        {
            var v = res.vacancy;
            var DESC = '';
            var COMM = '';

            if(res.success)
            {
                $("input[name=job]").val(v.id);

                DESC += '<h3>'+v.name+'</h3>';
                DESC += '<p>'+v.desc+'</p>';
                DESC += '<p class="post-footer">';
                DESC += '<span class="date link"><a href="' + v.link + '" title="' + v.link + '" target="_blank">Оригинал</a></span>';
                DESC += '<span class="date likes"><span type="like" class="like">ГАГАГА</span>  ';
                DESC += '<span class="counter" id="' + v.id + '">'+v.likes+'</span>';
                DESC += '  <span type="unlike" class="like">WTF?</span> </span>';
                DESC += '</p>';

                if(res.comments.length > 0)
                {
                    $.each(res.comments, function(index, comment)
                    {
                        COMM += '<li>';
                        COMM += '<p>' + comment + '</p>';
                        COMM += '</li>';
                    });
                }
                else
                {
                    COMM = '<h1>Нет комментариев</h1>';
                }

                $(".bg").css('background', 'url(/media/' + v.cat_image + ')');
                $("#full, .bg").show();

                $("#full .desc").html(DESC);
                $("#full .comments").html(COMM);
            }
            {
                $("#full").show();
            }
        });
    });
});
