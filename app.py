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
            margin-bottom: 10px;
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
        .shift-box {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .shift-box select {
            width: 120px;
            padding: 5px;
            font-size: 14px;
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

    <div class="shift-box">
        <span>Shift:</span>
        <select id="shiftSelect" onchange="hitungTarget()">
            <option value="Day">Day</option>
            <option value="Night">Night</option>
        </select>
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
                <td colspan="2" id="totalLabel">Total Target / OT 3 Jam</td>
                <td id="totalTarget">0</td>
                <td id="totalAkumulasi">-</td>
            </tr>
        </tfoot>
    </table>
</div>

<script>
    const dataDay = [
        { no: 1, start: "07:30", end: "08:00", durasiMenit: 30 },
        { no: 2, start: "08:00", end: "09:00", durasiMenit: 60 },
        { no: 3, start: "09:00", end: "10:00", durasiMenit: 60 },
        { no: 4, start: "10:10", end: "11:00", durasiMenit: 50 },
        { no: 5, start: "11:00", end: "11:45", durasiMenit: 45 },
        { no: 6, start: "12:30", end: "13:00", durasiMenit: 30 },
        { no: 7, start: "13:00", end: "14:00", durasiMenit: 60 },
        { no: 8, start: "14:10", end: "15:00", durasiMenit: 50 },
        { no: 9, start: "15:00", end: "15:45", durasiMenit: 45 },
        { no: 10, start: "16:30", end: "17:00", durasiMenit: 45 },
        { no: 11, start: "17:00", end: "18:00", durasiMenit: 60 },
        { no: 12, start: "18:15", end: "19:15", durasiMenit: 60 }
    ];

    const dataNight = [
        { no: 1, start: "21:15", end: "22:00", durasiMenit: 45 },
        { no: 2, start: "22:10", end: "23:00", durasiMenit: 50 },
        { no: 3, start: "23:00", end: "00:00", durasiMenit: 60 },
        { no: 4, start: "00:30", end: "01:00", durasiMenit: 30 },
        { no: 5, start: "01:00", end: "02:00", durasiMenit: 60 },
        { no: 6, start: "02:00", end: "02:30", durasiMenit: 30 },
        { no: 7, start: "02:30", end: "04:00", durasiMenit: 90 },
        { no: 8, start: "04:00", end: "04:15", durasiMenit: 15 },
        { no: 9, start: "05:00", end: "06:00", durasiMenit: 75 },
        { no: 10, start: "06:00", end: "06:15", durasiMenit: 15 }
    ];

    function hitungTarget() {
        const taktTime = parseFloat(document.getElementById('taktInput').value) || 1;
        const shift = document.getElementById('shiftSelect').value;
        const tbody = document.getElementById('tableBody');
        const totalLabel = document.getElementById('totalLabel');
        
        tbody.innerHTML = "";
        
        let scheduleData = (shift === "Day") ? dataDay : dataNight;
        let totalTarget = 0;
        let akumulasi = 0;

        scheduleData.forEach((item) => {
            // Hitung nilai asli desimal tanpa dibulatkan Math.round
            let rawTarget = item.durasiMenit / taktTime;
            
            // Akumulasi menggunakan angka desimal asli agar akurat
            akumulasi += rawTarget;
            totalTarget += rawTarget;

            // Format string dengan 1 angka di belakang koma dan ubah titik (.) jadi koma (,)
            let targetStr = rawTarget.toFixed(1).replace('.', ',');
            let akumulasiStr = akumulasi.toFixed(1).replace('.', ',');

            let row = `<tr>
                <td>${item.no}</td>
                <td>${item.start} - ${item.end}</td>
                <td>${targetStr}</td>
                <td><b>${akumulasiStr}</b></td>
            </tr>`;
            tbody.innerHTML += row;
        });

        // Tampilkan total akhir dengan format desimal (1 angka di belakang koma)
        document.getElementById('totalTarget').innerText = totalTarget.toFixed(1).replace('.', ',');
        totalLabel.innerText = (shift === "Day") ? "Total Target / OT 3 Jam" : "OT 1,5 JAM";
    }

    hitungTarget();
</script>

</body>
</html>
"""

# Merender HTML ke dalam Streamlit
st.components.v1.html(html_code, height=680, scrolling=True)
