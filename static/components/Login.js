export default {
    template: `
<div class="container my-5" id="login">
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
      <div class="card p-4 shadow-sm">
        <h4 class="text-center mb-4">Login</h4>
        <form @submit.prevent="loginUser">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input
              type="email"
              class="form-control"
              id="email"
              v-model="formData.email"
              required
              placeholder="you@example.com"
            >
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="formData.password"
              required
              placeholder="Enter your password"
            >
          </div>
          <div class="d-grid">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

`,

data: function() {
    return {
        formData: {
            email: '',
            password: ''
        }
    };
},

methods: {
    loginUser() {
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.formData)
        })
        .then(response => {
          return response.json()
          .then(data => {
            if (response.ok) {
              localStorage.setItem('access_token', data.access_token);
              localStorage.setItem('user_id', data.user.id);
              localStorage.setItem('username', data.user.username);
              if (data.user.is_admin) {
                localStorage.setItem('is_admin', 'true');
                this.$router.push('/login');
              } else {
                localStorage.setItem('is_admin', 'false');
                this.$router.push('/login');
              }
              window.location.reload();
              alert('Login successful!');
            }
            else {
              alert(data.message);
            }
          })
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while logging in. Please try again.');
        });
      }
    }
  }