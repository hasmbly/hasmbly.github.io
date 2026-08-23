function deriveDescription(markdown = "") {
  const body = markdown.replace(/^---[\s\S]*?---\s*/, "");
  const paragraphs = body
    .replace(/```[\s\S]*?```/g, "")
    .split(/\r?\n\s*\r?\n/)
    .map((paragraph) =>
      paragraph
        .replace(/^#{1,6}\s+/gm, "")
        .replace(/^>\s?/gm, "")
        .replace(/^[-*+]\s+/gm, "")
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
        .replace(/[`*_~]/g, "")
        .replace(/\s+/g, " ")
        .trim(),
    )
    .filter(Boolean);

  const firstParagraph = paragraphs[0] || "A post from Hasbi's software engineering blog.";
  if (firstParagraph.length <= 180) {
    return firstParagraph;
  }

  const shortened = firstParagraph.slice(0, 181);
  const boundary = shortened.lastIndexOf(" ");
  return `${shortened.slice(0, boundary > 80 ? boundary : 180).trim()}...`;
}

export default {
  layout: "post.njk",
  isPost: true,
  navSection: "blogs",
  eleventyComputed: {
    description: (data) => deriveDescription(data.page.rawInput),
  },
};
