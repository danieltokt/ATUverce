// ===== ATUverce — Главный JS файл =====

// Утилиты
const LANGS = {
  ru: { feed:'Главная', profile:'Мой профиль', news:'Новости ATU', clubs:'Клубы', leaderboard:'Лидерборд', ai:'ИИ Помощник', logout:'Выйти', coins:'Ala Coins', createPost:'Поделись чем-то с однокурсниками...', publish:'Опубликовать', cancel:'Отмена', loadMore:'Загрузить ещё' },
  en: { feed:'Home', profile:'My Profile', news:'ATU News', clubs:'Clubs', leaderboard:'Leaderboard', ai:'AI Assistant', logout:'Log out', coins:'Ala Coins', createPost:'Share something with classmates...', publish:'Publish', cancel:'Cancel', loadMore:'Load more' },
  ky: { feed:'Башкы бет', profile:'Менин профилим', news:'АТУ жаңылыктары', clubs:'Клубдар', leaderboard:'Рейтинг', ai:'ИИ Жардамчы', logout:'Чыгуу', coins:'Ala Coins', createPost:'Курсташтарың менен бөлүш...', publish:'Жарыялоо', cancel:'Жокко чыгаруу', loadMore:'Дагы жүктөө' }
};

function getLang() { return localStorage.getItem('lang') || 'ru'; }
function setLang(lang) { localStorage.setItem('lang', lang); location.reload(); }
function tr(key) { return LANGS[getLang()][key] || key; }
window.tr = tr;
window.setLang = setLang;
window.getLang = getLang;

const utils = {
  timeAgo(date) {
    const diff = (Date.now() - new Date(date)) / 1000;
    if (diff < 60) return 'только что';
    if (diff < 3600) return `${Math.floor(diff/60)} мин назад`;
    if (diff < 86400) return `${Math.floor(diff/3600)} ч назад`;
    if (diff < 604800) return `${Math.floor(diff/86400)} дн назад`;
    return new Date(date).toLocaleDateString('ru-RU');
  },

  getInitials(name) {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  },

  avatarHTML(user, size = '') {
    if (user.avatar) {
      return `<div class="avatar ${size}"><img src="${user.avatar}" alt="${user.full_name}"></div>`;
    }
    return `<div class="avatar ${size}">${utils.getInitials(user.full_name || user.username)}</div>`;
  },

  showAlert(msg, type = 'success') {
    const el = document.createElement('div');
    el.style.cssText = `position:fixed;top:70px;right:16px;z-index:999;padding:12px 20px;border-radius:8px;font-size:14px;font-weight:500;box-shadow:0 4px 12px rgba(0,0,0,0.15);background:${type === 'success' ? '#42b883' : '#e74c3c'};color:white;`;
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3000);
  }
};

// Компоненты
const components = {
  postCard(post) {
    const coins_info = `<span style="color:#f4b400;font-size:12px">+5 Ala Coins</span>`;
    return `
      <div class="card post-card" id="post-${post.id}">
        <div class="post-header">
          ${utils.avatarHTML(post.author)}
          <div>
            <div class="post-author">${post.author.full_name || post.author.username}</div>
            <div class="post-meta">${post.author.faculty || ''} · ${utils.timeAgo(post.created_at)}</div>
          </div>
        </div>
        <div class="post-content">${post.content}</div>
        ${post.media ? `<img src="${post.media}" class="post-media" alt="Медиа">` : ''}
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
          ${(post.tags || []).map(tag => `<span style="color:var(--primary);font-size:13px">#${tag}</span>`).join('')}
        </div>
        <div class="post-actions">
          <button class="action-btn ${post.is_liked ? 'liked' : ''}" onclick="toggleLike(${post.id}, this)">
            ❤️ ${post.likes_count || 0}
          </button>
          <button class="action-btn" onclick="openComments(${post.id})">
            💬 ${post.comments_count || 0}
          </button>
          <button class="action-btn" onclick="sharePost(${post.id})">
            🔗 Поделиться
          </button>
        </div>
      </div>`;
  },

  leaderboardItem(user, rank) {
    const rankClass = rank <= 3 ? `rank-${rank}` : 'rank-other';
    return `
      <div class="leaderboard-item">
        <div class="rank-badge ${rankClass}">${rank}</div>
        ${utils.avatarHTML(user)}
        <div style="flex:1">
          <div style="font-weight:600;font-size:14px">${user.full_name}</div>
          <div style="font-size:12px;color:var(--text-muted)">${user.faculty || 'Студент'}</div>
        </div>
        <div style="text-align:right">
          <div style="font-weight:700;color:#f4b400">${user.ala_coins}</div>
          <div style="font-size:11px;color:var(--text-muted)">Ala Coins</div>
        </div>
      </div>`;
  },

  newsCard(news) {
    const cats = { event:'cat-event', achievement:'cat-achievement', scholarship:'cat-scholarship', announcement:'cat-announcement' };
    return `
      <div class="card news-card">
        ${news.image ? `<img src="${news.image}" style="width:100%;height:200px;object-fit:cover;border-radius:8px 8px 0 0;margin:-16px -16px 16px;width:calc(100%+32px)" alt="${news.title}">` : ''}
        <span class="news-category ${cats[news.category] || 'cat-announcement'}">${news.category}</span>
        <h3 style="font-size:16px;margin-bottom:8px">${news.title}</h3>
        <p style="color:var(--text-muted);font-size:14px">${news.content.slice(0, 150)}...</p>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px">
          <span style="font-size:12px;color:var(--text-muted)">${utils.timeAgo(news.created_at)}</span>
          <button class="btn btn-outline" style="padding:6px 14px;font-size:13px">Читать →</button>
        </div>
      </div>`;
  }
};

// Действия
async function toggleLike(postId, btn) {
  try {
    const res = await api.likePost(postId);
    const count = btn.querySelector('span') || btn;
    btn.classList.toggle('liked');
    btn.innerHTML = `❤️ ${res.likes_count}`;
  } catch(e) { utils.showAlert('Ошибка', 'error'); }
}

async function openComments(postId) {
  // TODO: открыть модальное окно комментариев
  console.log('Открываем комментарии для поста', postId);
}

function sharePost(postId) {
  navigator.clipboard.writeText(`${window.location.origin}/pages/feed.html#post-${postId}`);
  utils.showAlert('Ссылка скопирована!');
}

// Перезаписываем showAlert с фирменными цветами
utils.showAlert = function(msg, type = 'success') {
  const el = document.createElement('div');
  const bg = type === 'success' ? '#1B3A8C' : '#C8102E';
  el.style.cssText = `position:fixed;top:70px;right:16px;z-index:9999;padding:12px 20px;border-radius:10px;font-size:14px;font-weight:600;box-shadow:0 8px 24px rgba(0,0,0,0.2);background:${bg};color:white;display:flex;align-items:center;gap:8px;max-width:300px;animation:slideIn 0.3s ease;`;
  el.innerHTML = `<span>${type === 'success' ? '✅' : '⚠️'}</span> ${msg}`;
  document.body.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity 0.3s'; setTimeout(() => el.remove(), 300); }, 3000);
};

const style = document.createElement('style');
style.textContent = '@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}';
document.head.appendChild(style);

window.utils = utils;
window.components = components;
window.toggleLike = toggleLike;
window.openComments = openComments;
window.sharePost = sharePost;