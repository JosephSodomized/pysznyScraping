<?php
    $conn = new mysqli('localhost', 'root', '', '31775790_etl');
        if (mysqli_connect_errno())
            {
                echo 'Nie powiodła się próba połączenia z bazą danych.';
            }
    mysqli_set_charset($conn,'utf8');
    $query = ('TRUNCATE TABLE info');
    mysqli_query($conn, $query);

    header('Location: result.php')


 ?>