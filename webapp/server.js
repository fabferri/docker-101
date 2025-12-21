const http = require('http');
const os = require('os');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Docker Web App</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
          }
          .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          }
          h1 { color: #2c3e50; }
          .info { 
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
          }
          .success {
            color: #27ae60;
            font-weight: bold;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🐳 Docker Web Application</h1>
          <p class="success">✓ Your Docker web app is running successfully!</p>
          
          <div class="info">
            <h3>Container Information:</h3>
            <ul>
              <li><strong>Hostname:</strong> ${os.hostname()}</li>
              <li><strong>Platform:</strong> ${os.platform()}</li>
              <li><strong>Node.js Version:</strong> ${process.version}</li>
              <li><strong>Port:</strong> ${PORT}</li>
            </ul>
          </div>
          
          <h3>What's Next?</h3>
          <ul>
            <li>Try stopping and restarting the container</li>
            <li>Modify the code and rebuild the image</li>
            <li>Use volume mounts for live development</li>
            <li>Explore Docker Compose for multi-container apps</li>
          </ul>
        </div>
      </body>
      </html>
    `);
  } else if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }));
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
  }
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Visit http://localhost:${PORT} in your browser`);
});
