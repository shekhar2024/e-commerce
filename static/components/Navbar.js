export default {
  template: `
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold text-primary" to="/">E-Commerce</router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li v-if="!isLoggedIn" class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li v-if="isLoggedIn && isAdmin" class="nav-item">
            <router-link class="nav-link" to="/home">Home</router-link>
          </li>
          <li v-if="isLoggedIn && !isAdmin" class="nav-item">
            <router-link class="nav-link" to="/home">Home</router-link>
          </li>
          <li v-if="isLoggedIn" class="nav-item">
            <button @click="logout" class="btn btn-outline-danger">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  `,

  data() {
    return {
      isAdmin: localStorage.getItem("is_admin") === "true",
      isLoggedIn: !!localStorage.getItem("access_token"),
      userId: localStorage.getItem("user_id"),
    };
  },

  methods: {
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user_id");
      localStorage.removeItem("username");
      if (localStorage.getItem("is_admin")) {
        localStorage.removeItem("is_admin");
      }
      this.isLoggedIn = false;
      this.$router.push("/login");
    }
  },
};