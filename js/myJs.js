

$(document).on('click', 'button.showDesc', function () {
   $(this).next("div").toggle("slow");
});

$(document).on('click', '.clearResponse', function () {
   $('.response').text(" ");
   $('.response1').text(" ");
   $('.commentMessage').text(" ");
});

$(document).on('click', '.fetchComments', function () {
   var div = $(this).closest('.oneModal');
   var id = $(this).data('id');
   var parentID = 0;
   var data = {bookID:id, parentID:parentID};
   var url = window.location.origin + "/Books-Library/Index/index";

   sendAjax1(url, data, function (data) {
      div.find('.commentList').html(data.responseText);
   });

});



$(document).on('click', 'button.reply', function () {

   var card = $(this).closest('.comments');
   var replyField = $(this).data('type');
   card.find('.'+replyField).toggle("slow");

   // console.log(card.find('.'+replyField));
   $('.modal').animate({
      scrollTo: card.find('.'+replyField).offset()
   }, 2000);

   // jQuery.scrollTo(card.find('.'+replyField), 1000);
});

// $(document).on('click', 'button.secondReply', function () {
//    var card = $(this).closest('.oneComment');
//    var secondReplyField = card.find('.secondReplyField');
//    $(secondReplyField).toggle("slow");
// });

$(document).ready(function(){
   $(".opacity").hover(function() {
      $(this).animate({opacity: '0.7'}, 250);
      }, function() {
      $(this).animate({opacity: '1'}, 250);
   } );
});

$(document).ready(function(){
   $(".tr").hover(function() {
      $(this).css('backgroundColor', '#f5f0f0');
   }, function() {
      $(this).css('backgroundColor', '#fff');
   } );
});

$(document).on('click', '.addAuthorGrade', function () {

   var div = $(this).parents('.modal:first');
   var id = div.data('id');
   var grade = div.find('input[name="grade"]').val();
   var type = div.data('type');

   if ((grade<1) || (grade>10))
   {
      div.find('.response').text("Ocena powinna mieścić się w przedziale 1-10");
      return;
   }

   var baseUrl = window.location.origin + "/Books-Library/";
   var url = "Authors/authorGradeAdd/" + id;

   url = baseUrl + url;

   sendAjax1(url, grade, function (data) {
      console.log(data);
      div.find('.response').text(data.responseText);

   });
});

$(document).on('click', '.addBookGrade', function () {

   var div = $(this).parents('.modal:first');
   var id = div.data('id');
   var grade = div.find('input[name="grade"]').val();
   var type = div.data('type');

   if ((grade<1) || (grade>10))
   {
      div.find('.response').text("Ocena powinna mieścić się w przedziale 1-10");
      return;
   }

   var baseUrl = window.location.origin + "/Books-Library/";
   var url = "Books/bookGradeAdd/" + id;

   url = baseUrl + url;

   sendAjax1(url, grade, function (data) {
      console.log(data);
      div.find('.response').text(data.responseText);

   });
});


$(document).on('click', '.deleteUserBook', function () {

   var result = confirm("Czy na pewno chcesz usunąć?");
   if (result) {
      var tr = $(this).closest('tr')
      var url_id = $(this).val();
      var url = 'User/deleteBook/'

      url = window.location.origin + "/Books-Library/" + url + url_id;

      sendAjax(url, function (data) {

         if (data.responseText == 'usunieto')
         {
            tr.fadeOut(1000, function () {
               $(this).remove();
            });
         }
      });
   }
});

$(document).on('click', '.deleteBook', function () {

   var result = confirm("Czy na pewno chcesz usunąć?");
   if (result) {
      var tr = $(this).closest('tr');
      var url_id = $(this).val();
      var url = 'Books/deleteBook/';

      url = window.location.origin + "/Books-Library/" + url + url_id;

      sendAjax(url, function (data) {

         if (data.responseText == 'usunieto')
         {
            tr.fadeOut(1000, function () {
               $(this).remove();
            });
         }
      });
   }
});

$(document).on('click', '.deleteAuthor', function () {

   var result = confirm("Czy na pewno chcesz usunąć?");
   if (result) {
      var tr = $(this).closest('tr');
      var url_id = $(this).val();
      var url = 'Authors/authorDelete/';

      url = window.location.origin + "/Books-Library/" + url + url_id;

      sendAjax(url, function (data) {

         if (data.responseText == 'usunieto')
         {
            tr.fadeOut(1000, function () {
               $(this).remove();
            });
         }
      });
   }
});

$(document).on('click', '.updateRead', function () {

   var result = confirm("Czy na pewno chcesz ozanczyć tę pozycję jako przeczytana?");
   if (result) {
      var tr = $(this).closest('tr');
      var url_id = $(this).val();
      var url = 'User/updateReadBook/';
      var title = $(this).data('title');
      var author = $(this).data('author');
      // var button = "<button class=\"btn btn-danger btn-xs btn-delete deleteUserBook\"  value=\" <?php echo $book['id'] ?>\" >Delete</button>"
      var button = "<button class='btn btn-danger btn-xs btn-delete deleteUserBook' value='" + url_id + "' >Delete</button>" ;


      url = window.location.origin + "/Books-Library/" + url + url_id;

      sendAjax(url,function (data) {

         if (data.responseText == 'zmodyfikowano')
         {
            tr.fadeOut(1000, function () {
               $(this).remove();
            });
            $('.isRead tbody').append("<tr><td>" + title + "</td><td>" + author + "</td><td>" + button + "</td></tr>");
         }
      });
   }
});


$(document).on('click', '.toRead', function () {

   var div = $(this).parents('.modal:first');
   var id = div.data('id');
   var type = $(this).data('id');

   var baseUrl = window.location.origin + "/Books-Library/";
   var url = "User/books/" + id;
   var read = 0;

   url = baseUrl + url;

   sendAjax1(url, read, function (data) {
      console.log(data);
      div.find('.response1').text(data.responseText);

   });

});

$(document).on('click', '.read', function () {

   var div = $(this).parents('.modal:first');
   var id = div.data('id');
   var type = $(this).data('id');

   var baseUrl = window.location.origin + "/Books-Library/";
   var url = "User/books/" + id;
   var read = 1;

   url = baseUrl + url;

   sendAjax1(url, read, function (data) {
      console.log(data);
      div.find('.response1').text(data.responseText);

   });

});

$(document).ready(function () {
   $(document).on('click','.addComment', function (event) {

      event.preventDefault();
      var form = $(this).parents('form:first');
      var data = form.serializeArray();
      var div = $(this).closest('.commentSection');
      var type = $(this).data('type');
      // var name = div.closest('.'+$(this).data('name'));
      // var name = div.parents('.'+$(this).data('name'));
      var name = $(this).parents('.'+$(this).data('name') + ':first');
      console.log($(this).data('name'));
      console.log(name);

      var id = $(this).data('id');
      var url = window.location.origin + "/Books-Library/User/addComment/" + id;

      sendAjax1(url, data, function (data) {
         if(data.error != '')
         {
            form.find('.commentMessage:first').text(data.error);
            // commentList.append(data.responseText);
            name.find('.'+type).before(data.responseText);
            // div.find('.'+name).insertBefore(data.responseText);
         }
      })
   });
});


function sendAjax(url, error)
{
   $.post({
      url: url,
      data: {},
      success: function (data) {
         alert("succes");
      },
      error: error,
      dataType: "JSON"
   });
}



function sendAjax1(url, data, error)
{
   $.post({
      url: url,
      data: {data:data},
      success: function (data) {
         alert("succes");
      },
      error: error,
      dataType: "JSON"
   });
}

function sendAjax2(url, data, error) {
   $.post({
      url: url,
      data: {data: data},
      success:  error,
      error: function (data) {
         alert("error");
      },
      dataType: "JSON"
   });
}

