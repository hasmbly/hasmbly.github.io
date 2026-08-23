import { rm } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const workspace = path.resolve(process.cwd());
const output = path.resolve(workspace, "_site");

if (path.dirname(output) !== workspace || path.basename(output) !== "_site") {
  throw new Error(`Refusing to clean unexpected output path: ${output}`);
}

await rm(output, { recursive: true, force: true });
