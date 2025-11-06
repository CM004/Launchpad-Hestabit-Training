const fs = require('fs');
const { LoremIpsum } = require('lorem-ipsum'); //destructive assignment

// Initialize the lorem-ipsum generator
const lorem = new LoremIpsum();

const totalWords = 200000;
let generatedWords = 0;

// Create a writable stream for the corpus.txt file
const writeStream = fs.createWriteStream('corpus.txt');

while (generatedWords < totalWords) {
  const chunkSize = 1000; 
  const words = lorem.generateWords(chunkSize);
  
  writeStream.write(words + ' '); //write the chunk to the file
  generatedWords += chunkSize; //generatedWords will increase by 1000
}

writeStream.end();
console.log(`Generated corpus.txt with ${totalWords} words`);
