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
            title: {
                text: '新闻类型占比',
                x: 'center'
            },
            series: [
                {
                    name:'新闻类型',
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
    function setLineOption(data1,data2) {
        var option = {
            xAxis: {
                type: 'category',
                data: data2
            },
            yAxis: {
                type: 'value'
            },
            title: {
                text: '近五日新闻数量',
                x: 'center'
            },
            series: [{
                data: data1,
                type: 'line'
            }]
        };
        lineChart.setOption(option);
    }
    $.get('/admin_page/admin_users/',function (data) {
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

            setUserOption(data1, data2);
        } else {
            alert('数据获取失败');
        }
    });
    var userChart = echarts.init(document.getElementById('active_user'));
    function setUserOption(data1,data2) {
        var option = {
            color: ['#3398DB'],
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },

            xAxis : [
                {
                    type : 'category',
                    data : data2,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            title: {
                text: '近五日活跃用户量',
                x: 'center'
            },
            yAxis : [
                {
                    type : 'value'
                }
            ],
            series : [
                {
                    name:'访问用户数',
                    type:'bar',
                    barWidth: '60%',
                    data:data1,
                }
            ]
        };
        userChart.setOption(option);
    }
    $.get('/admin_page/admin_numbers/',function (data) {
        if (data.code === 200){
            console.log(data.name,data.value);
            setNumberOption(data.name,data.value);
        } else {
            alert('数据获取失败');
        }
    });
    var numberChart = echarts.init(document.getElementById('web_user'));
    function setNumberOption(name,value) {
        var option = {
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: name,
            },
            yAxis: {
                type: 'value'
            },
            title: {
                text: '近五日网站访问量',
                x: 'center'
            },
            series: [{
                data: value,
                type: 'line',
                areaStyle: {}
            }]
        };

        numberChart.setOption(option);
    }
});