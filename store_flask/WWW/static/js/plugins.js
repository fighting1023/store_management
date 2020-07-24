const plugins = {
  // ajax接口统一部分
  "realm": function () {
    let realm = 'http://47.105.91.77:5000'
    return realm;
  },
  "hqstock":"怀柔",
  "zkstock":"中科院",
  //  // 登录页面设置
  // "index": function () {
  //   let index = 'http://152.136.18.170/audit_static/'
  //   return index;
  // },

  
  //解析url
  "GetRequest": function () {
    var url = decodeURI(location.search); //获取url中"?"符后的字串   
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for (var i = 0; i < strs.length; i++) {
        theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
      }
    }
    return theRequest;
  },
  /**
   * ajax封装
   */
  "AjaxPlugin": function (option) {

       var formData =new FormData();
       var arr = option.data;
       for(var key in arr){
        formData.append(key, arr[key]);
       }

    $.ajax({
      url: option.url,
      type: option.type,
      dataType: 'json',
      data: formData,
      cache: false,        // 不缓存数据
      processData: false,  // 不处理数据
      contentType: false,   // 不设置内容类型
      async: option.async || true,
      success: function (data) {
        
        // console.log(data)
      
        if (data.code == 200) {

          option.action(data)
        }else if(data.cod == 401){
          window.parent.location.href = '../../html/login.html'
        }
        else {
          option.othererro(data)
        }

      },
      erro: function (data) {
        alert('系统出错，请稍等');
      }

    })
  },
 
  //获取当前时间
  "getDay": function () {
    var date = new Date();
    var seperator1 = "-";
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
      month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
      strDate = "0" + strDate;
    }
    var currentdate = year + seperator1 + month + seperator1 + strDate;
    return currentdate
  },
  // 获取前几天(后几天)的日期
  "fun_date": function (num) {
    var o1 ="" ;
    var o2 ="";
    var date1 = new Date(),
      time1 = date1.getFullYear() + "-" + (date1.getMonth() + 1) + "-" + date1.getDate(); //time1表示当前时间
    var date2 = new Date(date1);
    date2.setDate(date1.getDate() + num);
    if(date2.getMonth() + 1<10){
      o1 = "0";
    }
    if(date2.getDate()<10){
      o2 = "0";
    }
    var time2 = date2.getFullYear() + "-" + o1 +(date2.getMonth() + 1) + "-" + o2 + date2.getDate();
    return time2;
  },

  'tq_page': function (option) {
    // 合并对象
    function extend(target, source) {
      for (var obj in source) {
        target[obj] = source[obj];
      }
      return target; 
    }
    var page1 = {
      'page': 1,
      'perPage': 10
    }
    var pagedatas = extend(page1, option.datas);
    // plugins.console(pagedatas)
    layer.load(2);
    plugins.AjaxPlugin({
      url: option.url,
      type: 'post',
      data: pagedatas,
      dataType: 'json',
      action: function (data) {
        console.log(data)
        layer.closeAll('loading');
        option.page(data)
        layui.use('laypage', function () {
          var laypage = layui.laypage;
          //执行一个laypage实例
          laypage.render({
            elem: option.elem,
            count: data.data.pageCount,
            layout: ['count', 'prev', 'page', 'next', 'limit', 'skip'],
            jump: function (obj, first) {
              // option.obj(obj)

              if (!first) {
                layer.load(2);
                var page2 = {
                  'page': obj.curr,
                  'perPage': obj.limit
                }
                var pagedatas2 = extend(page2, option.datas);

                // plugins.console(pagedatas2)
                plugins.AjaxPlugin({
                  url: option.url,
                  type: 'post',
                  data: pagedatas2,
                  dataType: 'json',

                  action: function (data) {
                    layer.closeAll('loading');

                    option.page(data);
                  },

                });
              }
            }
          });
        });
      }
    })
  },

  //处理后台传过来的文件流下载
  // filedata是一个对象参数

  //plugins.fileDownload({       
  //   url:plugins.realm()+'bill_service/pay-down',
  //   type:'post',
  //   filename:'download.xls',
  //   data:{'appid':$('#searchgoods').val(),
  //         'period':$('#date3').val()
  //      }
  // })
  // 只有是Post的时候才会有参数  plugin.
  'fileDownload': function (filedata) {

    var oReq = new XMLHttpRequest();
    oReq.open(filedata.type, filedata.url, true);
    oReq.responseType = "blob";
    oReq.onload = function (oEvent) {
      var content = oReq.response;

      var elink = document.createElement('a');
      elink.download = filedata.
      filename;
      elink.style.display = 'none';

      var blob = new Blob([content]);
      elink.href = URL.createObjectURL(blob);

      document.body.appendChild(elink);
      elink.click();

      document.body.removeChild(elink);
    };
    if (filedata.data) {
      var formData = new FormData();
      var datas = filedata.data;
      for (var index in datas) {
        formData.append(index, datas[index]);
      }
      oReq.send(formData);
    } else {
      oReq.send();
    }

  },

  // 秒数转换为 时分秒
  'formatSeconds': function (value) {
    var secondTime = parseInt(value); // 秒
    var minuteTime = 0; // 分
    var hourTime = 0; // 小时
    var day = 0; // 小时
    if (secondTime > 60) { //如果秒数大于60，将秒数转换成整数
      //获取分钟，除以60取整数，得到整数分钟
      minuteTime = parseInt(secondTime / 60);
      //获取秒数，秒数取佘，得到整数秒数
      secondTime = parseInt(secondTime % 60);
      //如果分钟大于60，将分钟转换成小时
      if (minuteTime > 60) {
        //获取小时，获取分钟除以60，得到整数小时
        hourTime = parseInt(minuteTime / 60);
        //获取小时后取佘的分，获取分钟除以60取佘的分
        minuteTime = parseInt(minuteTime % 60);

        if (hourTime > 24) {
          day = parseInt(hourTime / 24)
          hourTime = parseInt(hourTime % 24)
        }
      }
     
    }
    var result = "" + parseInt(secondTime) + "秒";

    if (minuteTime > 0) {
      result = "" + parseInt(minuteTime) + "分" + result;
    }
    if (hourTime > 0) {
      result = "" + parseInt(hourTime) + "小时" + result;
    }
    if (day > 0) {
      result = "" + parseInt(day) + "天" + result;
    }
    return result;
  }



}


//调用 plugins.名字(参数)
