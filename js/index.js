$( document ).ready(function() {

    $(document).on('click', '.ETLButton', function () {

        event.preventDefault();
        var form = $(this).parents('form:first');
        var formData = form.serializeArray();

        var data = {};

        data[formData[0]['name']] = formData[0]['value'];

        if(formData[1])
        {
            data[formData[1]['name']] = formData[1]['value'];
        }

        if(data['process'] == 'processExtract')
        {
            $('#processTransform').removeClass('d-none');
            $('#processLoad').addClass('d-none');
        }

        if(data['process'] == 'processTransform')
        {
            $('#processLoad').removeClass('d-none');
        }

        if(data['process'] == 'processLoad')
        {
            $('#processTransform').addClass('d-none');
        }

        console.log(data);
        var url = window.location.origin + "/pysznyScraping/index.php?ajax=1&process=" + data['process'] + '&postcode=' + data['postcode'];

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
             alert('assassas');
            }
        };
        xhttp.open("GET", url, true);
        xhttp.send();


    });

    function sendAjax1(url, data, error)
    {
       $.ajax({
            type: 'POST',
          url: url,
          data: {data:data},
          success: function (data) {
             alert("succes");
          },
          error: error,
          dataType: "JSON"
       });
    }
});


