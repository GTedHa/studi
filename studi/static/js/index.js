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
            const notes = data.notes;
            var list = document.createElement('ul');
            list.className = "list-group";

            for(var i = 0; i < notes.length; i++){
              var atagItem = document.createElement('a');
              atagItem.href = 'note/' + notes[i].note_id;

              var item = document.createElement('li');
              item.className = "list-group-item";
              item.dataset.id = notes[i].note_id;

              item.appendChild(document.createTextNode(notes[i].note_name));
              atagItem.appendChild(item);
              list.appendChild(atagItem);
            }

            $('.notes-box').append(list);

          } else if (xhr.status === 500) {
            // console.log('server error');
          } else {
            // console.log('xhr.status');
            // console.log(xhr.status);
          }
     
        },
        error: function(error) {
          //  console.log(error);
          //  console.log('error');
        }
     });


     $(document).on('click', '.list-group-item' ,function(){
    
      var noteId = $(this).data('id');
      var noteName = $(this).text();
 
      // list click 시에 localStrorage에 저장
     localStorage.setItem('noteId', noteId);
     localStorage.setItem('noteName', noteName);
     })
     
});
    
