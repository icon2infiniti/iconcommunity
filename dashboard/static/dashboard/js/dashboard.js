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
                position: "nearest"
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
                        callback: function(value) {
                            var ranges = [
                                { divider: 1e6, suffix: 'M' },
                                { divider: 1e3, suffix: 'k' }
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

        //var chart_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        //var chart_data = [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100];
        var chart_labels = chartlabels;
        var chart_data = chartdata;
        var ctx = document.getElementById("chartBig1").getContext('2d');
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
                    data: chart_data,
                }]
            },
            options: gradientChartOptionsConfigurationWithTooltipICON
        };
        var myChartData = new Chart(ctx, config);
    },

};