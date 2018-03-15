// 个人信息修改页面
// 显示隐藏修改密码
$("#update_password").click(function () {
    $("#update_password_form").toggle();
});

// 取消修改密码(隐藏修改密码)
$("#cancel_update_password").click(function () {
    $("#update_password_form").hide();
});