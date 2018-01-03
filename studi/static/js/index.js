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


     $(document).on('click', '.list-group-item' ,function(){
    
      var noteId = $(this).data('id');
      var noteName = $(this).text();
      console.log('noteName');
      console.log(noteName);
      console.log('noteId');
      console.log(noteId);

      // list click 시에 localStrorage에 저장
     localStorage.setItem('noteId', noteId);
     localStorage.setItem('noteName', noteName);

     //todo url을 변경하지 않고 넘길 수도 있으나
     // a 태그로 url 이동하는 걸로 수정
     $.ajax({
       url : '/note/'+ noteId,
       type: 'GET',
       async: false,
       success : function(data){
        //  console.log('data');
        //  console.log(data);
         $('body').html(data);
       },
       error : function(){
         console.log('error');
       }
     })


     })
     
});
    
