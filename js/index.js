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

                var errorMessage = 'Wprowadzony kod pocztowy nie istnieje. Prosimy o sprawdzenie danych i sprobowanie ponownie.';
                var messageClass = 'countOfRecords';
                if(data['process'] == 'processExtract')
                {

                    clearClass(messageClass);
                    if(this.responseText.trim() === errorMessage) {

                        $('#etlForm').append('<p class="countOfRecords alert alert-danger">Error: ' + this.responseText + '</p>');
                        $('#processExtract').removeAttr('disabled');
                        $('#allProcess').removeAttr('disabled');
                        return;
                    }

                    var countOfRecords = this.responseText;

                    $('#etlForm').append('<p class="countOfRecords alert alert-success">Liczba pobranych rekordów: ' + countOfRecords + '</p>');

                    $('#processExtract').removeAttr('disabled');
                    $('#processTransform').removeAttr('disabled');
                    $('#processLoad').attr('disabled');
                    $('#showResults').addClass('d-none');
            }

                if(data['process'] == 'processTransform')
                {
                    $('#processLoad').removeAttr('disabled');
                }

                if(data['process'] == 'processLoad')
                {
                    var countOfRecords = this.responseText;
                    clearClass(messageClass);
                    $('#etlForm').append('<p class="countOfRecords alert alert-success">Liczba rekordów załadowanych do bazy danych: ' + countOfRecords + '</p>');

                    $('#processTransform').prop('disabled', "true");
                    $('#showResults').removeClass('d-none');
                }

                if(data['process'] == 'allProcess')
                {
                    clearClass(messageClass);
                    if(this.responseText.trim() === errorMessage) {

                        $('#etlForm').append('<p class="countOfRecords alert alert-danger">Error: ' + this.responseText + '</p>');
                        $('#processExtract').removeAttr('disabled');
                        $('#allProcess').removeAttr('disabled');

                        return;
                    }
                    var countOfRecords = this.responseText;
                    $('#etlForm').append('<p class="countOfRecords alert alert-success">Liczba rekordów załadowanych do bazy danych: ' + countOfRecords + '</p>');

                    $('#processExtract').removeAttr('disabled');
                    $('#allProcess').removeAttr('disabled');
                    $('#showResults').removeClass('d-none');

                }

            }
        };
        xhttp.open("GET", url, true);
        xhttp.send();

    });

});

function clearClass(className)
{
    $("." + className).remove();
}

