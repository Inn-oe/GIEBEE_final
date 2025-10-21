// @ts-nocheck
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('locationChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: chartData,
        options: chartOptions
    });
});
