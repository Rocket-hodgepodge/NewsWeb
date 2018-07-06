$(function () {
    $.get('/admin_page/admin_count/', function (data) {
        if (data.code === 200){
            console.log(data.count_types);
            setMyOption(data.count_types);
        } else {
            alert('数据获取失败');
        }
    });
    var myChart = echarts.init(document.getElementById('type_count'));
    function setMyOption(data) {
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
        myChart.setOption(option);
    }

});