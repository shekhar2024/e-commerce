import Login from './components/Login.js';

const routes = [
    { path: '/login', component: Login }
]

const router = new VueRouter({
    routes
});

const app = new Vue({
    router,
    el: '#app',
    template: `
    
    <router-view></router-view>
    
    `,

    data: {
        section: 'frontend'
    },


});