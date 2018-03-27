// 获取文章分类，然后js创建分类节点
$.getJSON('/category_list_handle/', function (ret) {
    $.each(ret, function (key, value) {
        var url = "/filter_category/" + key + "/";
        var cate = document.getElementById("cate-list");
        var span = document.createElement("span");
        span.setAttribute("class", "badge");
        var value1 = document.createTextNode(value[1]);
        span.appendChild(value1);
        var a = document.createElement("a");
        a.setAttribute("href", url);
        a.setAttribute("class", "list-group-item");
        var value0 = document.createTextNode(value[0]);
        a.appendChild(value0);
        a.appendChild(span);
        cate.appendChild(a);
    })
});

// 获取最新文章
$.getJSON('/new_article_json_handle/', function (ret) {
    $.each(ret, function (key, value) {
        var url = "/article/" + key + "/";
        var html = '<a href="' + url + '" class="list-group-item">' + value + '</a>';
        $("#new-list").append(html)
    })
});

// 获取热门文章
$.getJSON('/hot_article_json_handle/', function (ret) {
    // 定义排序规则 {id: 'id', data: ['title','num']}
    function compare(a, b) {
        if (a.data[1] < b.data[1])
            return -1;
        if (a.data[1] > b.data[1])
            return 1;
        return 0;
    }

    var countries = [];
    //将返回的JSON 数据变为 {id: 'id', data: ['title','num']} 的形式，并放入数组中
    $.each(ret, function (key, value) {
        countries.push({
            id: key,
            data: value
        })
    });
    // 使用自定义规则排序
    countries.sort(compare);

    // 遍历数据，并创建 HTML 代码
    for (var i = 0; i < countries.length; i++) {
        var url = "/article/" + countries[i].id + "/";
        var bagde = "<span class='badge'>" + countries[i].data[1] + "</span>";
        var html = '<a href="' + url + '" class="list-group-item">' + countries[i].data[0] + bagde + '</a>';
        $("#hot-list").prepend(html);
    }
});

// Message显示3秒后消失
$("#msg_alert").delay(3000).fadeOut();


// 文章内容页面的评论
// 添加引用
$(".quote_comment").click(function () {
    var $comment = $(document.getElementById("comment"));
    var user_comment = $(this).find('input').val();
    var quote_info = user_comment.split(",");
    // 获取引用的 用户名和对应评论内容
    var user = quote_info[0];
    var quote = quote_info[1];
    // 获取回复框中 已有的文本
    var old_value = $comment.val();
    // 组合新文本
    $comment.val("@" + user + "\n" + old_value + "[quote]\n" + quote + "\n[/quote]");
});

// 回复评论，获取评论的id和用户名
$(".reply_comment").click(function () {
    var $comment = $(document.getElementById("comment"));
    var id_user = $(this).find('input').val();
    var reply_info = id_user.split(",");
    // 获取回复评论的 id和用户名
    var id = reply_info[0];
    var user = reply_info[1];
    // 获取回复框中 已有的文本
    var old_value = $comment.val();
    // 组合新文本
    $comment.val("@" + user + "\n" + old_value);
});

// 删除评论(confirm确认)
$(".del_comment").click(function () {
    var d = confirm("确定删除此条评论？");
    if (d === true) {
        var id = $(this).find('input').val();
        var url = "/del_comment/" + id + "/";
        $.ajax({
            url: url,
            type: "GET",
            async: true,
            success: function () {
                location.reload()
            }
        });
    }
});

// 删除文章(弹出模态框确认)
$(".del_article").click(function () {
    var id = $(this).attr("id").split("_").pop();
    $("#del_id").val(id);
    var title = $(this).attr("title");
    $("#del_title").text(title)
});


// 个人信息修改页面
// 显示隐藏修改密码
$("#update_password").click(function () {
    $("#update_password_form").toggle();
});

// 取消修改密码(隐藏修改密码)
$("#cancel_update_password").click(function () {
    $("#update_password_form").hide();
});


// 登录表单验证
$("#login_form,#modal_login_form").validate({
    // error表示错误信息，element表示触发元素
    errorPlacement: function (error, element) {     // 错误信息显示位置
        $("#" + element.attr("id") + "_error").append(error);
    },
    highlight: function (element, errorClass) {     // 高亮显示,设置为错误样式// element是 DOM对象
        $(element).parent().removeClass("has-success").addClass("has-error");  // 第二个参数为样式,设置为错误样式
        $(element).next().css("color", "red");
    },
    unhighlight: function (element, errorClass) {   // 取消高亮,设定为正确样式
        var elem = $(element).parent();
        if (elem.hasClass("has-error")) {
            elem.removeClass("has-error");
            elem.addClass("has-success");
        } else {
            elem.addClass("has-success");
        }
        $(element).next().css("color", "");
    },
    rules: {
        "username": {
            required: true,
            rangelength: [3, 15]                // 长度范围
        },
        "password": {
            required: true,
            rangelength: [5, 32]
        }
    }
});


// 注册表单的验证
$("#register_form,#modal_register_form").validate({
    // debug: true,                                    // 调试模式
    submitHandler: function (form) {
        form.submit();                              // 手动提交
    },
    // error表示错误信息，element表示触发元素
    errorPlacement: function (error, element) {     // 错误信息显示位置
        $("#" + element.attr("id") + "_error").append(error);
    },
    highlight: function (element, errorClass) {     // 高亮显示,设置为错误样式
        // element是 DOM对象
        $(element).parent().removeClass("has-success").addClass("has-error");  // 第二个参数为样式,设置为错误样式
        $(element).next().css("color", "red");
    },
    unhighlight: function (element, errorClass) {   // 取消高亮,设定为正确样式
        var elem = $(element).parent();
        if (elem.hasClass("has-error")) {
            elem.removeClass("has-error");
            elem.addClass("has-success");
        } else {
            elem.addClass("has-success");
        }
        $(element).next().css("color", "");
    },

    // 使用下面的错误样式会导致 高亮显示位置错误 所以直接在高亮中设置样式
    // errorClass: "",                              // 定义的错误样式
    // validClass : "",                             // 定义的正确样式
    rules: {
        username: {
            required: true,
            rangelength: [3, 15],
            remote: {
                url: "/user/check_username/",
                type: "POST",
                data: {  // 发送数据
                    "username": function () {
                        return $("#reg_username").val();
                    }
                },
                dataFilter: function (data, type) {  // 处理完成执行
                    return data.trim() === "true";
                }
            }
        },
        email: {
            required: true,
            email: true
        },
        password: {
            required: true,
            rangelength: [5, 32]
        },
        re_password: {
            required: true,
            rangelength: [5, 32],
            equalTo: "#reg_password"
        }

    },
    messages: {
        "username": {
            required: "用户名不能为空",
            remote: "用户名已存在"
        }
    }
});


// 登录和注册模态框切换
$(".my_modal_login").click(function () {
    $("#registerModal").modal("hide");
});
$(".my_modal_register").click(function () {
    $("#loginModal").modal("hide");
});