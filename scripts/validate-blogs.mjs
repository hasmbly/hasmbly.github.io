import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const blogsDirectory = path.resolve("blogs");
const allowedFilename = /^[a-z0-9]+(?:-[a-z0-9]+)*\.md$/;
const isoDate = /^\d{4}-\d{2}-\d{2}$/;

function frontMatterValue(frontMatter, field) {
  const match = frontMatter.match(new RegExp(`^${field}:\\s*(.+?)\\s*$`, "m"));
  return match?.[1]?.replace(/^['"]|['"]$/g, "").trim() || "";
}

function isCalendarDate(value) {
  if (!isoDate.test(value)) {
    return false;
  }

  const parsed = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(parsed.valueOf()) && parsed.toISOString().slice(0, 10) === value;
}

const entries = await readdir(blogsDirectory, { withFileTypes: true });
const markdownFiles = entries.filter((entry) => entry.isFile() && entry.name.endsWith(".md"));
const errors = [];

for (const entry of markdownFiles) {
  if (!allowedFilename.test(entry.name)) {
    errors.push(`${entry.name}: filename must use lowercase kebab-case.`);
  }

  const source = await readFile(path.join(blogsDirectory, entry.name), "utf8");
  const frontMatterMatch = source.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!frontMatterMatch) {
    errors.push(`${entry.name}: missing YAML front matter.`);
    continue;
  }

  const title = frontMatterValue(frontMatterMatch[1], "title");
  const date = frontMatterValue(frontMatterMatch[1], "date");

  if (!title) {
    errors.push(`${entry.name}: title is required.`);
  }
  if (!isCalendarDate(date)) {
    errors.push(`${entry.name}: date must be a valid YYYY-MM-DD value.`);
  }
}

if (errors.length) {
  console.error(`Blog validation failed:\n- ${errors.join("\n- ")}`);
  process.exit(1);
}

console.log(`Validated ${markdownFiles.length} blog post${markdownFiles.length === 1 ? "" : "s"}.`);
