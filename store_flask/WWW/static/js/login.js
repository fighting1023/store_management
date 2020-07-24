layui.define(['layer', 'form', 'tips'], function (exports) {
    var form = layui.form,
        layer = layui.layer,
        $ = layui.$,
        tips = layui.tips;


    // 登陆检测
    $('#dlsub').click(function () {

           let username = $('#account').val();
           let password = $('.pasd').val();
           

        if ($('#account').val() && $('.pasd').val()) {
           
            plugins.AjaxPlugin({
                url: plugins.realm()+'/login',
                type: 'post',
                data: {
                        "username":username,
                        "password":password
                    },
                action: function (data) {
                    console.log(data.data)
                
                    
                $.cookie('username',data.data.username, { path: '/', expires: 1 });
                $.cookie('power',data.data.right, { path: '/', expires: 1 });
            
                   
                    window.location = '../index.html';

                },
                othererro: function (data) {
                    tips.warning(data.msg);
                }
            });
        } else {
            tips.warning('请把信息填写完整');
            return false;
        }
    });

    $(document).keydown(function (event) {
        if (event.keyCode == 13) {
            $('#dlsub').click();
        }
    });

    exports('login', {});
});