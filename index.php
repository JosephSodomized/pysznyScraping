<?php

    $conn = new mysqli('localhost', 'root', '', '31775790_etl');

    if (mysqli_connect_errno())
        {
            echo 'Nie powiodła się próba połączenia z bazą danych.';
         }
    mysqli_set_charset($conn,'utf8');
    $conn->query('CREATE TABLE IF NOT EXISTS info (id SMALLINT NOT NULL AUTO_INCREMENT, title VARCHAR(200), kitchen VARCHAR(200), review_count SMALLINT, average_delivery_time VARCHAR(200), delivery_cost VARCHAR(200), minimum_order VARCHAR(200) , rating_number FLOAT, last_written_review VARCHAR(200), PRIMARY KEY(id))');

    if(isset($_GET['ajax']))
    {

        $conn->query('DELETE FROM info');
        $process = isset($_GET['process']) ? $_GET['process'] : '';
        $postcode = isset($_GET['postcode']) ? $_GET['postcode'] : '';

        shell_exec('python '.__DIR__.'/webscraper.py '.$process.' '.$postcode);

        if ($_GET['process'] == 'processExtract')
        {
            $arrayOfRestaurantName = json_decode(file_get_contents('data/namesList.json'));
            $countOfExtractRecords = count($arrayOfRestaurantName);
            echo $countOfExtractRecords;
            die;
        }
        elseif ($_GET['process'] == 'processLoad' || $_GET['process'] == 'allProcess')
        {
            $records = $conn->query('SELECT * FROM info');
            $countOfLoadRecords = count($records->fetch_all());
            echo $countOfLoadRecords;
            die;
        }

    }
?>


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
</head>
<body style="background-color: #ffbf80">


    <header>
      <img src="pyszne.png">
    </header>

    <div class="container text-center">
        <form id="etlForm" method="post">
            <div >
              <h5 class="text-white mt-3">Podaj kod pocztowy</h5>
            </div>
            <div class="input-group mb-3 w-25 p-3 mx-auto">
              <input type="text" class="form-control" placeholder="np. 30-529" maxlength="6" name="postcode" pattern="[0-9]{2}\-[0-9]{3}" autocomplete="off" required autofocus aria-label="Kod pocztowy" value="" />
            </div>
            <div class="mb-3" aria-label="ETL">
              <button type="submit" id="allProcess" name="submitETL" class=" ETLButton btn btn-secondary" value="ETL">ETL</button>
            </div>
            <div class="btn-group btn-group-sm btn-outline-secondary mb-3" role="group" aria-label="ETL">
              <button type="submit" name="submitE" id="processExtract" class=" ETLButton btn btn-secondary" value="E" >E</button>
              <button type="submit" name="submitT" id="processTransform" disabled class="ETLButton btn btn-secondary" value="T" >T</button>
              <button type="submit" name="submitL" id="processLoad" disabled="true" class="ETLButton btn btn-secondary" value="L" >L</button>
            </div>
        </form>

        <div class="mt-3">
            <a id="showResults" class="d-none" aria-label="Results" href="result.php">Zobacz wyniki</a>
        </div>

        <?php if (isset($countOfExtractRecords)) :?>

            <div class="text-center">
                <p>Liczba pobranych rekordów: <?php echo $countOfExtractRecords; ?></p>
            </div>

        <?php endif; ?>

        <?php if (isset($countOfLoadRecords)) :?>

            <div class="text-center">
                <p>Liczba rekordów załadowanych do bazy danych: <?php echo $countOfLoadRecords; ?></p>
            </div>

        <?php endif; ?>


    </div>

</body>
</html>