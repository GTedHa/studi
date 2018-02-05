console.log('vueComponent.js')

// 루트 인스턴스 생성
new Vue({
    el: '#example'
})

var vm = new Vue({
    el: '#notes',
    data: {
        isOk: false, // default : false
        timer: 0, // timer
        totalTime : 0, // timer
        title: 'basic title',
        noteId: null,
        pointList: [],
        currentClauseId: null, // 현재 보여지고 있는 clause
        currentClauseTitle : '',
        currentClauseContent : '',
        currentIndex : '',
        checkPoint : 1, // survey's value, default : 1 (전체 보기)
        isAvailClause : false, // 조건에 해당하는 clause 인지 여부
        currentOptions : {
            imp: 1, // 0 : 안중요, 1 : 중요
            und: 2, // 0 : 이해x, 1 : 보통,  2 : 이해 o
        },
        constCurrentOptions : {
            imp: 1, // 0 : 안중요, 1 : 중요
            und: 2, // 0 : 이해x, 1 : 보통,  2 : 이해 o
        },
        radio : 0,
        isChanged : false,
        tiemrObj : null
    },
    created: function () {
        console.log('\n [created]');

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
        filterClause : function(thisPoint){
            console.log('\n [filterClause]');

            // 현재의 cluase가 survey 조건과 부합하면 true,
            //                            부합하지 않으면 false 

           // checkPoint : 1 ( 전체보기 )
            //              2 ( 중요한 것만 보기 , imp = 1)
            //              3 ( 아는 것만 보기, und = 2)
            //              4 ( 애매한 것만 보기, und = 1 )
            //              5 (모르는 것만 보기, und = 0 )


            switch (Number(this.checkPoint)) {
                case 1 : console.log('1 : 전체보기 입니다');
                        this.isAvailClause = true;
                        break;
                case 2 : console.log('2 : 중요한 것만 보기(imp = 1)');
                        if (thisPoint.imp == 1) {
                            this.isAvailClause = true;
                        } else {
                            this.isAvailClause = false;
                        }
                         break;
                case 3 : console.log('3 : 아는 것만 보기(und = 2)');
                        if (thisPoint.und == 2) {
                            this.isAvailClause = true;
                        } else {
                            this.isAvailClause = false;
                        }
                         break;
                case 4 : console.log('4 : 애매한 것만 보기 (und = 1)');
                        if (thisPoint.und == 1) {
                            this.isAvailClause = true;
                        } else {
                            this.isAvailClause = false;
                        }                     
                         break;
                case 5 : console.log('5 : 모르는 것만 보기 (und = 0)');
                        if (thisPoint.und == 0) {
                            this.isAvailClause = true;
                        } else {
                            this.isAvailClause = false;
                        }
                         break;       
            }
            console.log('해당 퀴즈는 보여줘도 되겠습니까? : ' + this.isAvailClause);
        }, 
        showClause: function (clauseId) {
            console.log('\n [showClause]');
            // 보여질 예정인 clauseId의 point 정보 search
            var thisClausePoint = this.searchPointInfo(clauseId);

            // 해당 point 정보가 this.checkPoint 조건에 맞는지 검사
                this.filterClause(thisClausePoint);


            if (this.isAvailClause) {
                // todo 변경 여부 상관 없이 일단 업데이트 하도록 하기 위함
                  // 업데이트 시킬 value
                this.currentOptions.imp = thisClausePoint.imp;
                this.currentOptions.und = thisClausePoint.und;

                // 저장되어 있는 value
                this.constCurrentOptions.imp = thisClausePoint.imp;
                this.constCurrentOptions.und = thisClausePoint.und;

                var $collapseContent = $('#collapseContent');

                if($collapseContent.hasClass('in')){
                    $('#collapse-btn').click();
                }
    
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
                        self.currentClauseId = data.clause_id;
                        self.currentClauseTitle = data.title;
                        self.currentClauseContent = data.contents;
    
                    }, error: function (error) {
                        console.log('get cluase fail');
                    }
                })

            } else {
                // 조건에 해당하지 않으므로 다음 cluase로 이동
                this.next();
            }
        },
        searchPointInfo : function (clauseId) {
            console.log('\n [searchPointInfo]');
           for( obj of this.pointList){
               // 해당 clause의 point 정보를 찾음
               if(obj.clause_id == clauseId){
                    console.log('현재 퀴즈 '+ clauseId +' 번의 포인트 정보');
                    console.log(JSON.stringify(obj, null, 2));
                   return obj; // 일치하는 point 정보를 반환
               }
           }
        },
        updateClause : function (clauseId){
            console.log('\n [updateClause]');
            var self = this;

            $.ajax({
                url : "/point/update",
                type : 'PUT',
                async : false,
                data : {
                    clause_id : this.currentClauseId,
                    imp : this.currentOptions.imp,
                    und : this.currentOptions.und
                },
                dataType : 'json',
                success : function (data, textStatus, xhr){
                    console.log('update success');
                    console.log(data);
                    // this.pointlist에서 해당 clause를 찾아서
                    // value를 변경시킨다
                    for( obj of self.pointList){
                        if(obj.clause_id == self.currentClauseId){
                            // 변경한 clause 정보
                            obj.imp = self.currentOptions.imp;
                            obj.und = self.currentOptions.und;
                        }
                    }
                }, error : function (error){
                    console.log('update error');
                }
            })
          
        },
        start: function () {
            console.log('\n [start]');
            // console.log('this.pointList');
            // console.log(this.pointList);
            this.startTimer(); // timer
            this.showClause(this.pointList[0].clause_id);
             // 첫 clause의 id를 넘겨줌 
            this.isOk = true; 
        },
        next: function () {
        console.log('\n [next]');
        // console.log('if timerObj');
        // console.log(timerObj);
        this.startTimer(); // timer
            // todo 변경 사항이 있을 경우만 업데이트 
            if (this.isAvailClauses) { //&& this.isChanged
                this.updateClause(this.currentClauseId);
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
                        // todo servey 쪽으로 이동
                        this.isOk = false;
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
            this.startTimer(); // timer
            // todo 변경 사항이 있을 경우만 업데이트 
            if (this.isAvailClauses) { //&& this.isChanged
                this.updateClause(this.currentClauseId);
            }
            var prevClauseId = 0;
            var currentIndex = 0;
            for(clause of this.pointList){
                if(this.currentClauseId === clause.clause_id){
                    // first caluse 
                    if(currentIndex === 0){
                        console.log('첫 퀴즈입니다');
                        this.isOk = false;
                        // todo servey 쪽으로 이동
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
            // console.log('startTimer');
            this.totalTime = Number(this.timer); // 사용자가 입력한 time을 저장함 
            var self = this;
            
            if(this.timerObj != null){
                // 기존에 실행하던 타이머가 있다면 종료
                clearInterval(this.timerObj);
            }
            this.timerObj = window.setInterval(function () {
                if (self.totalTime > 0) {
                    self.totalTime--;
                }

                if(Number(self.totalTime) === 0){
                    // console.log('0초 종료');

                    var $collapseContent = $('#collapseContent');
                    // todo 여기서 collapse 열기 동작 실행
                    if(!$collapseContent.hasClass('in')){
                        $('#collapse-btn').click();
                    }

                    clearInterval(self.timerObj);
                    self.timerObj = null;
                }
            }, 1000);
        },
        checkImp : function(){
            // 중요 버튼을 눌렀을 때의 동작 
            console.log('checkImp');
            console.log('this.currentOptions.imp');
            console.log(this.currentOptions.imp); 
        },
        checkUnd : function(el){   
            var und = el.target.value;
            this.currentOptions.und = und;
        },
        checkSurveyPoint : function (el){
            console.log('checkSurveyPoint');
            // 선택된 radio's value
            this.checkPoint = el.target.value; 
            console.log(this.checkPoint);
        },
    },
    watch: {
        pointList: function () {
            console.log('pointList is changed');
            console.log(this.pointList);
        }
    }
})

