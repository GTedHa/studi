Vue.component('clause-content', {
    // 옵션
    props: ['currentClauseContent'],
    template: '<p v-html="clauseContent"></p>',
    data: function () {
        var clauseContent = this.currentClauseContent.replace(/\n/g, "<br /> ")
        return {
            clauseContent
        }
    },
    watch: {
        'currentClauseContent': function (val) {
            this.clauseContent = this.currentClauseContent.replace(/\n/g, "<br /> ")
        }
    }
});

Vue.component('clause-title', {
    props: ['currentClauseTitle'],
    template: '<div v-html="clauseTitle"></div>',
    data: function () {
        var clauseTitle = this.currentClauseTitle.replace(/\n/g, "<br /> ")
        return {
            clauseTitle
        }
    },
    watch: {
        'currentClauseTitle': function (val) {
            this.clauseTitle = this.currentClauseTitle.replace(/\n/g, "<br /> ")
        }
    }
});

new Vue({
    el: '#notes',
    data: {
        isOk: false, // default : false
        timer: 0, // timer
        totalTime: 0, // timer
        title: 'basic title',
        noteId: null,
        pointList: [],
        currentClauseId: null, // 현재 보여지고 있는 clause
        currentClauseTitle: '',
        currentClauseContent: '',
        currentIndex: '',
        checkPoint: 1, // survey's value, default : 1 (전체 보기)
        isAvailClause: false, // 조건에 해당하는 clause 인지 여부
        currentOptions: {
            imp: 1, // 0 : 안중요, 1 : 중요
            und: 2, // 0 : 이해x, 1 : 보통,  2 : 이해 o
        },
        constCurrentOptions: {
            imp: 1, // 0 : 안중요, 1 : 중요
            und: 2, // 0 : 이해x, 1 : 보통,  2 : 이해 o
        }, 
        firstClauseId: null,
        radio: 0,
        isChanged: false,
        tiemrObj: null
    },
    created: function () {
        $(document).on('click', '#delete-note', function(e) {
            var noteName = localStorage.getItem('noteName');
            $('#file-name').text(noteName);
        })

        $(document).on('click', '#delete-file', function (e) {
            var $this = $(e);
            var noteId = localStorage.getItem('noteId');

            $.ajax({
                url: "/note/delete",
                type: 'delete', 
                data: {
                    'note_id': Number(noteId)
                },
                dataType: 'json',
                success: function (data, textStatus, xhr) {
                    // 성공 시 메인(index.html)로 이동
                    location.href = '../';
                },
                error: function (error) {
                    alert('삭제 실패');
                }
            })

        })


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
                // console.log('포인트 정보를 가져왔습니다');

            },
            error: function (error) {
                alert('포인트 정보가 없습니다. 관리자에게 문의해주세요');
            }
        })

    },
    methods: {
        filterClause: function (thisPoint) {
            /*
             현재의 cluase가 survey 조건과 부합하면 true,
                                       부합하지 않으면 false 

             checkPoint : 1 ( 전체보기 )
                          2 ( 중요한 것만 보기 , imp = 1)
                          3 ( 아는 것만 보기, und = 2)
                          4 ( 애매한 것만 보기, und = 1 )
                          5 (모르는 것만 보기, und = 0 )
            */
            switch (Number(this.checkPoint)) {
                case 1:
                    // 전체보기
                    this.isAvailClause = true;
                    break;
                case 2:
                    // 중요한 것만 보기 (Imp = 1)
                    if (thisPoint.imp == 1) {
                        this.isAvailClause = true;
                    } else {
                        this.isAvailClause = false;
                    }
                    break;
                case 3:
                    // 아는 것만 보기 (und = 2)
                    if (thisPoint.und == 2) {
                        this.isAvailClause = true;
                    } else {
                        this.isAvailClause = false;
                    }
                    break;
                case 4:
                    // 애매한 것만 보기 (und = 1)
                    if (thisPoint.und == 1) {
                        this.isAvailClause = true;
                    } else {
                        this.isAvailClause = false;
                    }
                    break;
                case 5:
                    // 모르는 것만 보기 (und = 0)
                    if (thisPoint.und == 0) {
                        this.isAvailClause = true;
                    } else {
                        this.isAvailClause = false;
                    }
                    break;
            }
        },
        showClause: function (clauseId) {
            // 보여질 예정인 clauseId의 point 정보 search
            var thisClausePoint = this.searchPointInfo(clauseId);

            // 해당 point 정보가 this.checkPoint 조건에 맞는지 검사
            this.filterClause(thisClausePoint);

            if (this.isAvailClause) {
                this.isOk = true;
                // todo 변경 여부 상관 없이 일단 업데이트 하도록 하기 위함
                // 업데이트 시킬 value
                this.currentOptions.imp = thisClausePoint.imp;
                this.currentOptions.und = thisClausePoint.und;

                // 저장되어 있는 value
                this.constCurrentOptions.imp = thisClausePoint.imp;
                this.constCurrentOptions.und = thisClausePoint.und;

                var $collapseContent = $('#collapseContent');
                if ($collapseContent.hasClass('in')) {
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
                        self.currentClauseId = data.clause_id;
                        self.currentClauseTitle = data.title;
                        self.currentClauseContent = data.contents;

                    }, error: function (error) {
                        alert("퀴즈를 불러올 수 없습니다");
                    }
                })
            } else {
                // 조건에 해당하지 않으므로 다음 cluase로 이동
                this.next(clauseId);
            }
        },
        searchPointInfo: function (clauseId) {
            for (obj of this.pointList) {
                // 해당 clause의 point 정보를 찾음
                if (obj.clause_id == clauseId) {
                    return obj; // 일치하는 point 정보를 반환
                }
            }
        },
        updateClause: function (clauseId) {
            var self = this;

            $.ajax({
                url: "/point/update",
                type: 'PUT',
                async: false,
                data: {
                    clause_id: this.currentClauseId,
                    imp: this.currentOptions.imp,
                    und: this.currentOptions.und
                },
                dataType: 'json',
                success: function (data, textStatus, xhr) {
                    // this.pointlist에서 해당 clause를 찾아서 value를 변경
                    for (obj of self.pointList) {
                        if (obj.clause_id == self.currentClauseId) {
                            // 변경한 clause 정보
                            obj.imp = self.currentOptions.imp;
                            obj.und = self.currentOptions.und;
                        }
                    }
                }, error: function (error) {
                    alert('업데이트에 실패하였습니다');
                }
            })

        },
        start: function () {
            this.startTimer(); // timer
            this.showClause(this.pointList[0].clause_id);
        },
        next: function (currentClauseId) {
            // todo 변경 사항이 있을 경우만 업데이트 
            // if (this.isAvailClauses) { //&& this.isChanged
            this.updateClause(currentClauseId);
            // }

            var currentIndex = 0;
            // 조건 조회하여 다음 퀴즈 보여주기
            for (clause of this.pointList) {
                if (currentClauseId === clause.clause_id) {
                    // last clause
                    if (currentIndex === this.pointList.length - 1) {
                        this.isOk = false; // todo servey 쪽으로 이동
                        alert('해당 조건의 퀴즈가 존재하지 않습니다');
                        return;
                    } else {
                        currentIndex++;
                        // 현재의 퀴즈 객체까지 왔을 때 다음 clause를 currentClauseId에 넣어준다
                        this.currentClauseId = this.pointList[currentIndex].clause_id;

                        this.showClause(this.currentClauseId);
                        this.startTimer(); // timer
                        return;
                    }
                } else {
                    currentIndex++;
                }
            }
        },
        prev: function () {
            this.startTimer(); // timer
            // todo 변경 사항이 있을 경우만 업데이트 
            // if (this.isAvailClauses) { //&& this.isChanged
            this.updateClause(this.currentClauseId);
            // }
            var prevClauseId = 0;
            var currentIndex = 0;
            for (clause of this.pointList) {
                if (this.currentClauseId === clause.clause_id) {
                    // first caluse 
                    if (currentIndex === 0) {
                        // 첫 퀴즈
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
            this.totalTime = Number(this.timer); // 사용자가 입력한 time을 저장함 
            var self = this;

            if (this.timerObj != null) {
                // 기존에 실행하던 타이머가 있다면 종료
                clearInterval(this.timerObj);
            }
            this.timerObj = window.setInterval(function () {
                if (self.totalTime > 0) {
                    self.totalTime--;
                }

                if (Number(self.totalTime) === 0) {
                    var $collapseContent = $('#collapseContent');
                    // todo 여기서 collapse 열기 동작 실행
                    if (!$collapseContent.hasClass('in')) {
                        $('#collapse-btn').click();
                    }

                    clearInterval(self.timerObj);
                    self.timerObj = null;
                }
            }, 1000);
        },
        checkImp: function () {
        },
        checkUnd: function (el) {
            var und = el.target.value;
            this.currentOptions.und = und;
        },
        checkSurveyPoint: function (el) {
            // 선택된 radio's value
            this.checkPoint = el.target.value;
        }
    }
})

