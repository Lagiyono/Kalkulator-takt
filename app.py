import streamlit as st

# Menyimpan kode HTML ke dalam variabel string
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kalkulator Takt Time & Target Akumulatif</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 15px;
            color: #333;
        }
        .container {
            max-width: 500px;
            margin: auto;
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            font-size: 18px;
            color: #003366;
            margin-bottom: 15px;
        }
        .takt-box {
            background: #ffeb3b;
            padding: 10px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .takt-box input {
            width: 80px;
            padding: 5px;
            font-size: 16px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #003366;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .total-row {
            font-weight: bold;
            background-color: #e9ecef;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Monitoring Target Produksi</h2>
    
    <div class="takt-box">
        <span>Takt Time (Menit):</span>
        <input type="number" id="taktInput" value="13" step="0.1" oninput="hitungTarget()">
    </div>

    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Jam Mulai - Selesai</th>
                <th>Target</th>
                <th>Akumulasi</th>
            </tr>
        </thead>
        <tbody id="tableBody">
            <!-- Data dimasukkan via JavaScript -->
        </tbody>
        <tfoot>
            <tr class="total-row">
                <td colspan="2">Total Target / OT 3 Jam</td>
                <td id="totalTarget">0</td>
                <td id="totalAkumulasi">-</td>
            </tr>
        </tfoot>
    </table>
</div>

<script>
    const scheduleData = [
        { no: 1, start: "07:30", end: "08:00", durasiMenit: 30 },
        { no: 2, start: "08:00", end: "09:00", durasiMenit: 60 },
        { no: 3, start: "09:00", end: "10:00", durasiMenit: 60 },
        { no: 4, start: "10:10", end: "11:00", durasiMenit: 50 },
        { no: 5, start: "11:00", end: "11:45", durasiMenit: 45 },
        { no: 6, start: "12:30", end: "13:00", durasiMenit: 30 },
        { no: 7, start: "13:00", end: "14:00", durasiMenit: 60 },
        { no: 8, start: "14:10", end: "15:00", durasiMenit: 50 },
        { no: 9, start: "15:00", end: "15:45", durasiMenit: 45 },
        { no: 10, start: "16:30", end: "17:00", durasiMenit: 30 },
        { no: 11, start: "17:00", end: "18:00", durasiMenit: 60 },
        { no: 12, start: "18:15", end: "19:15", durasiMenit: 60 }
    ];

    function hitungTarget() {
        const taktTime = parseFloat(document.getElementById('taktInput').value) || 1;
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = "";
        
        let totalTarget = 0;
        let akumulasi = 0;

        scheduleData.forEach((item) => {
            let targetPerJam = Math.round(item.durasiMenit / taktTime);
            if (targetPerJam < 1) targetPerJam = 1;
            
            akumulasi += targetPerJam;
            totalTarget += targetPerJam;

            let row = `<tr>
                <td>${item.no}</td>
                <td>${item.start} - ${item.end}</td>
                <td>${targetPerJam}</td>
                <td><b>${akumulasi}</b></td>
            </tr>`;
            tbody.innerHTML += row;
        });

        document.getElementById('totalTarget').innerText = totalTarget;
    }

    hitungTarget();
</script>

</body>
</html>
"""

# Merender HTML ke dalam Streamlit (atur tinggi sesuai kebutuhan, misal 650px)
st.components.v1.html(html_code, height=650, scrolling=True)
