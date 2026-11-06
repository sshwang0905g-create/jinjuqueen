// Vercel Serverless Function: GitHub Repository as Serverless JSON Database for Properties
// Path: /api/properties.js

const fs = require('fs');
const path = require('path');

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'sshwang0905g-create';
const GITHUB_REPO = process.env.GITHUB_REPO || 'jinjuqueen';
const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'main';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'queen1234!';
const FILE_PATH = 'data/properties.json';

module.exports = async (req, res) => {
  // CORS & Header Setup
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-admin-password');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    // ------------------------------------------------------------------
    // GET: Retrieve Properties from GitHub or Local Fallback
    // ------------------------------------------------------------------
    if (req.method === 'GET') {
      if (GITHUB_TOKEN && GITHUB_OWNER && GITHUB_REPO) {
        try {
          const ghUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${FILE_PATH}?ref=${GITHUB_BRANCH}&t=${Date.now()}`;
          const response = await fetch(ghUrl, {
            headers: {
              'Authorization': `Bearer ${GITHUB_TOKEN}`,
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'JinjuQueen-Serverless-Admin'
            }
          });

          if (response.ok) {
            const fileData = await response.json();
            const contentStr = Buffer.from(fileData.content, 'base64').toString('utf-8');
            const props = JSON.parse(contentStr);
            return res.status(200).json({
              success: true,
              source: 'github',
              sha: fileData.sha,
              properties: props
            });
          }
        } catch (fetchErr) {
          console.warn('GitHub fetch failed, falling back to local file:', fetchErr);
        }
      }

      // Local filesystem fallback
      const localFilePath = path.join(process.cwd(), FILE_PATH);
      if (fs.existsSync(localFilePath)) {
        const fileContent = fs.readFileSync(localFilePath, 'utf-8');
        const props = JSON.parse(fileContent);
        return res.status(200).json({
          success: true,
          source: 'local',
          properties: props
        });
      }

      return res.status(404).json({ success: false, message: 'properties.json file not found' });
    }

    // ------------------------------------------------------------------
    // AUTH CHECK FOR WRITE OPERATIONS (POST)
    // ------------------------------------------------------------------
    const authHeader = req.headers['authorization'] || '';
    const customPass = req.headers['x-admin-password'] || '';
    const token = authHeader.replace('Bearer ', '').trim();

    if (token !== ADMIN_PASSWORD && customPass !== ADMIN_PASSWORD) {
      return res.status(401).json({
        success: false,
        message: '관리자 인증에 실패했습니다. 비밀번호를 확인해 주세요.'
      });
    }

    // Parse request body
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) {}
    }

    const { action, property, properties: bulkList } = body || {};

    // 1. Fetch current properties & sha
    let currentProps = [];
    let currentSha = null;

    if (GITHUB_TOKEN && GITHUB_OWNER && GITHUB_REPO) {
      try {
        const ghUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${FILE_PATH}?ref=${GITHUB_BRANCH}&t=${Date.now()}`;
        const response = await fetch(ghUrl, {
          headers: {
            'Authorization': `Bearer ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'JinjuQueen-Serverless-Admin'
          }
        });
        if (response.ok) {
          const fileData = await response.json();
          currentSha = fileData.sha;
          const contentStr = Buffer.from(fileData.content, 'base64').toString('utf-8');
          currentProps = JSON.parse(contentStr);
        }
      } catch (err) {
        console.warn('GitHub fetch error on write:', err);
      }
    }

    if (currentProps.length === 0) {
      const localFilePath = path.join(process.cwd(), FILE_PATH);
      if (fs.existsSync(localFilePath)) {
        currentProps = JSON.parse(fs.readFileSync(localFilePath, 'utf-8'));
      }
    }

    // 2. Perform CRUD mutation
    let finalProps = [...currentProps];

    if (bulkList && Array.isArray(bulkList)) {
      finalProps = bulkList;
    } else if (action === 'toggle_status' && property) {
      const targetId = property.id;
      for (const p of finalProps) {
        if (p.id === targetId) {
          p.status = p.status === 'ACTIVE' ? 'SOLD' : 'ACTIVE';
          p.badge = p.status === 'SOLD' ? '거래완료' : '추천매물';
          break;
        }
      }
    } else if (action === 'create' && property) {
      const newProp = {
        ...property,
        id: property.id || `prop-${Date.now()}`,
        status: property.status || 'ACTIVE',
        badge: property.badge || '추천매물'
      };
      finalProps.unshift(newProp);
    } else if (action === 'update' && property) {
      const idx = finalProps.findIndex(p => p.id === property.id);
      if (idx > -1) {
        finalProps[idx] = { ...finalProps[idx], ...property };
      }
    } else if (action === 'delete' && property && property.id) {
      finalProps = finalProps.filter(p => p.id !== property.id);
    } else if (action === 'toggle_private' && property) {
      const targetId = property.id;
      for (const p of finalProps) {
        if (p.id === targetId) {
          const newPriv = property.isPrivate !== undefined ? property.isPrivate : !Boolean(p.isPrivate || p.status === 'PRIVATE' || p.hidden);
          p.isPrivate = newPriv;
          p.hidden = newPriv;
          break;
        }
      }
    }

    const jsonString = JSON.stringify(finalProps, null, 2);

    // 3. Save to GitHub Repository (Vercel Serverless Persistent DB)
    if (GITHUB_TOKEN && GITHUB_OWNER && GITHUB_REPO) {
      if (!currentSha) {
        try {
          const ghUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${FILE_PATH}?ref=${GITHUB_BRANCH}&t=${Date.now()}`;
          const headRes = await fetch(ghUrl, {
            headers: {
              'Authorization': `Bearer ${GITHUB_TOKEN}`,
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'JinjuQueen-Serverless-Admin'
            }
          });
          if (headRes.ok) {
            const hData = await headRes.json();
            currentSha = hData.sha;
          }
        } catch (e) {}
      }

      const ghPutUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${FILE_PATH}`;
      const commitMessage = `feat(properties): ${action || 'update'} properties.json by Serverless Admin`;
      const base64Content = Buffer.from(jsonString, 'utf-8').toString('base64');

      const commitRes = await fetch(ghPutUrl, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json',
          'User-Agent': 'JinjuQueen-Serverless-Admin'
        },
        body: JSON.stringify({
          message: commitMessage,
          content: base64Content,
          sha: currentSha,
          branch: GITHUB_BRANCH
        })
      });

      if (!commitRes.ok) {
        const errorData = await commitRes.json();
        return res.status(commitRes.status).json({
          success: false,
          message: `GitHub 커밋 실패: ${errorData.message}`,
          details: errorData
        });
      }

      const commitResult = await commitRes.json();
      return res.status(200).json({
        success: true,
        source: 'github',
        commit: commitResult.commit.sha,
        properties: finalProps,
        message: 'GitHub 저장소(data/properties.json)에 성공적으로 커밋되어 영구 보존되었습니다.'
      });
    }

    // Fallback: Local filesystem write
    try {
      const localFilePath = path.join(process.cwd(), FILE_PATH);
      fs.writeFileSync(localFilePath, jsonString, 'utf-8');
      return res.status(200).json({
        success: true,
        source: 'local',
        properties: finalProps,
        message: '로컬 data/properties.json 파일에 저장되었습니다. (Vercel 환경변수 설정 시 GitHub 영구 커밋 연동)'
      });
    } catch (fsErr) {
      // If Vercel read-only filesystem without GitHub token
      return res.status(500).json({
        success: false,
        message: 'Vercel 서버리스 환경에서는 GitHub 환경변수(GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO)가 설정되어야 데이터가 영구 보존됩니다.'
      });
    }

  } catch (error) {
    console.error('Serverless Properties API Error:', error);
    return res.status(500).json({
      success: false,
      message: error.message || '서버리스 매물 API 처리 중 오류가 발생했습니다.'
    });
  }
};

