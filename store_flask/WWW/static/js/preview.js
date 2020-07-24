layui.define(['layer', 'form', 'tips'], function (exports) {
  var form = layui.form,
    layer = layui.layer,
    $ = layui.$,
    tips = layui.tips;
     function renderForm() {
        layui.use('form', function () {
          var form = layui.form; //高版本建议把括号去掉，有的低版本，需要加()
          form.render();
        });
      }
    function addseat(){
       $('.seatStock').append(
          '<option value="'+plugins.hqstock+'">' + plugins.hqstock + '库存</option>'
        )
        $('.seatStock').append(
          '<option value="'+plugins.zkstock+'">' + plugins.zkstock + '库存</option>'
        )
        renderForm()
         $('#seatStock').val(plugins.hqstock);
  }
  addseat()

  layui.use('form', function () {
    var form = layui.form;
    
    form.on('select(seatStock)', function (data) {
      $('#seatStock').val(data.value);
      // if(data.value==1){
      //    $('.seathouse').text(plugins.hqstock)
      // }else if(data.value==2){
      //    $('.seathouse').text(plugins.zkstock)
      // }
      $('.layui-table1 .tr1').empty();
      $('.layui-table1 .tr2').empty();
      checkseat();

    });

    form.on('select(searchgoods)', function (data) {
      // $('#searchgoods').val(data.value);
      console.log(data)

    });
    
     form.on('select(tiaojian)', function (data) {
      $('#tiaojian').val(data.value);

    });
  });

 
 
  // 获取当下日期  // 时间范围实列
  
  $('.startdate').val(plugins.fun_date(-30))
  $('.enddate').val(plugins.getDay())
  var dates = plugins.fun_date(-30)+' - '+plugins.getDay()
  layui.use('laydate', function () {
    var laydate = layui.laydate;
    //执行一个laydate实例
    laydate.render({
      elem: '#date2',
      range: true, //或 range: '~' 来自定义分割字符
      value:dates,
      done: function (value, date, endDate) {
          $('.startdate').val(value.substring(0,10))
          $('.enddate').val(value.substring(13,value.length))
      }   
    });
  });  
  




  // 获取产品
  plugins.AjaxPlugin({
    url: plugins.realm() + '/productlist',
    type: 'get',
    dataType: 'json',
    action: function (data) {
      console.log(data)
      for (var i = 0; i < data.data.length; i++) {
        // plugins.console(data.data[i].productName)
        $('.searchgoods').append(
          '<option value="' + data.data[i].product_name + '">' + data.data[i].product_name + '</option>'
        )
      }
      renderForm()
    }

  });
 

 //获取所有总共库存量
 function total(){
     plugins.AjaxPlugin({
        url: plugins.realm() + '/total',
        type: 'post',
        data:{
          "seat1":'中科院',
          "seat2":'怀柔'
        },
        dataType: 'json',
        action: function (data) {
          console.log(data)
          $('.all').text(data.data.allstock)
          $('.zk').text(data.data.seat1_stock)
          $('.hq').text(data.data.seat2_stock)
        }

      });
 }


 //添加地方库存信息
 function checkseat(){
      let seat = $('#seatStock').val();
     console.log(seat)
     plugins.AjaxPlugin({
        url: plugins.realm() + '/warehouse',
        type: 'post',
        dataType: 'json',
        data:{
           "seat":seat
        },
        action: function (data) {
          let datas = data.data
          console.log(datas)
          for(var i =0;i<datas.length;i++){
              $('.layui-table1 .tr1').prepend(
                '<th>'+datas[i].product_name+'</th>'
                )
              $('.layui-table1 .tr2').append(
                '<th>'+datas[i].product_num+'</th>'
                )

           }

        }

      });
 }

//添加合计信息
function sum(){
      let seat = $('#seatStock').val();

      let product_name  = $('#searchgoods').val();
      
      let condation = $('#tiaojian').val();
      let startdate = $('.startdate').val();
      let enddate = $('.enddate').val();
     plugins.AjaxPlugin({
        url: plugins.realm() + '/sum',
        type: 'post',
        dataType: 'json',
        data:{
        'seat': seat,
        'product_name':product_name,

        'condation':condation,
        'startdate':startdate,
        'enddate':enddate,
      },
        action: function (data) {
          console.log(data)
          $('.inTotal').text(data.data.allinstock)
          $('.outTotal').text(data.data.alloutstock)
          $('.fareTotal').text(data.data.allfare)
        }
      });
}






  function addCount(data) {
    for (var i = 0; i < data.data.dataList.length; i++) {
       j=i+1;
      if(data.data.dataList[i].operation==1){
           operation = "入库"
       }else{
           operation = "出库"
       }
       // var riqi = data.data.dataList[i].opttime
       let id =data.data.dataList[i].id;
       let product =data.data.dataList[i].product_name;
       let operate = operation;
       let num =data.data.dataList[i].number;
       let date =data.data.dataList[i].opttime;
       let fare =data.data.dataList[i].fare;     

       var href = "./html/edit.html?id="+id+"&product="+product+"&date="+date+"&operate="+operate+"&num="+num+"&fare="+fare;
      
      $('.layui-table').append(
        '<tr>' +
        '<td>'+j+'</td>' +
        // '<td lau-href="'+href+'" lau-title="渠道:'+data.data.dataList[i].id+'" class="laychannel">' + data.data.dataList[i].id + '</td>' + 
        '<td>' + data.data.dataList[i].product_name + '</td>' +
        '<td>' + operation + '</td>' +
        '<td>' + data.data.dataList[i].number + '</td>' +
        '<td>' + data.data.dataList[i].opttime + '</td>' +
        '<td>' + data.data.dataList[i].stock + '</td>' +
        '<td>' + data.data.dataList[i].fare + '</td>' +
        '<td>' + data.data.dataList[i].operator + '</td>' +
        '<td lau-href="'+href+'" lau-title="编辑'+j+'" >编辑</td>' +
        '</tr>'
      )
    }
    
     $('.layui-table2').prepend(
      '<thead>' +
      '<tr>' +
      ' <th>序列</th>' +
      ' <th>产品</th>' +
      ' <th>操作</th>' +
      ' <th>数量</th>' +
      ' <th>操作时间</th>' +
      ' <th>库存/存量</th>' +
      ' <th>运费</th>' +
      ' <th>操作人</th>' +
      ' <th></th>' +
      ' </thead> '
    )

  }

  function getData() {
    let seat = $('#seatStock').val();
    let product_name  = $('#searchgoods').val();
    let datetime = $('#date2').val();
    let condation = $('#tiaojian').val();
    let startdate = $('.startdate').val();
    let enddate = $('.enddate').val();
    plugins.tq_page({
      elem: 'laypage1',
      url: plugins.realm() + '/stock',
      type: 'post',
      dataType: 'json',
      datas: {
        'seat': seat,
        'product_name':product_name,
        'condation':condation,
        'startdate':startdate,
        'enddate':enddate,
      },
      page: function (data) {
        console.log(data)
        layer.closeAll('loading');
        $('.layui-table').empty();
        addCount(data)
      }
    })

  }
   total()
   checkseat();
   sum();
   getData()
   





  $('#searchAction').click(function () {
    getData()
    sum();
  })


  exports('preview', {});
});