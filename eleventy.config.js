import markdownIt from "markdown-it";

function stripHtml(value = "") {
  return value
    .replace(/<pre[\s\S]*?<\/pre>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

function truncateAtWord(value, limit = 180) {
  if (value.length <= limit) {
    return value;
  }

  const shortened = value.slice(0, limit + 1);
  const wordBoundary = shortened.lastIndexOf(" ");
  return `${shortened.slice(0, wordBoundary > 80 ? wordBoundary : limit).trim()}...`;
}

export default function (eleventyConfig) {
  eleventyConfig.setLibrary(
    "md",
    markdownIt({
      html: false,
      linkify: false,
      typographer: false,
    }),
  );

  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("output/pdf");
  eleventyConfig.addPassthroughCopy({ public: "/" });

  eleventyConfig.ignores.add("README.md");
  eleventyConfig.ignores.add("scripts/**");

  eleventyConfig.addGlobalData("site", {
    name: "Hasbi",
    title: "Hasbi - Full-Stack Software Engineer",
    description:
      "Portfolio of Hasbi, a full-stack software engineer focused on reliable, secure, and efficient software.",
    url: "https://hasmbly.github.io",
  });

  eleventyConfig.addCollection("posts", (collectionApi) =>
    collectionApi
      .getFilteredByGlob("./blogs/*.md")
      .sort((left, right) => right.date - left.date),
  );

  eleventyConfig.addFilter("dateMachine", (date) =>
    new Intl.DateTimeFormat("en-CA", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      timeZone: "UTC",
    }).format(date),
  );

  eleventyConfig.addFilter("dateReadable", (date) =>
    new Intl.DateTimeFormat("en", {
      year: "numeric",
      month: "long",
      day: "numeric",
      timeZone: "UTC",
    }).format(date),
  );

  eleventyConfig.addFilter("excerpt", (content) =>
    truncateAtWord(stripHtml(content)),
  );

  eleventyConfig.addFilter("postTags", (tags) => {
    if (!tags) {
      return [];
    }
    return Array.isArray(tags) ? tags : [tags];
  });

  return {
    dir: {
      input: ".",
      includes: "_includes",
      output: "_site",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: false,
  };
}
