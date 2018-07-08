$(function () {
    $.get('/admin_page/admin_count/', function (data) {
        if (data.code === 200){
            console.log(data.count_types);
            setCakeOption(data.count_types);
        } else {
            alert('数据获取失败');
        }
    });
    var cakeChart = echarts.init(document.getElementById('type_count'));
    function setCakeOption(data) {
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            series: [
                {
                    name:'访问来源',
                    type:'pie',
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:data
                }
            ]
        };
        cakeChart.setOption(option);
    }
    $.get('/admin_page/admin_time/',function (data) {
        if (data.code === 200){
            console.log(data.datas);
            var data1 = [];
            var data2 = [];
            var j = 0;
            for (var i=data.datas.length-1; i >= 0; i--){
                data1[j] = data.datas[i].value;
                data2[j] = data.datas[i].name;
                j++;
            }

            setLineOption(data1, data2);
        } else {
            alert('数据获取失败');
        }
    });
    var lineChart = echarts.init(document.getElementById('news_count'));
    // setLineOption();
    function setLineOption(data1,data2) {
        var option = {
            xAxis: {
                type: 'category',
                data: data2
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: data1,
                type: 'line'
            }]
        };
        lineChart.setOption(option);
    }
});