function initializeChart(dates, navs, schemeName) {
    const ctx = document.getElementById('fundChart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates.reverse(),
            datasets: [{
                label: `${schemeName} - Fund NAV`,
                data: navs.reverse(),
                borderColor: 'rgba(0, 128, 0, 1)',
                backgroundColor: 'rgba(0, 128, 0, 0.2)',
                borderWidth: 0.3,
                fill: true,
                pointRadius: 1,
                pointHoverRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: false, text: 'Year' },
                    ticks: { autoSkip: true, maxTicksLimit: 5 }
                },
                y: {
                    title: { display: true, text: 'NAV' },
                    beginAtZero: true,
                }
            },
            plugins: {
                legend: { display: true, position: 'top' ,onClick: (e) => e.stopPropagation()},
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                }
            }
        }
    });
}
document.addEventListener("DOMContentLoaded", function() {
    const dates = JSON.parse(document.getElementById('datesData').textContent);
    const navs = JSON.parse(document.getElementById('navsData').textContent);
    const schemeName = document.getElementById('schemeNameData').textContent;
    initializeChart(dates, navs, schemeName);
});
