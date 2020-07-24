layui.define(['layer', 'form', 'tips'], function (exports) {
  var form = layui.form,
    layer = layui.layer,
    $ = layui.$,
    tips = layui.tips;

  layui.use('form', function () {
    var form = layui.form;

    form.on('select(searchgoods)', function (data) {
      $('#searchgoods').val(data.value);

    });
    form.on('select(orderStatus)', function (data) {
      $('#orderStatus').val(data.value);

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
    url: plugins.realm() + '/products/lists',
    type: 'get',
    dataType: 'json',
    action: function (data) {

      for (var i = 0; i < data.data.length; i++) {
        // plugins.console(data.data[i].productName)
        $('.searchgoods').append(
          '<option value="' + data.data[i].productId + '">' + data.data[i].productName + '</option>'
        )
      }
      renderForm()
    }
  });

  function addCount(data) {
    for (var i = 0; i < data.data.dataList.length; i++) {
      $('.layui-table1').append(
        '<tr>' +
        '<td>' + data.data.dataList[i].orderNum + '</td>' +
        '<td>' + data.data.dataList[i].productName + '</td>' +
        '<td>' + data.data.dataList[i].name + '</td>' +
        '<td>' + data.data.dataList[i].userPhone + '</td>' +
        '<td>' + data.data.dataList[i].amount + '</td>' +
        '<td>' + data.data.dataList[i].orderType + '</td>' +
        '<td>' + data.data.dataList[i].fromType + '</td>' +
        '<td>' + data.data.dataList[i].createTime + '</td>' +
        '<td>' + data.data.dataList[i].payNum + '</td>' +

        '</tr>'
      )
      
    }

   
    $('.layui-table1').prepend(
      '<thead>' +
      '<tr>' +
      ' <th>订单ID</th>' +
      ' <th>产品</th>' +
      ' <th>用户名</th>' +
      ' <th>手机号</th>'+
      ' <th>流水金额</th>' +
      ' <th>流水类型</th>' +
      ' <th>流水来源</th>' + 
      ' <th>时间</th>' +
      ' <th>支付单号</th>' +
      ' </tr>' +
      ' </thead> '
    )

 
     $('.layui-table1').append(
      '<tr>' +
      '<td style="width:50%" colspan="3">总笔数:' + data.data.countAmount.allNum + '</td>' +
      '<td style="width:50%" colspan="6">总流水:' + Number(data.data.countAmount.allAmount).toFixed(2) + '</td>' +
      '</tr>'
    )


    for (var i = 0; i < $('td').length; i++) {
      if ($('td').eq(i).text() == 0) {
        $('td').eq(i).text('-')
      }
    }
  }

  function getData() {
    plugins.tq_page({
      elem: 'laypage1',
      url: plugins.realm() + '/finances/count-lists',
      type: 'post',
      dataType: 'json',
      // datas:
      datas: {
        'orderNum': $('#inputData').val(),
        'productid': $('#searchgoods').val(),
        'orderStatus': $('#orderStatus').val(),
        'period': $('#date3').val(),
      },
      page: function (data) {
        layer.closeAll('loading');
        $('.layui-table').empty();
        addCount(data)
      }
    })
   
  }
  getData()

  layui.use('laydate', function () {
    var laydate = layui.laydate;

    //执行一个laydate实例
    laydate.render({
      elem: '#date3',
      range: true //或 range: '~' 来自定义分割字符
        ,
      done: function (value, date, endDate) {
        $('#date3').val(value);
      }
    });
  });



  $('#searchAction').click(function () {
    getData()
  })


  exports('examine', {});
});