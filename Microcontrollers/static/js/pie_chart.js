$(function () {
	$('#container').highcharts({
	chart: {
	    plotBackgroundColor: 'rgba(224,224,224,0.0)',
	    backgroundColor: 'rgba(224,224,224,0.0)',
	    plotBorderWidth: null,
	    plotShadow: false,
	    type: 'pie',
	    options3d: {
	        enabled: true,
	        alpha: 45,
	        beta: 0,
	    }
	},
	credits: {
		enabled: false,
	},
	title: {
	    text: 'Gateway Uptime for ' + new Date().toDateString(),
	},
	tooltip: {
	    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	},
	plotOptions: {
	    pie: {
	        allowPointSelect: true,
	        cursor: 'pointer',
	        depth: 35,
	        dataLabels: {
	            enabled: true,
	            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
	            style: {
	                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
	            }
	        },
	    }
	},
	series: [{
	    name: "Gateway Availability",
	    colorByPoint: true,
	    data: [{
	        name: "Online",
	        y: {{ uptime }}
	    }, {
	    	name: "Offline",
        	y: {{ downtime }},
            }]
        }]
    });
});