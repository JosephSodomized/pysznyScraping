<?php
  $postcode = $_POST['postcode'];
  $submitETL = $_POST['submitETL'];
  $submitE = $_POST['submitE'];
  $submitT = $_POST['submitT'];
  $submitL = $_POST['submitL'];

  echo "{$postcode}, {$submitE}--<br />";
  if ($postcode) {
    $command = "";
    $res;
    if ($submitE) {
      $command = "python webscraper.py processExtract {$postcode} 2>&1";
    } else
    if ($submitT) {
      $command = "python webscraper.py processTransform 2>&1";
    } else
    if ($submitL) {
      $command = "python webscraper.py processLoad 2>&1";
    } else {
      $command = "python webscraper.py {$postcode} 2>&1";
    }

    exec($command, $validation, $ok);
  }
?>
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta name="description" content="Restauracje z Pyszne.pl">
    <meta name="author" content="Dominik Malcharczyk, Karolina Pytlak, Anna Łuszczkiewicz, Sebastian Krawczyk">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Pyszny Scraping</title>

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <header>
      <img src="pyszne.png">
    </header>
    <div class="container">
      <form method="post">
        <div>
          <h5 class="text-white mt-3">Podaj kod pocztowy</h5>
        </div>
        <div class="input-group mb-3 w-25 p-3 mx-auto">
          <input type="search" class="form-control" placeholder="np. 30-529" maxlength="6" name="postcode" pattern="[0-9]{2}\-[0-9]{3}" autocomplete="off" required autofocus aria-label="Kod pocztowy" value="<?=$postcode?>" />
        </div>
        <div class="mb-3" aria-label="ETL">
          <button type="submit" name="submitETL" class="btn btn-secondary" value="ETL">ETL</button>
        </div>
        <div class="btn-group btn-group-sm btn-outline-secondary mb-3" role="group" aria-label="ETL">
          <button type="submit" name="submitE" class="btn btn-secondary" value="E" <?=($submitE || $submitT ? "disabled" : "")?>>E</button>
          <button type="submit" name="submitT" class="btn btn-secondary" value="T" <?=($submitE ? "" : "disabled")?>>T</button>
          <button type="submit" name="submitL" class="btn btn-secondary" value="L" <?=($submitT ? "" : "disabled")?>>L</button>
        </div>
        <div class="mt-3">
          <a aria-label="Results" href="/result.php">Zobacz wyniki</a>
        </div>
      </form>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>
