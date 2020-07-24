layui.define(['layer', 'form', 'tips'], function (exports) {
   layer = layui.layer,
      $ = layui.$,
      tips = layui.tips;
    layui.use('form', function () {
    var form = layui.form;

    
  }); 

  function adddata(){
    let ID = plugins.GetRequest().id;
    let product = plugins.GetRequest().product;
    let operate = plugins.GetRequest().operate;
    let num = plugins.GetRequest().num;
    let date = plugins.GetRequest().date;
    let fare = plugins.GetRequest().fare;

    if(operate=="出库"){
       out_in = -1
    }else{
      out_in = 1;
    }
    $('.ID').val(ID);
    $('.product_name').val(product);
    $('.operate').val(operate);
    $('.num').val(num);
    $('.fare').val(fare);
    $('.date').val(date);
    $('.out_in').val(out_in);

    
  }
adddata();

  
    
  


   $('#Keep').click(function () {
       var ID =plugins.GetRequest().id;
       var num = $('.num').val();
       var product_name = $('.product_name').val();
       var date =$('.date').val();
       var fare = $('.fare').val();
       var out_in = $('.out_in').val();
           
            
               plugins.AjaxPlugin({
                url: plugins.realm()+'/edit',
                type: 'post',
                data: {
                        "ID":ID,
                        "product_name":product_name,
                        "out_in":out_in,
                        "num":num,
                        "date":date,
                        "fare":fare
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
            
         
      })

   exports('edit', {});
});