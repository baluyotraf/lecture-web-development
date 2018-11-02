new Vue({
    el: '#login',
    data: {
        username: null,
        password: null,
        message: null,
    },
    mounted: function() {
        token = localStorage.getItem('token')
        if (token !== null){
            window.location.href = '/entries.html'
        }
    },
    methods: {
        logIn: function() {
            axios({
                method: 'get',
                url: '/api/tokens',
                auth: {
                    username: this.username,
                    password: this.password,
                }
            })
            .then((response) => {
                token = response.data.tokens
                localStorage.setItem('token', token)
                window.location.href = '/entries.html'
            })
            .catch((response) => {
                localStorage.clear()
            });
        },
        signUp: function() {
            axios({
                method: 'post',
                url: '/api/users',
                data: {
                    username: this.username,
                    password: this.password,
                }
            })
            .then((response) => {
                this.message = `Account ${this.username} created`;
            })
            .catch((response) => {})
        }
    },
})