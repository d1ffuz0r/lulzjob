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

            if(res.jobs.length)
            {
                $.each(res.jobs, function(index, job)
                {
                    var html = '';
                    var d = new Date(job.date);
                    var m = parseInt(d.getMonth());

                    html += '<article>';
                    if(total > 9)
                    {
                        html += '<div class="cat_' + job.category + ' ' + total + ' hidden">';
                    }
                    else
                    {
                        html += '<div class="cat_' + job.category + ' ' + total + '">';
                    }
                    html += '<h1>' + job.name + '</h1>';
                    html += '<p>' + job.desc + '</p>';
                    html += '<p class="post-footer">';
                    html += '<a href="#full" class="readmore" id="' + job.id + '">Полностью</a> | ';
                    html += 'Комментарии (' + job.comments + ') | ';
                    html += '<span class="date">' + d.getDate() + ':' + (m+1) + ':' + d.getFullYear() + '</span> | ';
                    html += '<span class="date">Рейтинг: ' + job.likes + '</span>';
                    html += '</p>';
                    html += '</div>';
                    html += '</article>';

                    $("#main").append(html);

                    total += 1;
                });
            }
            else
            {
                $("#main").append("<h1>ПРИШЛО ВРЕМЯ ДОБАВИТЬ ВАКАНСИЙ</h1>");
            }

            if(total > 10)
            {
                $("#main").append('<p class="post-footer morebut" style="float: right;"><a href="#more" class="more">Больше</a></p>');
            }
        }, "json");
    });

    // show create vacancy form
    $("#add").click(function()
    {
        $(".add, .add form").show();
    });

    $(".close").click(function()
    {
        $(".popup, .bg").hide();
        $(".bg").css('background-image','');
    });

    $("#addvacancy").validate(
    {
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

    $("#addcomment").validate(
    {
        onkeyup: false,
        onblur : false,
        submitHandler: function()
        {
            $("#addcomment").ajaxSubmit(function(res)
            {
                var comment = '';

                if (res.success)
                {
                    comment += '<li>';
                    comment += '<p>' + res.text + '</p>';
                    comment += '</li>';

                    $("textarea[name=text]").val('');
                    $("#full .comments h1").remove();
                    $("#full .comments").append(comment);
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
            var desc = '';
            var comm = '';

            if(res.success)
            {
                $("input[name=job]").val(v.id);

                desc += '<h3>'+v.name+'</h3>';
                desc += '<p>'+v.desc+'</p>';
                desc += '<p class="post-footer">';
                desc += '<span class="date link"><a href="' + v.link + '" title="' + v.link + '" target="_blank">Оригинал</a></span>';
                desc += '<span class="date likes"><span type="like" class="like">ГАГАГА</span>  ';
                desc += '<span class="counter" id="' + v.id + '">'+v.likes+'</span>';
                desc += '  <span type="unlike" class="like">WTF?</span> </span>';
                desc += '</p>';

                if(res.comments.length > 0)
                {
                    $.each(res.comments, function(index, comment)
                    {
                        comm += '<li>';
                        comm += '<p>' + comment + '</p>';
                        comm += '</li>';
                    });
                }
                else
                {
                    comm = '<h1>Нет комментариев</h1>';
                }

                $(".bg").css('background', 'url(/site_media/' + v.cat_image + ')');
                $("#full, .bg").show();

                $("#full .desc").html(desc);
                $("#full .comments").html(comm);
            }
            {
                $("#full").show();
            }
        });
    });
});
