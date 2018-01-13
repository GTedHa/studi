console.log('vueComponent.js')
// 등록
Vue.component('my-component', {
    template: '<div>사용자 정의 컴포넌트 입니다!</div>'
})

// 루트 인스턴스 생성
new Vue({
    el: '#example'
})

var vm = new Vue({
    el: '#notes',
    data: {
        isOk: false, // default : false
        timer: 0, // timer
        title: 'basic title',
        noteId: null,
        
        pointList: [],
        currentClauseId: null, // 현재 보여지고 있는 clause
        currentClauseTitle : '',
        currentClauseContent : '',
        currentIndex : '',
        currentOtions : {
            imp: 0, // 0 : 안중요, 1 : 중요
            und: 0, // 0 : 이해x, 1 : 보통,  2 : 이해 o
        },
        radio : 0,
        isChanged : false,
    },
    created: function () {

        var noteId = localStorage.getItem('noteId');
        var noteName = localStorage.getItem('noteName');
        var self = this; // ajax에서는 this에 대한 scope가 변경되므로 this를 담아서 전달해주어야 함

        this.title = noteName;
        this.noteId = noteId;

        // clause에 대한 point 정보 호출
        $.ajax({
            url: "/points",
            type: 'POST',
            async: false,
            data: {
                note_id: this.noteId
            },
            dataType: 'json',
            success: function (data, textStatus, xhr) {
                self.pointList = data.clause_points;
            },
            error: function (error) {
                console.log('get points fail');
            }
        })

    },
    methods: {
        showClause: function (clauseId) {

            console.log('showNextCluase');
            console.log('clauseId');
            console.log(clauseId);
            var self = this;

            $.ajax({
                url: "/clause",
                type: 'POST',
                async: false,
                data: {
                    clause_id: clauseId
                },
                dataType: 'json',
                success: function (data, textStatus, xhr) {
                    // console.log('get cluase success');
                    // console.log(data);
                    // console.log(data.title)
                    // console.log($('#clause-title'));
                    self.currentClauseTitle = data.title;
                    self.currentClauseContent = data.contents;

                }, error: function (error) {
                    console.log('get cluase fail');
                }
            })
        },
        updateClause : function (clauseId){
            var self = this;

            $.ajax({
                url : "point/update",
                type : 'PUT',
                async : false,
                data : {
                    clause_id : this.currentClauseId,
                    imp : this.currentOtions.imp,
                    und : this.currentOtions.und
                },
                dataType : 'json',
                success : function (data, textStatus, xhr){
                    console.log('update success');
                    console.log(data);
                }, error : function (error){
                    console.log('update error');
                }
            })
          
        },
        start: function () {
            console.log('start');
            console.log('this.pointList');
            console.log(this.pointList);

            this.currentClauseId = this.pointList[0].clause_id;

        

            console.log('this.currentClauseId');
            console.log(this.currentClauseId);
            
            this.showClause(this.currentClauseId);
            this.isOk = true;
        },
        next: function () {
        console.log('\n next');
            // 변경 사항이 있을 경우만 업데이트 
            if (this.isChanged) {
                // this.updateClause(this.currentClauseId);
            }

            var stop = false;
            var currentIndex = 0;
            // 조건 조회하여 다음 퀴즈 보여주기
            for(clause of this.pointList){
       
                if (stop === true) {
                    this.currentClauseId = clause.clause_id;
                    this.showClause(this.currentClauseId);
                    return;
                }
                if (this.currentClauseId === clause.clause_id) {
                    // last clause
                    if(currentIndex === this.pointList.length - 1){
                        return;
                    }
                    // 세부 조건은 여기서 추가
                    stop = true;
                }
                currentIndex ++;
            } 

        },
        prev : function () {
            console.log('\nprev');
            // 변경 사항이 있을 경우만 업데이트 
            if (this.isChanged) {
                // this.updateClause(this.currentClauseId);
            }
            var prevClauseId = 0;
            var currentIndex = 0;
            for(clause of this.pointList){
                if(this.currentClauseId === clause.clause_id){
                    // first caluse 
                    if(currentIndex === 0){
                        console.log('첫 퀴즈입니다');
                        return false;
                    }

                    this.currentClauseId = prevClauseId;
                } else {
                    prevClauseId = clause.clause_id;
                }
                currentIndex++;
            }
            this.showClause(this.currentClauseId);

        },
        startTimer: function () {
            var totalTime = this.timer;
            var timerObj = window.setInterval(function () {
                if (totalTime > 0) {
                    totalTime--;
                } else {
                    clearInterval(timerObj);
                }
            }, 1000);
        }
    },
    watch: {
        pointList: function () {
            // console.log('pointList is changed');
            // console.log(this.pointList);
        },
        currentOtions : function(){
            // option의 value가 변경될 경우에
            this.isChanged = true; 
        }
    }
})

