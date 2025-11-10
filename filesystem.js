const fs = require('fs');
const process = require('process');
const { execSync } = require('child_process');

const filePath = '/home/chandramohan/Desktop/day1/largefile.txt';
const resultPath = 'logs/day1-perf.json';
const results = {}; // Object to hold both benchmark results

const createTestFile = () => {
  if (fs.existsSync(filePath)) {
    console.log('File already exists, skipping file creation.');
    return; 
  }

  // Use dd command 
  try {
    execSync(`dd if=/dev/urandom of=${filePath} bs=1M count=51`);
    console.log(`Test file created with random data: 51MB`);
  } catch (error) {
    console.error('Error creating file with dd:', error);
  }
};

//  warms up the OS cache
const warmCache = (callback) => {
  fs.createReadStream(filePath)
    .on('data', () => {}) // read through the file
    .on('end', () => {
      console.log('Cache warmed up for file.');
      callback();
    })
    .on('error', (err) => {
      console.error('Error warming cache:', err);
      callback();
    });
};

const benchmarkReadFile = (callback) => {
  const startMemory = process.memoryUsage().rss;
  const start = Date.now();

  fs.readFile(filePath, (err, data) => {
    if (err) {
      console.error('Error reading file:', err);
      return;
    }

    const endMemory = process.memoryUsage().rss;
    const end = Date.now();

    results.readFile = {
      time: end - start,
      memory: endMemory - startMemory
    };
    console.log(
      `Buffer (fs.readFile): { executionTime: ${results.readFile.time} ms, memoryUsed: ${results.readFile.memory} bytes }`
    );

    callback();
  });
};

const benchmarkStreamFile = (callback) => {
  const startMemory = process.memoryUsage().rss;
  const start = Date.now();

  fs.createReadStream(filePath)
    .on('data', () => {}) // Consume data
    .on('end', () => {
      const endMemory = process.memoryUsage().rss;
      const end = Date.now();

      results.stream = {
        time: end - start,
        memory: endMemory - startMemory
      };
      console.log(
        `Buffer (fs.createReadStream): { executionTime: ${results.stream.time} ms, memoryUsed: ${results.stream.memory} bytes }`
      );

      callback();
    })
    .on('error', (err) => {
      console.error('Stream error:', err);
    });
};

const saveResults = () => {
  fs.writeFileSync(resultPath, JSON.stringify(results, null, 2));
  console.log(`Results saved to ${resultPath}`);
};

// warm cache before each benchmark
createTestFile();

warmCache(() => {
  benchmarkReadFile(() => {
    console.log('readFile benchmark complete');
    warmCache(() => {
      benchmarkStreamFile(() => {
        console.log('stream benchmark complete');
        saveResults();
      });
    });
  });
});
