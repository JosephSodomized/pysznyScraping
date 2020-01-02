$( document ).ready(function() {

    $(document).on('click', '.ETLButton', function () {

        event.preventDefault();

        $('#allProcess').prop('disabled', "true");
        $('#processExtract').prop('disabled', "true");
        $('#processTransform').prop('disabled', "true");
        $('#processLoad').prop('disabled', "true");

        var form = $(this).parents('form:first');
        var formData = form.serializeArray();

        var data = {};

        if(formData[0])
        {
            data[formData[0]['name']] = formData[0]['value'];
        }

        data['process'] = $(this).attr('id');

        var url = window.location.origin + "/pysznyScraping/index.php?ajax=1&process=" + data['process'] + '&postcode=' + data['postcode'];

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {

                if(data['process'] == 'processExtract')
                {
                    $('#processExtract').removeAttr('disabled');
                    $('#processTransform').removeAttr('disabled');
                    $('#processLoad').attr('disabled');
                    $('#showResults').addClass('d-none');

                    console.log(this.responseText);
                    var countOfRecords = this.responseText;

                    $('#etlForm').append('<p class="countOfRecords">Liczba pobranych rekordów: ' + countOfRecords + '</p>');
                }

                if(data['process'] == 'processTransform')
                {
                    $('#processLoad').removeAttr('disabled');
                }

                if(data['process'] == 'processLoad')
                {
                    $('#processTransform').prop('disabled', "true");
                    $('#showResults').removeClass('d-none');

                    var countOfRecords = this.responseText;

                    $('#etlForm').append('<p class="countOfRecords">Liczba rekordów załadowanych do bazy danych: ' + countOfRecords + '</p>');
                }

                if(data['process'] == 'allProcess')
                {
                    $('#processExtract').removeAttr('disabled');
                    $('#allProcess').removeAttr('disabled');

                    var countOfRecords = this.responseText;
                    $('#etlForm').append('<p class="countOfRecords">Liczba rekordów załadowanych do bazy danych: ' + countOfRecords + '</p>');
                }

            }
        };
        xhttp.open("GET", url, true);
        xhttp.send();

    });

});


