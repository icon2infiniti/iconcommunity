type = ['', 'info', 'success', 'warning', 'danger'];

mapobj = {
    initVectorMap: function (mapData) {
        $('#worldMap').vectorMap({
            map: 'world_mill_en',
            backgroundColor: "transparent",
            zoomOnScroll: false,
            regionStyle: {
                initial: {
                    fill: '#e4e4e4',
                    "fill-opacity": 0.9,
                    stroke: 'none',
                    "stroke-width": 0,
                    "stroke-opacity": 0
                }
            },

            series: {
                regions: [{
                    values: mapData,
                    scale: ["#AAAAAA", "#444444"],
                    normalizeFunction: 'polynomial'
                }]
            },
        });
    },
};

charts = {

    initDashboardPageCharts: function (chartlabels, chartdata) {
        gradientChartOptionsConfigurationWithTooltipICON = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                callbacks: {
                    label: function (tooltipItems, data) {
                        return data.datasets[tooltipItems.datasetIndex].label + ': ' + data.datasets[0].data[tooltipItems.index].toLocaleString();
                    }
                }
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.0)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 60,
                        suggestedMax: 125,
                        padding: 20,
                        fontColor: "#9a9a9a",
                        stepSize: 100000,
                        callback: function (value) {
                            var ranges = [
                                {divider: 1e6, suffix: 'M'},
                                {divider: 1e3, suffix: 'k'}
                            ];

                            function formatNumber(n) {
                                for (var i = 0; i < ranges.length; i++) {
                                    if (n >= ranges[i].divider) {
                                        return (n / ranges[i].divider).toString() + ranges[i].suffix;
                                    }
                                }
                                return n;
                            }

                            return formatNumber(value);
                        }
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(26,170,186,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9a9a9a"
                    }
                }]
            }
        };
        var chart_labels = chartlabels.slice(-30);
        var chart_data = chartdata.slice(-30);
        var ctx = document.getElementById("dailyTx").getContext('2d');
        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
        gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        var config = {
            type: 'line',
            data: {
                labels: chart_labels,
                datasets: [{
                    label: "Daily Transactions",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#1aaaba',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#1aaaba',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#1aaaba',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: chart_data.slice(-30),
                }]
            },
            options: gradientChartOptionsConfigurationWithTooltipICON
        };
        var myChartData = new Chart(ctx, config);
        $("#0").click(function () {
            var data = myChartData.config.data;
            data.datasets[0].data = chart_data.slice(-7);
            data.labels = chart_labels.slice(-7);
            myChartData.update();
        });
        $("#1").click(function () {
            var data = myChartData.config.data;
            data.datasets[0].data = chart_data.slice(-14);
            data.labels = chart_labels.slice(-14);
            myChartData.update();
        });
        $("#2").click(function () {
            var data = myChartData.config.data;
            data.datasets[0].data = chart_data.slice(-30);
            data.labels = chart_labels.slice(-30);
            myChartData.update();
        });
    },

    initWalletCharts: function (ret20) {
        console.log(ret20);
        Highcharts.chart('top20wallets', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                backgroundColor: null,
                margin: 0,
                marginBottom: 0,
                spacing: "[0,0,0,0]",
            },
            title: {
                text: null,
            },
            tooltip: {
                useHTML: true,
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b><br>Balance: {point.tokens:,.0f}',
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    innerSize: 100,
                    depth: 45,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: null, //'#333333',
                        format: '<b><a href="https://tracker.icon.foundation/address/{point.name}" target="_blank">{point.name}</a></b>',
                        style: {
                            textOutline: false
                        }
                    }
                }
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'Percent',
                colorByPoint: true,
                data: ret20,
                innerSize: '40%'
            }]
        });
        Highcharts.setOptions({
            lang: {
                thousandsSep: ','
            }
        })
    },

    initWalletCountChart: function (selectDates, balanceCounts, totalCounts) {
        // Wallet Count (Multi Bar Chart)
        gradientBarChartConfiguration = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                callbacks: {
                    label: function (tooltipItems, data) {
                        if (tooltipItems.datasetIndex === 0)
                            return data.datasets[tooltipItems.datasetIndex].label + ': ' + data.datasets[0].data[tooltipItems.index].toLocaleString();
                        else if (tooltipItems.datasetIndex === 1)
                            return data.datasets[tooltipItems.datasetIndex].label + ': ' + data.datasets[1].data[tooltipItems.index].toLocaleString();
                    }
                }
            },
            responsive: true,
            scales: {
                yAxes: [{

                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 60,
                        suggestedMax: 120,
                        padding: 20,
                        fontColor: "#9e9e9e",
                        stepSize: 100000,
                        callback: function (value) {
                            var ranges = [
                                {divider: 1e6, suffix: 'M'},
                                {divider: 1e3, suffix: 'k'}
                            ];

                            function formatNumber(n) {
                                for (var i = 0; i < ranges.length; i++) {
                                    if (n >= ranges[i].divider) {
                                        return (n / ranges[i].divider).toString() + ranges[i].suffix;
                                    }
                                }
                                return n;
                            }

                            return formatNumber(value);
                        }
                    }
                }],

                xAxes: [{

                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9e9e9e",
                    }
                }]
            }
        };
        var ctx = document.getElementById("WalletCountChart").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
        gradientStroke.addColorStop(1, 'rgba(253,93,147,0.8)');
        gradientStroke.addColorStop(0, 'rgba(253,93,147,0)'); //blue colors

        var gradientStroke2 = ctx.createLinearGradient(0, 230, 0, 50);
        gradientStroke2.addColorStop(1, 'rgba(26,170,186,0.8)');
        gradientStroke2.addColorStop(0, 'rgba(0,0,0,0)'); //white colors

        var walletChartData = new Chart(ctx, {
            type: 'bar',
            responsive: true,
            data: {
                labels: selectDates.slice(-30),
                datasets: [{
                    label: "Has Balance Wallets",
                    fill: true,
                    backgroundColor: gradientStroke,
                    hoverBackgroundColor: gradientStroke,
                    borderColor: '#ff8a76',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    data: balanceCounts.slice(-30),
                },
                    {
                        label: "Total Wallets",
                        fill: true,
                        backgroundColor: gradientStroke2,
                        hoverBackgroundColor: gradientStroke2,
                        borderColor: '#098186',
                        borderWidth: 2,
                        borderDash: [],
                        borderDashOffset: 0.0,
                        data: totalCounts.slice(-30),
                    }]
            },
            options: gradientBarChartConfiguration
        });
        $("#wc0").click(function () {
            var data = walletChartData.config.data;
            data.datasets[0].data = balanceCounts.slice(-7);
            data.datasets[1].data = totalCounts.slice(-7);
            data.labels = selectDates.slice(-7);
            walletChartData.update();
        });
        $("#wc1").click(function () {
            var data = walletChartData.config.data;
            data.datasets[0].data = balanceCounts.slice(-14);
            data.datasets[1].data = totalCounts.slice(-14);
            data.labels = selectDates.slice(-14);
            walletChartData.update();
        });
        $("#wc2").click(function () {
            var data = walletChartData.config.data;
            data.datasets[0].data = balanceCounts.slice(-30);
            data.datasets[1].data = totalCounts.slice(-30);
            data.labels = selectDates.slice(-30);
            walletChartData.update();
        });
    },

    initRewardRateChart: function (inflation, reward, realyield, dates) {

        gradientChartOptionsConfigurationWithTooltipPurple = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                callbacks: {
                    label: function (tooltipItem, data) {
                        return Chart.defaults.global.tooltips.callbacks.label(tooltipItem, data) + '%';
                    }
                }
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.0)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 8,
                        suggestedMax: 14,
                        padding: 20,
                        fontColor: "#9a9a9a"
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(225,78,202,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9a9a9a"
                    }
                }]
            }
        };

        var ctx = document.getElementById("RewardRate").getContext("2d");
        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
        gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

        var data = {
            labels: dates.slice(-30),
            datasets: [
                {
                    label: "Real Yield",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#d048b6',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#d048b6',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#d048b6',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: realyield.slice(-30),
                },
                /*
                {
                    label: "Annual Inflation",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#d048b6',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#d048b6',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#d048b6',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    //data: [80, 100, 70, 80, 120, 80],
                    data: inflation,
                },
                {
                    label: "Annual Reward",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#3d7437',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#3d7437',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#3d7437',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    //data: [1, 2, 3, 7, 80, 90],
                    data: reward,
                }
                */
            ]
        };

        var rrChart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipPurple
        });

        $("#rr0").click(function () {
            var data = rrChart.config.data;
            data.datasets[0].data = realyield.slice(-7);
            data.labels = dates.slice(-7);
            rrChart.update();
        });
        $("#rr1").click(function () {
            var data = rrChart.config.data;
            data.datasets[0].data = realyield.slice(-14);
            data.labels = dates.slice(-14);
            rrChart.update();
        });
        $("#rr2").click(function () {
            var data = rrChart.config.data;
            data.datasets[0].data = realyield.slice(-30);
            data.labels = dates.slice(-30);
            rrChart.update();
        });
    },

    initTopDappsChart: function (dapps_create_day_list, daolette_txLastDay, daodice_txLastDay, stayge_txLastDay, somesing_txLastDay, daolette_volumeLastDayInUSD, daodice_volumeLastDayInUSD, stayge_volumeLastDayInUSD, somesing_volumeLastDayInUSD, daolette_dauLastDay, daodice_dauLastDay, stayge_dauLastDay, somesing_dauLastDay) {

        gradientChartOptionsConfigurationPurple = {
            maintainAspectRatio: false,
            legend: {
                display: true,
                labels: {
                    fontColor: '#9A9A9A'
                }
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                callbacks: {
                    label: function (tooltipItems, data) {
                        return data.datasets[tooltipItems.datasetIndex].label;
                    },
                    afterBody: function(tooltipItems, data){
                        //return data.datasets[tooltipItems.datasetIndex].label + ': ' + data.datasets[0].data[tooltipItems.index].toLocaleString();
                        //return d.datasets[t.datasetIndex].label;
                        var currentLabel = data.datasets[tooltipItems[0].datasetIndex].label;
                        if(currentLabel == 'ICONBet - DAOdice'){
                            var multistringText = ['Transactions: ' + daodice_txLastDay[tooltipItems[0].index].toLocaleString()];
                            multistringText.push(('USD Volume: $' + Math.round(daodice_volumeLastDayInUSD[tooltipItems[0].index]).toLocaleString()));
                            multistringText.push(('DAU: '+daodice_dauLastDay[tooltipItems[0].index]).toLocaleString());
                            return multistringText;
                        }
                        if(currentLabel == 'ICONBet - DAOlette') {
                            var multistringText = ['Transactions: ' + daolette_txLastDay[tooltipItems[0].index].toLocaleString()];
                            multistringText.push('USD Volume: $' + Math.round(daolette_volumeLastDayInUSD[tooltipItems[0].index]).toLocaleString());
                            multistringText.push(('DAU: ' + daolette_dauLastDay[tooltipItems[0].index]).toLocaleString());
                            return multistringText;
                        }
                        if(currentLabel == 'Stayge') {
                            var multistringText = ['Transactions: ' + stayge_txLastDay[tooltipItems[0].index].toLocaleString()];
                            multistringText.push('USD Volume: $' + Math.round(stayge_volumeLastDayInUSD[tooltipItems[0].index]).toLocaleString());
                            multistringText.push(('DAU: ' + stayge_dauLastDay[tooltipItems[0].index]).toLocaleString());
                            return multistringText;
                        }
                        if(currentLabel == 'Somesing') {
                            var multistringText = ['Transactions: ' + somesing_txLastDay[tooltipItems[0].index].toLocaleString()];
                            multistringText.push('USD Volume: $' + Math.round(somesing_volumeLastDayInUSD[tooltipItems[0].index]).toLocaleString());
                            multistringText.push(('DAU: ' + somesing_dauLastDay[tooltipItems[0].index]).toLocaleString());
                            return multistringText;
                        }


                        //return data.datasets[tooltipItems[0].datasetIndex].label;//tooltipItems[0].index;
                    }
                }
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(186,84,245,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 125,
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(186,84,245,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }]
            }
        };

        var ctx = document.getElementById("topdapps").getContext("2d");
        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        var dAppChartData = new Chart(ctx, {
            type: 'line',
            responsive: true,
            data: {
                labels: dapps_create_day_list,
                datasets: [
                {
                    label: "ICONBet - DAOlette",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#2380f7',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#2380f7',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#2380f7',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: daolette_txLastDay,
                },
                {
                    label: "ICONBet - DAOdice",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#be55ed',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#be55ed',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#be55ed',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: daodice_txLastDay,
                },
                {
                    label: "Somesing",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#ef4123',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#ef4123',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#ef4123',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: somesing_txLastDay,
                },
                {
                    label: "Stayge",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#44495d',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#44495d',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#44495d',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: stayge_txLastDay,
                },
                ]
            },
            options: gradientChartOptionsConfigurationPurple
        });
        $("#td0").click(function () {
            var data = dAppChartData.config.data;
            data.labels = dapps_create_day_list.slice(-7);
            data.datasets[0].data = daolette_txLastDay.slice(-7);
            data.datasets[1].data = daodice_txLastDay.slice(-7);
            data.datasets[2].data = somesing_txLastDay.slice(-7);
            data.datasets[3].data = stayge_txLastDay.slice(-7);
            dAppChartData.update();
        });
        $("#td1").click(function () {
            var data = dAppChartData.config.data;
            data.labels = dapps_create_day_list.slice(-14);
            data.datasets[0].data = daolette_txLastDay.slice(-14);
            data.datasets[1].data = daodice_txLastDay.slice(-14);
            data.datasets[2].data = somesing_txLastDay.slice(-14);
            data.datasets[3].data = stayge_txLastDay.slice(-14);
            dAppChartData.update();
        });
        $("#td2").click(function () {
            var data = dAppChartData.config.data;
            data.labels = dapps_create_day_list.slice(-30);
            data.datasets[0].data = daolette_txLastDay.slice(-30);
            data.datasets[1].data = daodice_txLastDay.slice(-30);
            data.datasets[2].data = somesing_txLastDay.slice(-30);
            data.datasets[3].data = stayge_txLastDay.slice(-30);
            dAppChartData.update();
        });
    },
};

function showmain() {
    $('#ranking_all').hide();
    $('#ranking_sub').hide();
    $('#ranking_main').show();
}

function showsub() {
    $('#ranking_all').hide();
    $('#ranking_sub').show();
    $('#ranking_main').hide();
}

function showall() {
    $('#ranking_all').show();
    $('#ranking_sub').hide();
    $('#ranking_main').hide();
}



