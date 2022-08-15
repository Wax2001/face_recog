

// Dashboard 1 Morris-chart

Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2020',
            employees: 0,
            reports: 0,
            avg_work_hours: 0,
            avg_hourly_rate: 0,
        }, {
            period: '2021',
            employees: 1,
            reports: 2,
            avg_work_hours: 18,
            avg_hourly_rate: 4,
        }, {
            period: '2022',
            employees: 1,
            reports: 5,
            avg_work_hours: 3,
            avg_hourly_rate: 4,
        },
        {
            period: '2023',
            employees: 2,
            reports: 16,
            avg_work_hours: 23,
            avg_hourly_rate: 12,
        },],
        
        xkey: 'period',
        ykeys: ['employees', 'reports', 'avg_work_hours', 'avg_hourly_rate'],
        labels: ['Employees', 'Reports', 'Average Worked Hours', 'Average Hourly Rate'],
        pointSize: 0,
        fillOpacity: 0.9,
        pointStrokeColors:['#e7e8ef', '#51e4ff', '#16198d', '#1155c2', '#d1c517'],
        behaveLikeLine: true,
        gridLineColor: '#eef0f2',
        lineWidth: 0,
        hideHover: 'auto',
        lineColors: ['#e7e8ef', '#51e4ff', '#16198d', '#1155c2', '#d1c517'],
        resize: true
        
    });

 $('.vcarousel').carousel({
            interval: 3000
         })