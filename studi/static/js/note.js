$(document).ready(function(){

    $(document).on('click', '#delete-note', function(e) {

        var $this = $(e);    
        var noteId = localStorage.getItem('noteId');

        // alert(noteId);
        var params = {
            'note_id' :Number(noteId)
        }
        // console.log('delete');
        // console.log(params);

        $.ajax({
            url : "/note/delete",
            type : 'delete',
            data : params,
            contentType : false,
            processData : false,
            success : function(data, textStatus, xhr){
                alert('성공');
                // 성공 시 메인(index.html)로 이동
                location.href('/');
            },
            error : function (error){
                alert('실패');
                console.log(error);
            }
        })
    });
});