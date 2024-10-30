// Initialize charts using Chart.js

// Risk Assessment Chart
const riskCtx = document.getElementById('riskChart').getContext('2d');
new Chart(riskCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
            label: 'Risk Level',
            data: [12, 19, 3, 5, 2, 3, 7],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Portfolio Insights Chart
const portfolioCtx = document.getElementById('portfolioChart').getContext('2d');
new Chart(portfolioCtx, {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Portfolio Performance',
            data: [20, 25, 30, 35, 40, 45, 50],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Portfolio Funds Chart
const fundsCtx = document.getElementById('fundsChart').getContext('2d');
new Chart(fundsCtx, {
    type: 'bar',
    data: {
        labels: ['Cash', 'Equity', 'Gold', 'Currency'],
        datasets: [{
            label: 'Funds Distribution',
            data: [30, 40, 20, 10],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
            borderColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Individual Liabilities Chart
const liabilitiesCtx = document.getElementById('liabilitiesChart').getContext('2d');
new Chart(liabilitiesCtx, {
    type: 'bar',
    data: {
        labels: ['Rent', 'Utilities', 'Loans'],
        datasets: [{
            label: 'Liabilities',
            data: [1500, 500, 1200],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
