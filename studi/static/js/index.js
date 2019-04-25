$(document).ready(function(){

     getNoteList(); // 노트 리스트 정보 가져오기

     $(document).on('click','#upload-file', function(){
      var selectedfile = $('#studi_material').prop("files")[0];

      $('#file-name').text(selectedfile.name);
      var formData = new FormData();
      formData.append("studi_material", selectedfile); 

      $.ajax({
        url : "/api/notes",
        type : 'POST',
        data : formData,
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        async : true,
        success : function(data, textStatus, xhr){
          location.reload(); // 화면 재시작하여 note list 다시 가져오기
        },
        error : function(error){
         alert('업로드 실패');
         location.reload(); // 화면 재시작하여 note list 다시 가져오기
        }
      })
     })

     // 모달 종료 시 재시작
     // todo 파일 업로드 하는 ui에서 bootstrap 제거
     $(document).on('click', '#close', function(){
        location.reload();
     })

     $('#studi_material').change(function(e){
       var selectedfile = $('#studi_material').prop("files")[0];
       $('#file-name').text(selectedfile.name);
     })

     $(document).on('click', '.list-group-item' ,function(){
    
      var noteId = $(this).data('id');
      var noteName = $(this).children('.noteName-item').text();

      // list click 시에 localStrorage에 저장
     localStorage.setItem('noteId', noteId);
     localStorage.setItem('noteName', noteName);
     })



     function getNoteList(){
      $.ajax({
        url: "/api/notes",
        type: 'GET',
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

            // 저장된 note가 있는 경우에만 Item을 추가
            if (notes && notes.length > 0) {
              for(var i = 0; i < notes.length; i++){
                var atagItem = document.createElement('a');
                atagItem.href = 'notes/' + notes[i].note_id;

                var item = document.createElement('li');
                item.className = "list-group-item";
                item.dataset.id = notes[i].note_id;

                var noteNameItem = document.createElement('span');
                noteNameItem.className = "noteName-item";
                noteNameItem.appendChild(document.createTextNode(notes[i].note_name));

                var nextItem = document.createElement('span');
                nextItem.className = "next-item";
                nextItem.appendChild(document.createTextNode('>'));

                item.appendChild(noteNameItem);
                item.appendChild(nextItem);

                atagItem.appendChild(item);
                list.appendChild(atagItem);
              }
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
     }
     
});
    
