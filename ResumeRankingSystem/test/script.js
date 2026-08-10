document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Simulate Scan Process
    alert('Scanning in progress...');

    // Simulated JSON Data
    const jsonData = [
        {
            "Category": "Machine Learning/AI",
            "Name": "Balaji O",
            "Position": "Staff Software Engineer",
            "Rank": "1"
        },
        {
            "Category": "Data Engineer",
            "Name": "Jeevankumar O",
            "Position": "Data Engineer",
            "Rank": "2"
        }
    ];

    // Display the Table
    displayTable(jsonData);
});

function displayTable(data) {
    const resultTable = document.getElementById('resultTable');
    resultTable.innerHTML = '';

    if (data.length === 0) {
        resultTable.innerHTML = '<p>No data available.</p>';
        return;
    }

    // Create Table
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Create Table Header
    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Create Table Body
    data.forEach(item => {
        const row = document.createElement('tr');
        Object.values(item).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    resultTable.appendChild(table);

    // Show the Table
    resultTable.classList.remove('hidden');
}
