const API_BASE = 'http://localhost:8084/api';

const api = {
  token: () => localStorage.getItem('access_token'),

  headers() {
    const h = { 'Content-Type': 'application/json' };
    if (this.token()) h['Authorization'] = `Bearer ${this.token()}`;
    return h;
  },

  async request(method, endpoint, data = null) {
    const options = { method, headers: this.headers() };
    if (data) options.body = JSON.stringify(data);

    const res = await fetch(`${API_BASE}${endpoint}`, options);

    if (res.status === 401) {
      const refreshed = await this.refreshToken();
      if (!refreshed) { window.location.href = '/pages/login.html'; return; }
      options.headers = this.headers();
      return fetch(`${API_BASE}${endpoint}`, options).then(r => r.json());
    }

    if (res.status === 204 || res.headers.get('content-length') === '0') {
      return {};
    }

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(JSON.stringify(err));
    }

    const text = await res.text();
    if (!text) return {};
    return JSON.parse(text);
  },

  get: (ep) => api.request('GET', ep),
  post: (ep, data) => api.request('POST', ep, data),
  put: (ep, data) => api.request('PUT', ep, data),
  delete: (ep) => api.request('DELETE', ep),
  patch: (ep, data) => api.request('PATCH', ep, data),

  async register(data) {
    const res = await fetch(`${API_BASE}/users/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(JSON.stringify(err));
    }
    return res.json();
  },

  async login(username, password) {
    const res = await fetch(`${API_BASE}/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw new Error('Неверный логин или пароль');
    const data = await res.json();
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  },

  async refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;
    const res = await fetch(`${API_BASE}/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });
    if (!res.ok) { localStorage.clear(); return false; }
    const data = await res.json();
    localStorage.setItem('access_token', data.access);
    return true;
  },

  logout() {
    localStorage.clear();
    window.location.href = '/pages/login.html';
  },

  isLoggedIn: () => !!localStorage.getItem('access_token'),

  getFeed: (page = 1) => api.get(`/posts/?page=${page}`),
  createPost: (data) => api.post('/posts/', data),
  likePost: (id) => api.post(`/posts/${id}/like/`, {}),
  getComments: (id) => api.get(`/posts/${id}/comments/`),
  addComment: (id, content) => api.post(`/posts/${id}/comments/`, { content }),

  getSession: (id) => api.get(`/ai/sessions/${id}/`),
  renameSession: (id, title) => api.patch(`/ai/sessions/${id}/`, { title }),
  deleteSession: (id) => api.delete(`/ai/sessions/${id}/`),

  getProfile: (id) => api.get(`/users/${id}/`),
  updateProfile: (data) => api.put('/users/me/', data),
  follow: (id) => api.post(`/users/${id}/follow/`, {}),

  getStories: () => api.get('/stories/'),
  getNews: (category = '') => api.get(`/news/?category=${category}`),
  getClubs: () => api.get('/clubs/'),
  joinClub: (id) => api.post(`/clubs/${id}/join/`, {}),

  getLeaderboard: () => api.get('/coins/leaderboard/'),
  getMyCoins: () => api.get('/coins/my/'),

  sendMessage: (message, sessionId = null) => api.post('/ai/chat/', { message, session_id: sessionId }),
  getChatSessions: () => api.get('/ai/sessions/'),
};

if (!api.isLoggedIn() &&
  !window.location.pathname.includes('login') &&
  !window.location.pathname.includes('register')) {
  window.location.href = '/pages/login.html';
}