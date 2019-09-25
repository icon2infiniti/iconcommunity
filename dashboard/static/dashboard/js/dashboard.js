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

function showmain(){
    $('#ranking_all').hide();
    $('#ranking_sub').hide();
    $('#ranking_main').show();
}

function showsub(){
    $('#ranking_all').hide();
    $('#ranking_sub').show();
    $('#ranking_main').hide();
}

function showall(){
    $('#ranking_all').show();
    $('#ranking_sub').hide();
    $('#ranking_main').hide();
}