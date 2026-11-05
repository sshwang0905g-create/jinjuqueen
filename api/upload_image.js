// Vercel Serverless Function: /api/upload_image
// Accepts JSON { "images": ["data:image/jpeg;base64,..."] }
// Returns { "success": true, "paths": [...] }

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) {}
    }

    const images = (body && body.images) ? body.images : [];
    // On Vercel serverless without persistent disk, data URLs can be preserved or passed through
    return res.status(200).json({
      success: true,
      paths: images
    });
  } catch (err) {
    return res.status(500).json({ success: false, message: err.message });
  }
};

