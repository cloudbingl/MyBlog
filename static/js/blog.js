// 每次刷新页面都去获取文章分类，然后js创建分类节点
$.getJSON('/category_list_handle/?t=' + new Date(), function (ret) {
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
$.getJSON('/new_article_json_handle/?t=' + new Date(), function (ret) {
    $.each(ret, function (key, value) {
        var url = "/article/" + key + "/";
        var html = '<a href="' + url + '" class="list-group-item">' + value + '</a>';
        $("#new-list").append(html)
    })
});


// 获取热门文章
$.getJSON('/hot_article_json_handle/?t=' + new Date(), function (ret) {
    // 根据{"id":(title, num)}中的num排序
    function sortRead(a, b) {
        return !(a.id[1] - b.id[1]);
    }
    [].slice.call(ret).sort(sortRead);

    $.each(ret, function (key, value) {
        var url = "/article/" + key + "/";
        var bagde_html = "<span class='badge'>"+ value[1] +"</span>"
        var html = '<a href="' + url + '" class="list-group-item">' + value[0] + bagde_html + '</a>';
        // 排序后是正序，使用prepend()可以依次从后向前插入标签
        // 从而显示为 阅读量从高到低排序
        $("#hot-list").prepend(html)
    })
});

// 初始化富文本框
// tinyMCE.init({
//     'mode': 'textareas',
//     'theme': 'advanced',
//     'language': 'zh-CN'
// });

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


