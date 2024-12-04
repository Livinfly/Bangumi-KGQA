// wiki_parser.mjs (注意文件扩展名为 .mjs)

import { parse2 } from '@bgm38/wiki';

const wikiString = process.argv[2];  // 通过命令行传入的字符串

const [error, w] = parse2(wikiString);

if (error) {
  console.error(JSON.stringify({ error: error.message }));
} else {
  console.log(JSON.stringify({ result: w }));
}
