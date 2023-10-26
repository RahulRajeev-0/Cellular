// (function ($) {
//     "use strict";


//     // Assuming you have imported Chart.js library and defined your chart configurations.

// // Get the canvas elements
// var weeklyChartCanvas = document.getElementById('weeklyChart');
// var monthlyChartCanvas = document.getElementById('monthlyChart');
// var yearlyChartCanvas = document.getElementById('yearlyChart');

// if (weeklyChartCanvas && monthlyChartCanvas && yearlyChartCanvas) {
//     var weeklyChart = new Chart(weeklyChartCanvas.getContext('2d'), {
//         // Your chart configuration here
//         // ...
//         data: {
//             labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
//             datasets: [{
//                 label: 'Weekly Sales',
//                 data: [1,2,3,4], // Use the data returned by get_weekly_sales()
//                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
//                 borderColor: 'rgba(44, 120, 220)',
//             }]
//         },
//         // ...
//     });

//     var monthlyChart = new Chart(monthlyChartCanvas.getContext('2d'), {
//         // Your chart configuration here
//         // ...
//         data: {
//             labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
//             datasets: [{
//                 label: 'Monthly Sales',
//                 data: [monthly_sales_data], // Use the data returned by get_monthly_sales()
//                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
//                 borderColor: 'rgba(44, 120, 220)',
//             }]
//         },
//         // ...
//     });

//     var yearlyChart = new Chart(yearlyChartCanvas.getContext('2d'), {
//         // Your chart configuration here
//         // ...
//         data: {
//             labels: ['2022', '2023'],
//             datasets: [{
//                 label: 'Yearly Sales',
//                 data: [yearly_sales_data], // Use the data returned by get_yearly_sales()
//                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
//                 borderColor: 'rgba(44, 120, 220)',
//             }]
//         },
//         // ...
//     });
// }



async function getSalesReport() {
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: 'http://127.0.0.1:8000/sales-report/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}






// })(jQuery);





(function ($) {
    "use strict";

    /*Sale statistics Chart*/
    if ($('#myChart').length) {


        var ctx = document.getElementById('myChart').getContext('2d');


        //getting data
        getSalesReport()
            .then(function(data) {
                console.log(data);
                // Do something with the data
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
        //parsing the data

        
        async function drawChart() {
            const salesData = await getSalesReport();
        
            const ctx = document.getElementById('myChart').getContext('2d');
        
            
            const productNames = salesData.weekly_sales.map(item => item.product__product_heading);
            const weeklySales = salesData.weekly_sales.map(item => item.weekly_sales);
            const monthlySales = salesData.monthly_sales.map(item => item.monthly_sales);
            const yearlySales = salesData.yearly_sales.map(item => item.yearly_sales);
            
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: productNames,
                    datasets: [
                        {
                            label: 'Weekly Sales',
                            data: weeklySales,
                            backgroundColor: 'rgba(44, 120, 220, 0.2)',
                            borderColor: 'rgba(44, 120, 220)',
                        },
                        {
                            label: 'Monthly Sales',
                            data: monthlySales,
                            backgroundColor: 'rgba(4, 209, 130, 0.2)',
                            borderColor: 'rgb(4, 209, 130)',
                        },
                        {
                            label: 'Yearly Sales',
                            data: yearlySales,
                            backgroundColor: 'rgba(380, 200, 230, 0.2)',
                            borderColor: 'rgb(380, 200, 230)',
                        }
                    ]
                },
                options: {
                    plugins: {
                        legend: {
                            labels: {
                                usePointStyle: true,
                            },
                        }
                    }
                }
            });
        }
        
        drawChart();





        // var chart = new Chart(ctx, {
        //     // The type of chart we want to create
        //     type: 'line',
            
        //     // The data for our dataset
        //     data: {
        //         labels: ['product1', 'product2', 'product3', 'product4'],
        //         datasets: [{
        //                 label: 'Weekly Sales',
        //                 tension: 0.3,
        //                 fill: true,
        //                 backgroundColor: 'rgba(44, 120, 220, 0.2)',
        //                 borderColor: 'rgba(44, 120, 220)',
        //                 data: [18, 17, 4, 3]
        //             },
        //             {
        //                 label: 'Monthly ',
        //                 tension: 0.3,
        //                 fill: true,
        //                 backgroundColor: 'rgba(4, 209, 130, 0.2)',
        //                 borderColor: 'rgb(4, 209, 130)',
        //                 data: [40, 20, 17, 9,]
        //             },
        //             {
        //                 label: 'Yearly',
        //                 tension: 0.3,
        //                 fill: true,
        //                 backgroundColor: 'rgba(380, 200, 230, 0.2)',
        //                 borderColor: 'rgb(380, 200, 230)',
        //                 data: [30, 10, 27, 19,]
        //             }

        //         ]
        //     },
        //     options: {
        //         plugins: {
        //         legend: {
        //             labels: {
        //             usePointStyle: true,
        //             },
        //         }
        //         }
        //     }
        // });

        
    } //End if



    /*Sale statistics Chart*/
    if ($('#myChart2').length) {
        var ctx = document.getElementById("myChart2");
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
            labels: ["900", "1200", "1400", "1600"],
            datasets: [
                {
                    label: "US",
                    backgroundColor: "#5897fb",
                    barThickness:10,
                    data: [233,321,783,900]
                }, 
                {
                    label: "Europe",
                    backgroundColor: "#7bcf86",
                    barThickness:10,
                    data: [408,547,675,734]
                },
                {
                    label: "Asian",
                    backgroundColor: "#ff9076",
                    barThickness:10,
                    data: [208,447,575,634]
                },
                {
                    label: "Africa",
                    backgroundColor: "#d595e5",
                    barThickness:10,
                    data: [123,345,122,302]
                },
            ]
            },
            options: {
                plugins: {
                    legend: {
                        labels: {
                        usePointStyle: true,
                        },
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } //end if
    
})(jQuery);