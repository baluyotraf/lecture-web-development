new Vue({
    el: '#entries',
    data: {
        user: {
            username: null,
        },
        diary: {},
        id: null,
        exists: false,
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
            this.id = parseInt(query.get('id'));
            this.exists = this.id !== NaN;
            if (this.exists) {
                axios({
                    method: 'get',
                    url: `/api/diary_entries/${this.id}`,
                    headers: {
                        'Authorization': 'Bearer ' + token
                    },
                })
                .then((response) => {
                    this.diary = response.data;
                })
                .catch((response) => {

                })
            }
        }
    },
    methods: {
        logOut: function() {
            localStorage.clear();
            window.location.href='/index.html';
        },
        deleteEntry: function() {
            if (this.exists){
                axios({
                    method: 'delete',
                    url: `/api/diary_entries/${this.id}`,
                    headers: {
                        'Authorization': `Bearer ` + token
                    }
                })
                .then((response) => {
                    window.location.href = '/entries.html'
                })
                .catch((response) => {

                });
            }
        }
    },
})