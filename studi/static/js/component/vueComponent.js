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
          noteId : null,
          istart : 0, // 0 : 
      },
      created : function(){
          console.log('created!!');
      }
  })

