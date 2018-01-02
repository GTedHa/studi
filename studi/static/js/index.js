$(document).ready(function(){

    $.ajax({
        url: "/notes",
        type: 'POST',
        async: false,
        dataType: 'json',
        success: function(data, textStatus, xhr) {

          // 200 : OK
          // 201 : OK, but empty response
          // 500 : server error
          if (xhr.status >= 200) {
            console.log('textStatus');
            console.log(textStatus);
            // console.log(data.notes); // note_name, note_id
            const notes = data.notes;
            console.log(notes);
            var list = document.createElement('ul');
            list.className = "list-group";

            for(var i = 0; i < notes.length; i++){
              var item = document.createElement('li');
              item.className = "list-group-item";
              item.dataset.id = notes[i].note_id;
              item.appendChild(document.createTextNode(notes[i].note_name));
              list.appendChild(item);
            }

            console.log('list');
            console.log(list);
            $('.notes-box').append(list);
           console.log('실행 완료')



          } else if (xhr.status === 500) {
            console.log('server error');
          } else {
            console.log('xhr.status');
            console.log(xhr.status);
          }
     
        },
        error: function(error) {
           console.log(error);
           console.log('error');
        }
     });

});
    
