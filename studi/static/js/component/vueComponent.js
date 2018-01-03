console.log('vueComponent.js')
// 등록
Vue.component('my-component', {
    template: '<div>사용자 정의 컴포넌트 입니다!</div>'
  })
  
  // 루트 인스턴스 생성
  new Vue({
    el: '#example'
  })

  new Vue({
      el : '#notes',
      data : {
          timer : 0, // timer
          title : 'title',
          noteId : null,
          imp : [], // 0 : 안중요, 1 : 중요
          und : [], // 0 : 이해x, 1 : 보통,  2 : 이해 o
          clauseList : [],
          selectedClauseList : []
      },
      created : function(){
          console.log('created!!');
          var noteId = localStorage.getItem('noteId');
          var noteName = localStorage.getItem('noteName');
          // 노트에 대한 정보 호출
        //   $.ajax({
        //       url : "note/",
        //   })
      },
      methods : {
          start : function(){
              console.log('start');
          },
          next : function(){
              // 조건 조회하여 
              // 다음 퀴즈 보여주기
          }
      }
  })

