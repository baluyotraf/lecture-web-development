new Vue({
    el: '#entries',
    data: {
        user: {
            username: null,
        },
        diaries: {},
        hasPrevious: false,
        hasNext: false,
        page: null,
    },
    mounted: function() {
        token = localStorage.getItem('token')
        if (token === null){
            window.location.href='/index.html';
        }
        else {
            axios({
                method: 'get',
                url: '/api/users/me',
                headers: {
                    'Authorization': 'Bearer ' +  token
                },
            })
            .then((response) => {
                this.user = response.data;                
            })
            .catch((response) => {
            })

            query = new URLSearchParams(window.location.search);
            this.page = parseInt(query.get('page')) || 1;

            axios({
                method: 'get',
                url: '/api/diary_entries',
                params: {
                    page: this.page,
                },
                headers: {
                    'Authorization': 'Bearer ' + token
                },
            })
            .then((response) => {
                this.diaries = response.data.items;
                this.hasPrevious = response.data.previous !== null;
                this.hasNext = response.data.next !== null;
            })
            .catch((response) => {

            })
        }
    },
    methods: {
        logOut: function() {
            localStorage.clear();
            window.location.href='/index.html';
        },
        movePage: function(pageMove) {
            newPage = this.page + pageMove;
            window.location.href = `/entries.html?page=${newPage}`;
        },
        createEntry: function() {
            window.location.href = '/editor.html';
        }
    },
})