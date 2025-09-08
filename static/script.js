import Login from './components/Login.js';
import Home from './components/Home.js';
import Navbar from './components/Navbar.js';

const routes = [
    { path: '/login', component: Login },
    { path: '/home', component: Home }
]

const router = new VueRouter({
    routes
});

const app = new Vue({
    router,
    el: '#app',
    template: `
    <div class="container">
        <nav-bar></nav-bar>
        <router-view></router-view>
    </div>
    `,

    data: {
        section: 'frontend'
    },

    components: {
        'nav-bar': Navbar
    }


});