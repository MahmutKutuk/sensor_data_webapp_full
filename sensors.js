async function loadLatest() {
    const res = await fetch('/api/sensors');
    const data = await res.json();
    const tbody = document.querySelector('#latest tbody');
    tbody.innerHTML = '';
    data.forEach(d => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${d.sensor_type}</td><td>${d.value}</td><td>${d.date}</td>`;
        tbody.appendChild(tr);
    });
}

async function loadTable(sensor='') {
    const url = sensor ? '/api/data?sensor='+sensor : '/api/data';
    const res = await fetch(url);
    const rows = await res.json();
    const tbody = document.querySelector('#sensorTable tbody');
    tbody.innerHTML = '';
    rows.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${r.id}</td><td>${r.sensor_type}</td><td>${r.value}</td><td>${r.date}</td>`;
        tbody.appendChild(tr);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#latest')) loadLatest();
    if(document.querySelector('#sensorTable')) loadTable();

    const applyBtn = document.getElementById('apply-filter');
    if(applyBtn) {
        applyBtn.addEventListener('click', () => {
            const sensor = document.getElementById('filter-sensor').value;
            loadTable(sensor);
        });
    }
});
