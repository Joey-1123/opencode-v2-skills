#!/usr/bin/env node
"use strict";

const https = require("https");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const REPO = "Joey-1123/opencode-v2-skills";
const SKILLS_DIR = process.env.HOME + "/.config/opencode/skills";
const CACHE_FILE = path.join(require("os").homedir(), ".cache", "opencode-skills", "catalog.json");
const SKILLS_API = `https://api.github.com/repos/${REPO}/contents/skills`;
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/main/skills`;
const TAR_URL = `https://api.github.com/repos/${REPO}/tarball`;

const chalk = require("chalk");

// Helper: fetch JSON from URL
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { "User-Agent": "opencode-skills/1.0" } }, (res) => {
      let data = "";
      res.on("data", chunk => data += chunk);
      res.on("end", () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on("error", reject);
  });
}

// Helper: download file from URL to path
function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { "User-Agent": "opencode-skills/1.0" } }, (res) => {
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(); });
      file.on("error", reject);
    }).on("error", reject);
  });
}

// Build catalog from GitHub API
async function buildCatalog() {
  try {
    const contents = await fetchJSON(SKILLS_API);
    const catalog = [];
    for (const item of contents) {
      if (item.type !== "dir") continue;
      const skillMdUrl = `${RAW_BASE}/${item.name}/SKILL.md`;
      let desc = "";
      try {
        const mdContent = await new Promise((resolve, reject) => {
          https.get(skillMdUrl, { headers: { "User-Agent": "opencode-skills/1.0" } }, (res) => {
            let data = "";
            res.on("data", chunk => data += chunk);
            res.on("end", () => resolve(data));
          }).on("error", reject);
        });
        const match = mdContent.match(/description:\s*(.+)/);
        if (match) desc = match[1].trim();
      } catch {}
      catalog.push({ name: item.name, description: desc, path: item.name });
    }
    // Save cache
    const cacheDir = path.dirname(CACHE_FILE);
    if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
    fs.writeFileSync(CACHE_FILE, JSON.stringify(catalog, null, 2));
    return catalog;
  } catch (e) {
    // Fallback to cache
    if (fs.existsSync(CACHE_FILE)) {
      return JSON.parse(fs.readFileSync(CACHE_FILE, "utf-8"));
    }
    throw new Error("Failed to fetch catalog: " + e.message);
  }
}

// Command: list
async function cmdList() {
  const catalog = await buildCatalog();
  const installed = getInstalled();
  console.log(`\n📦 ${chalk.bold(catalog.length)} skills available (${installed.length} installed)\n`);
  for (const s of catalog) {
    const status = installed.includes(s.name) ? chalk.green("✅") : chalk.gray("⬜");
    console.log(`  ${status} ${chalk.cyan(s.name)} — ${s.description}`);
  }
  console.log("");
}

// Command: search
async function cmdSearch(term) {
  const catalog = await buildCatalog();
  const results = catalog.filter(s =>
    s.name.toLowerCase().includes(term.toLowerCase()) ||
    s.description.toLowerCase().includes(term.toLowerCase())
  );
  if (results.length === 0) {
    console.log(`\n🔍 ${chalk.yellow("No skills found for \"" + term + "\"")}\n`);
    return;
  }
  console.log(`\n🔍 ${chalk.bold(results.length)} results for "${term}":\n`);
  for (const s of results) {
    console.log(`  ${chalk.cyan(s.name)} — ${s.description}`);
  }
  console.log("");
}

// Command: install
async function cmdInstall(name) {
  const installed = getInstalled();
  if (name) {
    // Install single skill
    const exists = installed.includes(name);
    if (exists) {
      console.log(`\n⚠️  ${chalk.yellow(name)} is already installed. Use /skill-manager update ${name}\n`);
      return;
    }
    const skillUrl = `${RAW_BASE}/${name}`;
    const dest = path.join(SKILLS_DIR, name);
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    // Download SKILL.md
    try {
      await downloadFile(`${skillUrl}/SKILL.md`, path.join(dest, "SKILL.md"));
      // Try to download scripts/
      try {
        const scripts = await fetchJSON(`${SKILLS_API}/${name}/contents/scripts`);
        if (!fs.existsSync(path.join(dest, "scripts"))) fs.mkdirSync(path.join(dest, "scripts"), { recursive: true });
        for (const f of scripts) {
          await downloadFile(f.download_url, path.join(dest, "scripts", f.name));
          fs.chmodSync(path.join(dest, "scripts", f.name), 0o755);
        }
      } catch {}
      // Try references/
      try {
        const refs = await fetchJSON(`${SKILLS_API}/${name}/contents/references`);
        if (!fs.existsSync(path.join(dest, "references"))) fs.mkdirSync(path.join(dest, "references"), { recursive: true });
        for (const f of refs) {
          await downloadFile(f.download_url, path.join(dest, "references", f.name));
        }
      } catch {}
      // Try assets/
      try {
        const assets = await fetchJSON(`${SKILLS_API}/${name}/contents/assets`);
        if (!fs.existsSync(path.join(dest, "assets"))) fs.mkdirSync(path.join(dest, "assets"), { recursive: true });
        for (const f of assets) {
          if (f.type === "dir") {
            // Handle subdirectories
            downloadDir(f.download_url, path.join(dest, "assets", f.name));
          } else {
            await downloadFile(f.download_url, path.join(dest, "assets", f.name));
          }
        }
      } catch {}
      console.log(`\n✅ Installed ${chalk.cyan(name)}\n`);
    } catch (e) {
      console.log(`\n❌ Failed to install ${name}: ${e.message}\n`);
    }
  } else {
    // Install all via tarball
    console.log("\n⬇️  Downloading all skills...");
    const tarPath = "/tmp/opencode-skills.tar.gz";
    await downloadFile(TAR_URL, tarPath);
    const destDir = SKILLS_DIR;
    if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
    execSync(`tar -xzf ${tarPath} -C ${destDir} --strip-components=2`, { stdio: "ignore" });
    fs.unlinkSync(tarPath);
    const count = getInstalled().length;
    console.log(`\n✅ ${chalk.bold(count)} skills installed!\n`);
  }
}

// Helper: download directory (simplified)
async function downloadDir(url, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  // Just download the directory listing and fetch files
  try {
    const items = await fetchJSON(url);
    for (const item of items) {
      if (item.type === "dir") {
        await downloadDir(item.download_url, path.join(dest, item.name));
      } else {
        await downloadFile(item.download_url, path.join(dest, item.name));
      }
    }
  } catch {}
}

// Command: uninstall
function cmdUninstall(name) {
  const dest = path.join(SKILLS_DIR, name);
  if (!fs.existsSync(dest)) {
    console.log(`\n⚠️  ${name} is not installed.\n`);
    return;
  }
  fs.rmSync(dest, { recursive: true });
  console.log(`\n🗑️  Removed ${chalk.cyan(name)}\n`);
}

// Command: update
async function cmdUpdate(name) {
  if (name) {
    // Update single skill
    const dest = path.join(SKILLS_DIR, name);
    if (!fs.existsSync(dest)) {
      console.log(`\n⚠️  ${name} is not installed. Use /skill-manager install ${name}\n`);
      return;
    }
    // Re-install that skill
    await cmdInstall(name);
  } else {
    // Update all: re-install all
    console.log("\n⬇️  Updating all skills...");
    const tarPath = "/tmp/opencode-skills-update.tar.gz";
    await downloadFile(TAR_URL, tarPath);
    execSync(`tar -xzf ${tarPath} -C ${SKILLS_DIR} --strip-components=2 --keep-newer`, { stdio: "ignore" });
    fs.unlinkSync(tarPath);
    console.log("\n✅ All skills updated!\n");
  }
}

// Helper: get installed skills
function getInstalled() {
  if (!fs.existsSync(SKILLS_DIR)) return [];
  try {
    return fs.readdirSync(SKILLS_DIR).filter(d => {
      const stat = fs.statSync(path.join(SKILLS_DIR, d));
      return stat.isDirectory();
    });
  } catch { return []; }
}

// Parse CLI args
const args = process.argv.slice(2);
const command = args[0];
const arg = args[1];

async function main() {
  switch (command) {
    case "list":
      await cmdList();
      break;
    case "search":
      if (!arg) { console.log("\nUsage: opencode-skills search <term>\n"); process.exit(1); }
      await cmdSearch(arg);
      break;
    case "install":
      await cmdInstall(arg);
      break;
    case "uninstall":
      if (!arg) { console.log("\nUsage: opencode-skills uninstall <name>\n"); process.exit(1); }
      cmdUninstall(arg);
      break;
    case "update":
      await cmdUpdate(arg);
      break;
    case "categories":
      // Show categories
      const catalog = await buildCatalog();
      const cats = {
        "🎨 Design & UI": ["py-side6-gui-design", "modern-web-design", "skill-creator"],
        "📄 Documentation": ["readme-generator", "technical-documentation-with-claude", "changelog-generator"],
        "🎬 Animation": ["animate", "motion-framer", "gsap-scrolltrigger", "react-spring-physics", "animejs", "lottie-animations", "review-animations", "improve-animations", "animation-vocabulary", "find-animation-opportunities"],
        "🎯 3D & WebGL": ["threejs-webgl", "react-three-fiber", "babylonjs-engine", "playcanvas-engine", "aframe-webxr", "lightweight-3d-effects", "pixijs-2d", "blender-web-pipeline", "spline-interactive", "rive-interactive", "substance-3d-texturing"],
        "📜 Scroll": ["barba-js", "locomotive-scroll", "scroll-reveal-libraries"],
        "🧩 Components": ["animated-component-libraries", "web3d-integration-patterns"],
      };
      for (const [cat, skills] of Object.entries(cats)) {
        console.log(`\n### ${cat}`);
        for (const s of skills) {
          const found = catalog.find(c => c.name === s);
          console.log(`  ${found ? "✅" : "⬜"} ${s}${found ? " — " + found.description : ""}`);
        }
      }
      console.log("");
      break;
    default:
      console.log(`
📦 OpenCode V2 Skills Marketplace

Usage: opencode-skills <command> [args]

Commands:
  list                    Browse all skills
  search <term>           Search skills by keyword
  install [name]          Install skill(s). Omit name for all
  uninstall <name>        Remove a skill
  update [name]           Update skill(s). Omit name for all
  categories              Show skills by category

Examples:
  opencode-skills list
  opencode-skills search animation
  opencode-skills install py-side6-gui-design
  opencode-skills install
  opencode-skills update animate
`);
  }
}

main().catch(console.error);
