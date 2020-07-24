layui.define(['layer', 'form', 'tips'], function (exports) {
   layer = layui.layer,
      $ = layui.$,
      tips = layui.tips;
   
  
   
    // 时间范围实列
  layui.use('laydate', function () {
    var laydate = layui.laydate;

    //执行一个laydate实例
    laydate.render({
      elem: '#date2',
      type: 'date',
      value:plugins.getDay(),
      done: function (value, date, endDate) {
        $('#date2').val(value);
      }
    });
  });


   $('#Keep').click(function () {
      var product_name = $('.productName').val();
      var add_date = $('#date2').val();
      
         if (product_name && add_date) {
            
               plugins.AjaxPlugin({
                url: plugins.realm()+'/addproduct',
                type: 'post',
                data: {
                        "product_name":product_name,
                        "add_date":add_date
                    },
                action: function (data) {
                    console.log(data.data)
                
               
                    tips.warning("添加成功");
                   
                    // window.location = '../index.html';

                },
                othererro: function (data) {
                    tips.warning(data.msg);
                }
            });
            
         } else {
            tips.warning('请把信息填写完整');
         }
      })
   
   exports('addproduct', {});
});