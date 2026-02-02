const http = require('http');

const postData = JSON.stringify({
  model: "llama3.2:3b",
  prompt: "Please provide detailed, in-depth analysis of each of the 10 operating income optimization strategies for Fortune 500 retailers that you mentioned: 1. Cost Reduction, 2. Inventory Optimization, 3. Supply Chain Modernization, 4. Store Operations Optimization, 5. E-commerce Optimization, 6. Data-Driven Decision Making, 7. Process Automation, 8. Partner with Technology Providers, 9. Employee Development and Training, 10. Continuous Monitoring and Improvement. For each strategy, provide specific implementation tactics, metrics for measuring success, and examples of how Fortune 500 retailers have successfully implemented these strategies.",
  stream: false
});

const options = {
  hostname: 'localhost',
  port: 11434,
  path: '/api/generate',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': postData.length
  }
};

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  
  res.on('data', (chunk) => {
    console.log(`Response: ${chunk.toString()}`);
  });
  
  res.on('end', () => {
    console.log('Request completed');
  });
});

req.on('error', (e) => {
  console.error(`Problem with request: ${e.message}`);
});

req.write(postData);
req.end();