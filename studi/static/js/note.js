$(document).ready(function(){

    $(document).on('click', '#delete-note', function(e) {

        var $this = $(e);    
        var noteId = localStorage.getItem('noteId');

        var params = 
        $.ajax({
            url : "/note/delete",
            type : 'delete',
            data :{
                'note_id' :Number(noteId)
            },
            dataType : 'json',
            success : function(data, textStatus, xhr){
                alert('삭제 성공');
                // 성공 시 메인(index.html)로 이동
                location.href = '../';
            },
            error : function (error){
                alert('삭제 실패');
            }
        })
    });
});