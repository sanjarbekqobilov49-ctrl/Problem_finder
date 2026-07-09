document.addEventListener('DOMContentLoaded', function() {
    function createChart(elementId, type, labels, data, label, colors) {
        const ctx = document.getElementById(elementId);
        if (!ctx) return;
        const defaultColors = [
            '#4361ee', '#3a86ff', '#4cc9f0', '#7209b7', '#f72585',
            '#e63946', '#f4a261', '#2a9d8f', '#264653', '#e76f51'
        ];
        new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: label || 'Soni',
                    data: data,
                    backgroundColor: colors || defaultColors.slice(0, data.length),
                    borderColor: colors || defaultColors.slice(0, data.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: type === 'pie' || type === 'doughnut',
                        position: 'bottom'
                    }
                },
                scales: type !== 'pie' && type !== 'doughnut' ? {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                } : undefined
            }
        });
    }

    if (typeof regionLabels !== 'undefined') {
        createChart('regionChart', 'bar', regionLabels, regionData, 'Respondentlar');
    }
    if (typeof ageLabels !== 'undefined') {
        createChart('ageChart', 'doughnut', ageLabels, ageData, 'Yosh');
    }
    if (typeof problemsLabels !== 'undefined') {
        createChart('problemsChart', 'bar', problemsLabels, problemsData, 'Muammolar');
    }
    if (typeof appsLabels !== 'undefined') {
        createChart('appsChart', 'pie', appsLabels, appsData, 'Ilovalar');
    }
    if (typeof dailyLabels !== 'undefined') {
        createChart('dailyChart', 'line', dailyLabels, dailyData, 'Kunlik');
    }
});
