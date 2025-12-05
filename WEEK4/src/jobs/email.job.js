require('dotenv').config({ path: '.env.local' });
const { Queue, Worker } = require('bullmq');
const Redis = require('ioredis');
const nodemailer = require('nodemailer');
const logger = require('../utils/logger');

// Redis connection using ioredis
const redisConnection = new Redis({
  host: 'localhost',
  port: 6379,
  maxRetriesPerRequest: null
});

// Gmail setup
const emailTransporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_USER,
    pass: process.env.GMAIL_APP_PASSWORD
  }
});

// Create email queue with Redis connection
const emailQueue = new Queue('emails', { connection: redisConnection });

// Process emails in background
new Worker('emails', async (job) => {
  const { to, subject, body } = job.data;
  
  await emailTransporter.sendMail({
    from: process.env.GMAIL_USER,
    to,
    subject,
    html: body
  });
  
  logger.info(`Email sent to ${to}`);
}, 
{
  connection: redisConnection,
  limiter: {
    max: 10,
    duration: 1000
  }
});

// Send welcome email
async function sendWelcomeEmail(user, requestId) {
  await emailQueue.add('welcome', {
    to: user.email,
    subject: 'Welcome!',
    body: `<h1>Hi ${user.name}!</h1><p>Welcome to our platform.</p>`,
    requestId
  }, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000
    }
  });
  
  logger.info('Welcome email queued', { requestId });
}

module.exports = { sendWelcomeEmail };


