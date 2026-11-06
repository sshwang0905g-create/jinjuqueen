// Vercel Serverless Function: Client Property Inquiries Database (매도·임대 & 매수·임차)
// Path: /api/inquiry.js

const fs = require('fs');
const path = require('path');

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'sshwang0905g-create';
const GITHUB_REPO = process.env.GITHUB_REPO || 'jinjuqueen';
const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'main';
const FILE_PATH = 'data/inquiries.json';

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    // ------------------------------------------------------------------
    // GET: Retrieve Inquiries
    // ------------------------------------------------------------------
    if (req.method === 'GET') {
      const localFilePath = path.join(process.cwd(), FILE_PATH);
      if (fs.existsSync(localFilePath)) {
        const fileContent = fs.readFileSync(localFilePath, 'utf-8');
        const list = JSON.parse(fileContent);
        return res.status(200).json({ success: true, inquiries: list });
      }
      return res.status(200).json({ success: true, inquiries: [] });
    }

    // ------------------------------------------------------------------
    // POST: Save Client Inquiry (매도/임대 or 매수/임차)
    // ------------------------------------------------------------------
    if (req.method === 'POST') {
      let body = req.body;
      if (typeof body === 'string') {
        try { body = JSON.parse(body); } catch (e) {}
      }

      const inquiry = {
        id: `inq-${Date.now()}`,
        mode: body.mode || 'sell',
        modeName: body.modeName || (body.mode === 'buy' ? '매물 구하기' : '매물 내놓기'),
        propType: body.propType || '',
        transType: body.transType || '',
        price: body.price || '',
        address: body.address || '',
        name: body.name || '',
        phone: body.phone || '',
        notes: body.notes || '',
        createdAt: new Date().toISOString()
      };

      // 1. Read existing local inquiries
      const localFilePath = path.join(process.cwd(), FILE_PATH);
      let list = [];
      if (fs.existsSync(localFilePath)) {
        try {
          list = JSON.parse(fs.readFileSync(localFilePath, 'utf-8'));
        } catch (e) {}
      }

      list.unshift(inquiry);

      // Save locally
      try {
        fs.writeFileSync(localFilePath, JSON.stringify(list, null, 2), 'utf-8');
      } catch (err) {}

      // 2. Commit to GitHub if token configured
      if (GITHUB_TOKEN && GITHUB_OWNER && GITHUB_REPO) {
        try {
          const ghUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${FILE_PATH}`;
          let currentSha = null;
          const headRes = await fetch(ghUrl + `?ref=${GITHUB_BRANCH}&t=${Date.now()}`, {
            headers: {
              'Authorization': `Bearer ${GITHUB_TOKEN}`,
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'JinjuQueen-Serverless'
            }
          });
          if (headRes.ok) {
            const hData = await headRes.json();
            currentSha = hData.sha;
          }

          const base64Content = Buffer.from(JSON.stringify(list, null, 2), 'utf-8').toString('base64');
          await fetch(ghUrl, {
            method: 'PUT',
            headers: {
              'Authorization': `Bearer ${GITHUB_TOKEN}`,
              'Accept': 'application/vnd.github.v3+json',
              'Content-Type': 'application/json',
              'User-Agent': 'JinjuQueen-Serverless'
            },
            body: JSON.stringify({
              message: `feat(inquiry): new client inquiry by ${inquiry.name} (${inquiry.modeName})`,
              content: base64Content,
              sha: currentSha,
              branch: GITHUB_BRANCH
            })
          });
        } catch (e) {}
      }

      return res.status(200).json({
        success: true,
        message: '고객 의뢰가 성공적으로 접수되었습니다.',
        inquiry
      });
    }

    return res.status(405).json({ success: false, message: 'Method not allowed' });
  } catch (err) {
    console.error('Inquiry API error:', err);
    return res.status(500).json({ success: false, message: err.message });
  }
};

