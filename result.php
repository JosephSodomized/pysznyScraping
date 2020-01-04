<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pyszne.etl</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">

    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script src="js/index.js"></script>
    <script>
        function downloadCSV(csv, fileName) {
            var csvFile;
            var downloadLink;

            csvFile = new Blob([csv], {type: "text/csv"});
            downloadLink = document.createElement("a");
            downloadLink.download = fileName;
            downloadLink.href = window.URL.createObjectURL(csvFile);
            downloadLink.style.display = "none";
            document.body.appendChild(downloadLink);
            downloadLink.click();
        }
        function exportToCSV(filename) {
            var csv = [];
            var rows = document.querySelectorAll("table tr");

            for (var i = 0; i < rows.length; i++) {
                var row = [], cols = rows[i].querySelectorAll("td, th");

                for (var j = 0; j < cols.length; j++)
                    row.push(cols[j].innerText);

                csv.push(row.join(";"));
            }
            downloadCSV(csv.join("\n"), filename);
        }
    </script>
</head>
<body style="background-color: #ffbf80">

<div class="container" style="margin-top: 20px">
    <div class="row">
        <div class="row">

            <table class="table table-bordered table-hover">
                <thead style="background-color:white">
                <tr>
                    <td>Nazwa restauracji</td>
                    <td>Rodzaj kuchni</td>
                    <td>Liczba recenzji</td>
                    <td>Średni czas dostawy (minuty)</td>
                    <td>Koszt dostawy (zł)</td>
                    <td>Zamówienie minimalne (zł)</td>
                    <td>Ocena</td>
                    <td>Ostatnia recenzja</td>
                </tr>
                </thead>
                <tbody>
                <?php
                $conn = new mysqli('localhost', 'root', '', '31775790_etl');
                $sql = $conn->query('SELECT * FROM info GROUP BY title HAVING COUNT(*) >= 1');

                while($data = $sql->fetch_array()) {


                    echo '
                                    <tr>
                                        <td>'.$data['title'].'</td>
                                        <td>'.$data['kitchen'].'</td>
                                        <td>'.$data['review_count'].'</td>
                                        <td>'.$data['average_delivery_time'].'</td>
                                        <td>'.$data['delivery_cost'].'</td>
                                        <td>'.$data['minimum_order'].'</td>
                                        <td>'.$data['rating_number'].'</td>
                                        <td>'.$data['last_written_review'].'</td>
                                    </tr>
                                ';
                }
                ?>
                </tbody>
            </table>
        </div>
        <button onclick="exportToCSV('plik.csv')" class="m-1">Eksportuj do pliku .csv</button>
        <form action="delete.php" method="get">
            <input type="submit" value="Wyczyść dane" class="mt-1 mb-3">
        </form>

    </div>
</div>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
<script type="text/javascript">
    $(document).ready(function() {
        $(".table").DataTable({
            "ordering": true,
            "searching": true,
            "paging": false,
            "order": [[2, "desc"]],
            "language": {
                "decimal": ",",
                "thousands": ".",
                "processing":     "Przetwarzanie...",
                "search":         "Szukaj:",
                "lengthMenu":     "Pokaż _MENU_ pozycji",
                "info":           "Pozycje od _START_ do _END_ z _TOTAL_ łącznie",
                "infoEmpty":      "Pozycji 0 z 0 dostępnych",
                "infoFiltered":   "(filtrowanie spośród _MAX_ dostępnych pozycji)",
                "infoPostFix":    "",
                "loadingRecords": "Wczytywanie...",
                "zeroRecords":    "Nie znaleziono pasujących pozycji",
                "emptyTable":     "Brak danych",
                "paginate": {
                    "first":      "Pierwsza",
                    "previous":   "Poprzednia",
                    "next":       "Następna",
                    "last":       "Ostatnia"
                },
                "aria": {
                    "sortAscending": ": aktywuj, by posortować kolumnę rosnąco",
                    "sortDescending": ": aktywuj, by posortować kolumnę malejąco"
                }
            }
        });
    });
</script>
</body>
