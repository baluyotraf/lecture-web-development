new Vue({
    el: '#entries',
    data: {
        user: {
            username: null,
        },
        diary: {
            title: null,
            body: null,
        },
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
            .catch((response) => {})

            query = new URLSearchParams(window.location.search);
            this.id = parseInt(query.get('id'));
            this.exists = !isNaN(this.id);
            if (this.exists) {
                axios({
                    method: 'get',
                    url: `/api/diary_entries/${this.id}`,
                    headers: {
                        'Authorization': 'Bearer ' + token
                    },
                })
                .then((response) => {
                    this.diary.title = response.data.title;
                    this.diary.body = response.data.body;
                })
                .catch((response) => {})
            }
        }
    },
    methods: {
        logOut: function() {
            localStorage.clear();
            window.location.href='/index.html';
        },
        saveEntry: function() {
            token = localStorage.getItem('token')
            if (this.exists) {
                axios({
                    method: 'patch',
                    url: `/api/diary_entries/${this.id}`,
                    headers: {
                        'Authorization': 'Bearer ' + token,
                    },
                    data: this.diary,
                })
                .then((response) => {
                    window.location.href = `/entry.html?id=${this.id}`;
                })
                .catch((response) => {});
            }
            else {
                axios({
                    method: 'post',
                    url: '/api/diary_entries',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                    },
                    data: this.diary,
                })
                .then((response) => {
                    id = response.data.id;
                    window.location.href = `/entry.html?id=${id}`;
                })
                .catch((response) => {
                    console.log(response);
                })
            }
        }
    },
})