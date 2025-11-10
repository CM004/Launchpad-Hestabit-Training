#!/usr/bin/env node
// ensures that Node.js is used to run the script regardless of different environments and installations,
// where the path to node might vary

const fs = require('fs');
const { promises: fsp } = fs;
const yargs = require('yargs');

// Parse command-line arguments using yargs
const argv = yargs(process.argv.slice(2))
  .option('file', { type: 'string', demandOption: true })
  .option('top', { type: 'number', default: 10 })
  .option('minLen', { type: 'number', default: 5 })
  .option('unique', { type: 'boolean', default: true })
  .argv;

/*
  --- Benchmark helper: readRangeBytes ---
  Read a byte range from the file using a stream and count bytes read.
  This is used only for measuring I/O performance (executionTime and memoryUsage).
  It does not convert to string or perform any word processing so the benchmark
  measures read overhead only.
*/
function readRangeBytes(filePath, start, end) {
  return new Promise((resolve, reject) => {
    let total = 0;
    const rs = fs.createReadStream(filePath, { start, end });
    rs.on('data', chunk => total += chunk.length);
    rs.on('end', () => resolve(total));
    rs.on('error', reject);
  });
}

/*
  --- Benchmark function: benchmarkConcurrency ---
  For a given concurrency level:
  1) split the file into roughly equal byte ranges,
  2) issue parallel reads (Promise.all),
  3) measure time using Date.now() (milliseconds) and memory using process.memoryUsage().rss (bytes).
  Returns an object { concurrency, executionTime, memoryUsage }.
*/
async function benchmarkConcurrency(filePath, concurrency) {
  const stat = await fsp.stat(filePath);
  const fileSize = stat.size;
  if (fileSize === 0) return { concurrency, executionTime: 0, memoryUsage: 0 };

  const chunkSize = Math.ceil(fileSize / concurrency);
  const tasks = [];

  for (let i = 0; i < concurrency; i++) {
    const start = i * chunkSize;
    const end = Math.min((i + 1) * chunkSize - 1, fileSize - 1);
    tasks.push(readRangeBytes(filePath, start, end));
  }

  const memBefore = process.memoryUsage().rss;
  const t0 = Date.now();

  // perform the parallel reads
  await Promise.all(tasks);

  const t1 = Date.now();
  const memAfter = process.memoryUsage().rss;

  const executionTime = t1 - t0;      // milliseconds
  const memoryUsage = memAfter - memBefore; // bytes

  return { concurrency, executionTime, memoryUsage };
}

(async () => {
  try {
    if (!fs.existsSync(argv.file)) {
      console.error('Error reading file: not found', argv.file);
      process.exit(1);
    }

    // Run benchmarks for concurrency levels 1, 4, 8 (measure only time + memory)
    const levels = [1, 4, 8];
    const perfSummary = [];

    for (const c of levels) {
      console.log(`Running benchmark for concurrency=${c}`);
      const entry = await benchmarkConcurrency(argv.file, c);
      perfSummary.push(entry);
      console.log(` => executionTime=${entry.executionTime}ms memoryUsage=${entry.memoryUsage} bytes`);
    }

    // write performance summary (assumes logs/ and output/ already exist)
    await fsp.writeFile('logs/perf-summary.json', JSON.stringify(perfSummary, null, 2), 'utf8');
    console.log('Saved logs/perf-summary.json');

    /*
      --- Now compute full stats exactly for the whole file (single read) ---
      Read the entire file, process words, and produce:
      totalWords, uniqueWords, longestWord, shortestWord, topWords
    */
    // Read the file asynchronously
    const text = await fsp.readFile(argv.file, 'utf8');

    // Process the text
    const words = text
      .toLowerCase()
      .split(/\s+/)
      .filter(word => word.length >= argv.minLen);  // Filter words based on minLen

    // Count word frequencies
    const wordCounts = words.reduce((acc, word) => {
      acc[word] = (acc[word] || 0) + 1;
      return acc;
    }, {});

    const uniqueWords = Object.keys(wordCounts);
    let longestWord = '';
    let shortestWord = '';

    uniqueWords.forEach(word => {
      if (word.length > longestWord.length) longestWord = word;
      if (word.length < shortestWord.length || shortestWord.length == 0) shortestWord = word;
    });

    const results = {
      totalWords: words.length,
      uniqueWords: uniqueWords.length,
      longestWord,
      shortestWord,
      topWords: Object.entries(wordCounts)
        .sort(([, a], [, b]) => b - a)  // Sort by frequency
        .slice(0, argv.top)  // Get the top N
        .map(([word, count]) => ({ word, count }))  // Format each word-count pair
    };

    console.log(`Total words: ${words.length}`);
    console.log(`Unique words: ${uniqueWords.length}`);
    console.log(`Longest word: ${longestWord}`);
    console.log(`Shortest word: ${shortestWord}`);
    if (argv.top > 0) {
      console.log(`Top ${argv.top} most repeated words:\n${results.topWords.map(({ word, count }) => `${word}: ${count}`).join('\n')}`);
    }

    // Save final stats (assumes output/ exists)
    await fsp.writeFile('output/stats.json', JSON.stringify(results, null, 2), 'utf8');

  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  }
})();
