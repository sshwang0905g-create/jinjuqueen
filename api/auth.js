// Vercel Serverless Function: Admin Authentication
// Path: /api/auth.js

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'queen1234!';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER;
const GITHUB_REPO = process.env.GITHUB_REPO;

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) {}
  }

  const { password } = body || {};

  if (password === ADMIN_PASSWORD) {
    return res.status(200).json({
      success: true,
      message: '관리자 인증 성공',
      token: ADMIN_PASSWORD,
      githubConnected: Boolean(GITHUB_TOKEN && GITHUB_OWNER && GITHUB_REPO),
      githubRepo: GITHUB_REPO ? `${GITHUB_OWNER}/${GITHUB_REPO}` : null
    });
  }

  return res.status(401).json({
    success: false,
    message: '비밀번호가 일치하지 않습니다.'
  });
};

