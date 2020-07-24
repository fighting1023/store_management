layui.define(['layer', 'form', 'tips'], function (exports) {
   layer = layui.layer,
      $ = layui.$,
      tips = layui.tips;
    layui.use('form', function () {
    var form = layui.form;

    form.on('select(searchgoods)', function (data) {
      $('#searchgoods').val(data.value);

    });
     form.on('select(out_in)', function (data) {
      $('#out_in').val(data.value);
        // console.log(data.value)
    });
    
  }); 

  function renderForm() {
    layui.use('form', function () {
      var form = layui.form; //高版本建议把括号去掉，有的低版本，需要加()
      form.render();
    });
  }
    // 获取产品
  plugins.AjaxPlugin({
    url: plugins.realm() + '/productlist',
    type: 'get',
    dataType: 'json',
    action: function (data) {
      for (var i = 0; i < data.data.length; i++) {
        // plugins.console(data.data[i].productName)
        $('.searchgoods').append(
          '<option value="' + data.data[i].id + '">' + data.data[i].product_name + '</option>'
        )
      }
      renderForm()
    }

  });

   
    // 时间实列
   $('#date2').val(plugins.getDay());
  layui.use('laydate', function () {
    var laydate = layui.laydate;
    //执行一个laydate实例
    laydate.render({
      elem: '#date2',
      value: new Date(),
      done: function (value, date, endDate) {
        $('#date2').val(value);
         
      }
    });

  });


   $('#Keep').click(function () {
       var seat =$('.seatStock').val();
       var produce_name =$('#searchgoods').val();
       var out_in =$('#out_in').val();
       var num =$('.num').val();
       var date =$('#date2').val();
       var fare =$('.fare').val();
       var operator =$('.operator').val();
      
       console.log(typeof num )
       console.log(typeof out_in )
       console.log(out_in )
       console.log(typeof fare )

         if (produce_name && operator) {
             if(num>0){
               plugins.AjaxPlugin({
                url: plugins.realm()+'/operateStock',
                type: 'post',
                data: {
                        "seat":seat,
                        "produce_name":produce_name,
                        "out_in":out_in,
                        "num":num,
                        "date":date,
                        "fare":fare,
                        "operator":operator
                    },
                action: function (data) {
                    console.log(data.data)
                               
                    tips.warning("添加成功");
                    // location.reload();
                    // window.location = '../index.html';

                },
                othererro: function (data) {
                    tips.warning(data.msg);
                }
            });
           }else{
             tips.warning('请填写有意义的数量');
           }
         } else {
            tips.warning('请把信息填写完整');
         }
      })
   exports('hqstock', {});
});